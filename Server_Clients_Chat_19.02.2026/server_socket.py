import json
import socket
import threading
from datetime import datetime
from pathlib import Path
import queue
import tkinter as tk
from tkinter import ttk, scrolledtext

PALETTE = {
	'background': '#111d2a',
	'panel': '#162436',
	'accent': '#00c2ff',
	'muted': '#7c8594',
	'text': '#f0f2f5',
	'ok': '#36d399',
	'error': '#ff6b6b'
}

HISTORY_LIMIT = 500
HISTORY_FILE = Path(__file__).with_name('chat_history.json')


class ChatServer:
	"""Threaded TCP server that reports lifecycle events back to the UI."""

	def __init__(self, host, port, event_queue):
		self.host = host
		self.port = port
		self.events = event_queue
		self.server_sock = None
		self.running = threading.Event()
		self.thread = None
		self.clients = {}
		self.lock = threading.Lock()
		self.history = self._load_history()
		self.message_counter = len(self.history)
		self._emit({'type': 'metrics', 'messages': self.message_counter})

	def start(self):
		if self.running.is_set():
			return
		self.running.set()
		self.thread = threading.Thread(target=self._run, daemon=True)
		self.thread.start()

	def stop(self):
		self.running.clear()
		if self.server_sock:
			try:
				self.server_sock.close()
			except OSError:
				pass
		self._shutdown_clients()

	def broadcast(self, payload, exclude=None):
		with self.lock:
			targets = list(self.clients.keys())
		for conn in targets:
			if conn is exclude:
				continue
			try:
				conn.sendall(payload)
			except OSError:
				self._drop_client(conn)

	def send_server_message(self, text):
		if not text:
			return
		entry = self._build_entry(name='Server', text=text, entry_type='system')
		self._append_history(entry)
		self.broadcast(self._encode(entry))
		self._emit({'type': 'log', 'text': f'[server] {text}'})

	def _run(self):
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
				srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				srv.bind((self.host, self.port))
				srv.listen()
				srv.settimeout(0.5)
				self.server_sock = srv
				self._emit({'type': 'status', 'state': 'running', 'host': self.host, 'port': self.port})
				self._emit({'type': 'log', 'text': f'Listening on {self.host}:{self.port}'})
				while self.running.is_set():
					try:
						conn, addr = srv.accept()
					except socket.timeout:
						continue
					except OSError:
						break
					threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True).start()
		except OSError as exc:
			self._emit({'type': 'log', 'text': f'Server error: {exc}'})
		finally:
			self._emit({'type': 'status', 'state': 'stopped'})
			self._shutdown_clients()
			self.server_sock = None

	def _handle_client(self, conn, addr):
		label = f'{addr[0]}:{addr[1]}'
		with self.lock:
			self.clients[conn] = label
		self._emit({'type': 'clients', 'items': list(self.clients.values())})
		self._emit({'type': 'log', 'text': f'{label} connected'})
		self._send_history(conn)
		buffer = b''
		try:
			while self.running.is_set():
				data = conn.recv(1024)
				if not data:
					break
				buffer += data
				while b'\n' in buffer:
					line, buffer = buffer.split(b'\n', 1)
					if not line:
						continue
					self._process_payload(line, label)
		except OSError:
			pass
		finally:
			self._drop_client(conn)
			conn.close()
			self._emit({'type': 'clients', 'items': list(self.clients.values())})
			self._emit({'type': 'log', 'text': f'{label} disconnected'})

	def _drop_client(self, conn):
		with self.lock:
			self.clients.pop(conn, None)

	def _shutdown_clients(self):
		with self.lock:
			connections = list(self.clients.keys())
		self.clients.clear()
		for conn in connections:
			try:
				conn.shutdown(socket.SHUT_RDWR)
			except OSError:
				pass
			try:
				conn.close()
			except OSError:
				pass
		self._emit({'type': 'clients', 'items': []})

	def _emit(self, payload):
		self.events.put(payload)

	def _build_entry(self, name, text, entry_type='message', timestamp=None):
		return {
			'type': entry_type,
			'name': name,
			'text': text,
			'time': timestamp or datetime.utcnow().isoformat()
		}

	def _append_history(self, entry):
		self.history.append(entry)
		if len(self.history) > HISTORY_LIMIT:
			self.history = self.history[-HISTORY_LIMIT:]
		self.message_counter = len(self.history)
		self._emit({'type': 'metrics', 'messages': self.message_counter})
		self._persist_history()

	def _persist_history(self):
		try:
			HISTORY_FILE.write_text(json.dumps(self.history, ensure_ascii=False, indent=2), encoding='utf-8')
		except OSError:
			self._emit({'type': 'log', 'text': 'Failed to persist history'})

	def _load_history(self):
		if HISTORY_FILE.exists():
			try:
				with HISTORY_FILE.open('r', encoding='utf-8') as fh:
					data = json.load(fh)
					if isinstance(data, list):
						sanitized = []
						for item in data[-HISTORY_LIMIT:]:
							if isinstance(item, dict):
								sanitized.append(item)
							else:
								sanitized.append(self._build_entry(name='Legacy', text=str(item)))
						return sanitized
			except (OSError, json.JSONDecodeError):
				pass
		return []

	def _send_history(self, conn):
		packet = {'type': 'history', 'items': self.history}
		try:
			conn.sendall(self._encode(packet))
		except OSError:
			pass

	def _process_payload(self, payload_bytes, label):
		try:
			obj = json.loads(payload_bytes.decode('utf-8'))
		except json.JSONDecodeError:
			self._emit({'type': 'log', 'text': f'Malformed payload from {label}'})
			return
		if obj.get('type') != 'message':
			return
		text = (obj.get('text') or '').strip()
		if not text:
			return
		name = obj.get('name') or label
		entry = self._build_entry(name=name, text=text)
		self._append_history(entry)
		self.broadcast(self._encode(entry))
		self._emit({'type': 'log', 'text': f'{label} → {text}'})

	def _encode(self, payload):
		return (json.dumps(payload, ensure_ascii=False) + '\n').encode('utf-8')


