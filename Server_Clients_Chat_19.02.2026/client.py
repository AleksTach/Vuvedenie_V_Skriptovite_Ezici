import json
import socket
import threading
from datetime import datetime
import queue
import tkinter as tk
from tkinter import ttk, scrolledtext

PALETTE = {
    'background': '#0b1220',
    'panel': '#141f33',
    'accent': '#ff9f1c',
    'secondary': '#2ec4b6',
    'text': '#f7f7ff',
    'muted': '#7a869a',
    'input_bg': '#1c2b45'
}


class ClientApp:
    def __init__(self, master):
        self.master = master
        master.title('Client Console')
        master.configure(bg=PALETTE['background'])
        master.geometry('720x480')

        self.sock = None
        self.recv_thread = None
        self.events = queue.Queue()
        self.connected = False

        self.host_var = tk.StringVar(value='10.101.211.51')
        self.port_var = tk.StringVar(value='50007')
        self.name_var = tk.StringVar(value='User')
        self.status_var = tk.StringVar(value='Disconnected')
        self.bytes_var = tk.IntVar(value=0)

        self._build_style()
        self._build_layout()
        self.master.protocol('WM_DELETE_WINDOW', self._on_close)
        self.master.after(120, self._process_events)

    def _build_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Dark.TLabel', background=PALETTE['background'], foreground=PALETTE['text'])
        style.configure('Panel.TFrame', background=PALETTE['panel'])
        style.configure('Accent.TButton', background=PALETTE['accent'], foreground=PALETTE['background'])
        style.configure('StatLabel.TLabel', background=PALETTE['panel'], foreground=PALETTE['muted'])
        style.configure('StatValue.TLabel', background=PALETTE['panel'], foreground=PALETTE['text'], font=('Segoe UI', 18, 'bold'))
        style.map('Accent.TButton', background=[('active', '#ffb347')])

    def _build_layout(self):
        head = tk.Frame(self.master, bg=PALETTE['background'])
        head.pack(fill='x', padx=20, pady=(16, 8))
        ttk.Label(head, text='Client Control', style='Dark.TLabel', font=('Segoe UI', 20, 'bold')).pack(side='left')
        self.status_chip = tk.Label(head, textvariable=self.status_var, bg=PALETTE['panel'], fg=PALETTE['text'], padx=12, pady=4)
        self.status_chip.pack(side='right')

        settings = tk.Frame(self.master, bg=PALETTE['background'])
        settings.pack(fill='x', padx=20, pady=4)
        self._labeled_entry(settings, 'Host', self.host_var)
        self._labeled_entry(settings, 'Port', self.port_var, width=7)
        self._labeled_entry(settings, 'Name', self.name_var)
        self.toggle_btn = ttk.Button(settings, text='Connect', style='Accent.TButton', command=self._toggle_connection)
        self.toggle_btn.pack(side='left', padx=(12, 0))

        stats = tk.Frame(self.master, bg=PALETTE['background'])
        stats.pack(fill='x', padx=20, pady=(4, 10))
        self._stat(stats, 'Bytes received', self.bytes_var)

        main = tk.Frame(self.master, bg=PALETTE['background'])
        main.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        self.log = scrolledtext.ScrolledText(main, state='disabled', wrap='word', bg=PALETTE['panel'], fg=PALETTE['text'], insertbackground=PALETTE['text'], borderwidth=0)
        self.log.pack(fill='both', expand=True)

        composer = tk.Frame(self.master, bg=PALETTE['background'])
        composer.pack(fill='x', padx=20, pady=(0, 20))
        ttk.Label(composer, text='Message', style='Dark.TLabel').pack(side='left', padx=(0, 12))
        entry_frame = tk.Frame(composer, bg=PALETTE['background'])
        entry_frame.pack(side='left', fill='x', expand=True)
        self.entry = tk.Entry(entry_frame, bg=PALETTE['input_bg'], fg=PALETTE['text'], insertbackground=PALETTE['text'], relief='solid', borderwidth=1, highlightthickness=1, highlightcolor=PALETTE['accent'], highlightbackground=PALETTE['panel'])
        self.entry.pack(fill='x', expand=True, ipady=8)
        self.entry.bind('<Return>', self._send_message)
        self.entry.focus_set()
        self.send_btn = ttk.Button(composer, text='Send', command=self._send_message)
        self.send_btn.pack(side='left', padx=(10, 0))

    def _labeled_entry(self, parent, label, variable, width=12):
        frame = tk.Frame(parent, bg=PALETTE['background'])
        frame.pack(side='left', padx=(0, 12))
        ttk.Label(frame, text=label, style='Dark.TLabel').pack(anchor='w')
        entry = ttk.Entry(frame, textvariable=variable, width=width)
        entry.pack()
        return entry

    def _stat(self, parent, title, variable):
        box = tk.Frame(parent, bg=PALETTE['panel'], padx=14, pady=12)
        box.pack(side='left', padx=(0, 12))
        ttk.Label(box, text=title.upper(), style='StatLabel.TLabel').pack(anchor='w')
        ttk.Label(box, textvariable=variable, style='StatValue.TLabel').pack(anchor='w')

    def _toggle_connection(self):
        if self.connected:
            self._disconnect()
            return
        try:
            port = int(self.port_var.get())
        except ValueError:
            self._append_log('Invalid port number')
            return
        host = self.host_var.get().strip()
        if not host:
            self._append_log('Host cannot be empty')
            return
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            self.recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
            self.recv_thread.start()
            self.connected = True
            self.status_var.set('Connected')
            self.status_chip.config(bg=PALETTE['secondary'])
            self.toggle_btn.config(text='Disconnect')
            self._append_log(f'Connected to {host}:{port}')
        except OSError as exc:
            self._append_log(f'Connection failed: {exc}')
            self.sock = None

    def _disconnect(self):
        self.connected = False
        self.status_var.set('Disconnected')
        self.status_chip.config(bg=PALETTE['panel'])
        self.toggle_btn.config(text='Connect')
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                self.sock.close()
            except OSError:
                pass
        self.sock = None
        self._append_log('Disconnected')

    def _recv_loop(self):
        buffer = b''
        try:
            while self.connected and self.sock:
                data = self.sock.recv(4096)
                if not data:
                    self.events.put({'type': 'system', 'text': 'Server closed connection'})
                    break
                buffer += data
                self.events.put({'type': 'bytes', 'value': len(data)})
                while b'\n' in buffer:
                    line, buffer = buffer.split(b'\n', 1)
                    if not line:
                        continue
                    try:
                        payload = json.loads(line.decode('utf-8'))
                    except json.JSONDecodeError:
                        continue
                    self.events.put({'type': 'packet', 'payload': payload})
        except OSError:
            self.events.put({'type': 'system', 'text': 'Connection error'})
        finally:
            self.connected = False
            if self.sock:
                try:
                    self.sock.close()
                except OSError:
                    pass
                self.sock = None
            self.events.put({'type': 'status', 'text': 'Disconnected'})

    def _process_events(self):
        while not self.events.empty():
            evt = self.events.get()
            type_ = evt.get('type')
            if type_ == 'packet':
                self._handle_packet(evt.get('payload', {}))
            elif type_ == 'system':
                self._append_log(evt.get('text', ''))
            elif type_ == 'bytes':
                self.bytes_var.set(self.bytes_var.get() + evt.get('value', 0))
            elif type_ == 'status':
                status = evt.get('text', '')
                if status:
                    self.status_var.set(status)
                if status == 'Connected':
                    self.status_chip.config(bg=PALETTE['secondary'])
                else:
                    self.status_chip.config(bg=PALETTE['panel'])
                    self.toggle_btn.config(text='Connect')
        self.master.after(120, self._process_events)

    def _handle_packet(self, payload):
        kind = payload.get('type')
        if kind == 'history':
            for item in payload.get('items', []):
                self._render_message(item)
        elif kind in ('message', 'system'):
            self._render_message(payload)

    def _render_message(self, item):
        name = item.get('name') or 'Unknown'
        text = item.get('text') or ''
        stamp = item.get('time')
        prefix = ''
        if stamp:
            try:
                parsed = datetime.fromisoformat(stamp)
                prefix = f"[{parsed.strftime('%H:%M:%S')}] "
            except ValueError:
                prefix = f"[{stamp}] "
        if item.get('type') == 'system':
            self._append_log(f"{prefix}[SERVER] {text}")
        else:
            self._append_log(f"{prefix}{name}: {text}")

    def _send_message(self, event=None):
        text = self.entry.get().strip()
        if not text or not self.sock:
            return
        packet = {
            'type': 'message',
            'name': self.name_var.get().strip() or 'User',
            'text': text,
            'time': datetime.utcnow().isoformat()
        }
        try:
            self.sock.sendall((json.dumps(packet, ensure_ascii=False) + '\n').encode('utf-8'))
            self.entry.delete(0, 'end')
        except OSError:
            self._append_log('Failed to send message')
            self._disconnect()

    def _append_log(self, text):
        if not text:
            return
        self.log.config(state='normal')
        self.log.insert('end', text + '\n')
        self.log.yview('end')
        self.log.config(state='disabled')

    def _on_close(self):
        self._disconnect()
        self.master.destroy()


def main():
    root = tk.Tk()
    ClientApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()