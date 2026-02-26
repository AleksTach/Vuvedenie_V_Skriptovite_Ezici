import webbrowser
from time import sleep

def webBrowser():
  websites = [
    "https://www.python.org/",
    "https://www.twitter.com/",
    "https://www.youtube.com/",
  ]
  choice = input("Enter the number of the website you want to open (1-3): ")
  print(f"Opening website: {websites[int(choice) - 1]}")
  sleep(2)
  webbrowser.open(websites[int(choice) - 1])

if __name__ == "__main__":
  webBrowser()