class ServerDashboard:
	def __init__(self, master):
		self.master = master
		master.title('Chat Server Dashboard')
		master.configure(bg=PALETTE['background'])
		master.geometry('820x540')

		self.events = queue.Queue()
		self.server = None
		self.status_var = tk.StringVar(value='Offline')
		self.host_var = tk.StringVar(value='0.0.0.0')
		self.port_var = tk.StringVar(value='50007')
		self.client_count = tk.IntVar(value=0)
		self.message_count = tk.IntVar(value=0)

		self._build_style()
		self._build_layout()
		self.master.protocol('WM_DELETE_WINDOW', self._on_close)
		self.master.after(120, self._poll_events)

	def _build_style(self):
		style = ttk.Style()
		style.theme_use('clam')
		style.configure('DarkFrame.TLabelframe', background=PALETTE['panel'], foreground=PALETTE['text'])
		style.configure('Dark.TLabel', background=PALETTE['panel'], foreground=PALETTE['text'])
		style.configure('Header.TLabel', background=PALETTE['background'], foreground=PALETTE['text'], font=('Segoe UI', 16, 'bold'))
		style.configure('Accent.TButton', background=PALETTE['accent'], foreground='#041421')
		style.map('Accent.TButton', background=[('active', '#33d6ff')])
		style.configure('Muted.TLabel', background=PALETTE['panel'], foreground=PALETTE['muted'])

	def _build_layout(self):
		head = tk.Frame(self.master, bg=PALETTE['background'])
		head.pack(fill='x', padx=20, pady=(18, 6))
		ttk.Label(head, text='Live Server Monitor', style='Header.TLabel').pack(side='left')
		self.status_badge = tk.Label(head, textvariable=self.status_var, bg=PALETTE['error'], fg=PALETTE['background'], font=('Segoe UI', 11, 'bold'), padx=12, pady=4)
		self.status_badge.pack(side='right')

		config = tk.Frame(self.master, bg=PALETTE['background'])
		config.pack(fill='x', padx=20, pady=6)
		self.host_entry = self._build_entry(config, 'Host', self.host_var)
		self.port_entry = self._build_entry(config, 'Port', self.port_var, width=8)
		self.toggle_btn = ttk.Button(config, text='Start Server', style='Accent.TButton', command=self._toggle_server)
		self.toggle_btn.pack(side='left', padx=(12, 0))

		stats = tk.Frame(self.master, bg=PALETTE['background'])
		stats.pack(fill='x', padx=20, pady=(6, 12))
		self._stat_box(stats, 'Connected', self.client_count)
		self._stat_box(stats, 'Messages relayed', self.message_count)

		main = tk.Frame(self.master, bg=PALETTE['background'])
		main.pack(fill='both', expand=True, padx=20, pady=(0, 20))

		left = ttk.LabelFrame(main, text='Active Clients', style='DarkFrame.TLabelframe')
		left.pack(side='left', fill='y', padx=(0, 12), ipadx=6, ipady=6)
		self.client_list = tk.Listbox(left, bg=PALETTE['panel'], fg=PALETTE['text'], bd=0, highlightthickness=0, width=26, activestyle='none', selectbackground=PALETTE['accent'])
		self.client_list.pack(fill='both', expand=True)

		right = ttk.LabelFrame(main, text='Traffic Log', style='DarkFrame.TLabelframe')
		right.pack(side='left', fill='both', expand=True)
		self.log = scrolledtext.ScrolledText(right, state='disabled', wrap='word', bg='#0f1824', fg=PALETTE['text'], insertbackground=PALETTE['text'], borderwidth=0)
		self.log.pack(fill='both', expand=True)

		composer = tk.Frame(self.master, bg=PALETTE['background'])
		composer.pack(fill='x', padx=20, pady=(0, 20))
		ttk.Label(composer, text='Broadcast', style='Dark.TLabel').pack(side='left', padx=(0, 10))
		self.broadcast_entry = ttk.Entry(composer)
		self.broadcast_entry.pack(side='left', fill='x', expand=True)
		self.broadcast_entry.bind('<Return>', self._send_broadcast)
		self.broadcast_btn = ttk.Button(composer, text='Send to all', command=self._send_broadcast)
		self.broadcast_btn.pack(side='left', padx=(10, 0))

	def _build_entry(self, parent, label, variable, width=14):
		wrapper = tk.Frame(parent, bg=PALETTE['background'])
		wrapper.pack(side='left', padx=(0, 12))
		ttk.Label(wrapper, text=label, style='Dark.TLabel').pack(anchor='w')
		entry = ttk.Entry(wrapper, textvariable=variable, width=width)
		entry.pack()
		return entry

	def _stat_box(self, parent, title, variable):
		box = tk.Frame(parent, bg=PALETTE['panel'], padx=18, pady=14)
		box.pack(side='left', padx=(0, 12))
		ttk.Label(box, text=title.upper(), style='Muted.TLabel').pack(anchor='w')
		ttk.Label(box, textvariable=variable, style='Dark.TLabel', font=('Segoe UI', 20, 'bold')).pack(anchor='w')

	def _toggle_server(self):
		if self.server and self.server.running.is_set():
			self._stop_server()
			return
		try:
			port = int(self.port_var.get())
		except ValueError:
			self._append_log('Invalid port value')
			return
		host = self.host_var.get().strip() or '0.0.0.0'
		self.server = ChatServer(host, port, self.events)
		self.server.start()
		self.toggle_btn.config(text='Stop Server')
		self.host_entry.config(state='disabled')
		self.port_entry.config(state='disabled')

	def _stop_server(self):
		if not self.server:
			return
		self.server.stop()
		self.server = None
		self.status_var.set('Offline')
		self.status_badge.config(bg=PALETTE['error'])
		self.toggle_btn.config(text='Start Server')
		self.host_entry.config(state='normal')
		self.port_entry.config(state='normal')

	def _send_broadcast(self, event=None):
		text = self.broadcast_entry.get().strip()
		if not text or not self.server:
			return
		self.server.send_server_message(text)
		self.broadcast_entry.delete(0, 'end')

	def _poll_events(self):
		while not self.events.empty():
			evt = self.events.get()
			type_ = evt.get('type')
			if type_ == 'log':
				self._append_log(evt.get('text', ''))
			elif type_ == 'status':
				self._set_status(evt.get('state'))
			elif type_ == 'clients':
				self._update_clients(evt.get('items', []))
			elif type_ == 'metrics':
				self.message_count.set(evt.get('messages', 0))
		self.master.after(120, self._poll_events)

	def _set_status(self, state):
		if state == 'running':
			self.status_var.set('Online')
			self.status_badge.config(bg=PALETTE['ok'])
		else:
			self.status_var.set('Offline')
			self.status_badge.config(bg=PALETTE['error'])
		if state != 'running':
			self.toggle_btn.config(text='Start Server')
			self.host_entry.config(state='normal')
			self.port_entry.config(state='normal')

	def _append_log(self, text):
		if not text:
			return
		self.log.config(state='normal')
		self.log.insert('end', f'{text}\n')
		self.log.yview('end')
		self.log.config(state='disabled')

	def _update_clients(self, items):
		self.client_list.delete(0, 'end')
		for item in items:
			self.client_list.insert('end', item)
		self.client_count.set(len(items))

	def _on_close(self):
		self._stop_server()
		self.master.destroy()


def main():
	root = tk.Tk()
	ServerDashboard(root)
	root.mainloop()


if __name__ == '__main__':
	main()