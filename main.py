import requests
import time
import tkinter as tk
from tkinter import messagebox, simpledialog 
import webbrowser
import threading
import json
import pystray 
from PIL import Image, ImageDraw 
from pystray import MenuItem as item 
import os
from winotify import Notification
import asyncio

stop_flag = threading.Event()
pause_flag = threading.Event()

with open('config.json', "r") as config_file:
  config = json.load(config_file)
  
api_url = config['api_url']
pr_url = config['pr_url']
token = config['token'] 
notify = config.get('notify_new_pr', True)

headers = {
  'Authorization': f'Bearer {token}',
  'Accept': 'application/vnd.github.v3+json'
}

seen_pr_numbers = []

import io

def get_open_prs():
  try:
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    # Raise an HTTPError for bad responses
    return response.json()
  except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
  except requests.exceptions.RequestException as req_err:
    print(f'Request error occurred: {req_err}')
  except ValueError as json_err:
    print(f'JSON decode error: {json_err}')
    print(f'Response content: {response.content}')
  return []

def show_custom_toast(title, msg): 
  toast = Notification(
    app_id="PR Notifier",
    title=title,
    msg=msg,
    duration='short'
  )
  toast.show()

def show_toast_pr(pr):
  toast = Notification(
    app_id="PR Notifier", 
    title=pr["title"] + " #" + str(pr["number"]),
    msg=" by " + pr["user"]["login"],
    duration='short'
  )
  toast.add_actions(label="Open Pull Request", launch=pr["html_url"])
  toast.show()

def notify_new_pr(pr):
  if notify:
    show_toast_pr(pr)

def on_stop(icon, item):
  stop_flag.set()
  os._exit(0)
  icon.stop()

def on_clicked(icon, item):
  print('Played')
  icon.icon = Image.open("resources/github.png")
  pause_flag.clear()

def on_pause(icon, item):
  print('Paused')
  icon.icon = Image.open("resources/github_paused.png")
  pause_flag.set()

def on_details(icon, item):
  webbrowser.open_new(pr_url)

def on_edit_config(icon, item):
  def show_modal():
    def save_config(new_config):
      with open('config.json', 'w') as config_file:
        json.dump(new_config, config_file, indent=4)
      messagebox.showinfo("Config", "Configuration saved successfully")
    
    new_pr = tk.Tk()
    new_pr.withdraw()

    top = tk.Toplevel(new_pr)
    top.title("Edit Config")
    top.iconbitmap("resources/github.ico")
    
    tk.Label(top, text="API URL:").grid(row=0, column=0, padx=10, pady=5)
    api_url_entry = tk.Entry(top, width=50)
    api_url_entry.grid(row=0, column=1, padx=10, pady=5) 
    api_url_entry.insert(0, config['api_url'])

    tk.Label(top, text="PR URL:").grid(row=1, column=0, padx=10, pady=5)
    pr_url_entry = tk.Entry(top, width=50)
    pr_url_entry.grid(row=1, column=1, padx=10, pady=5)
    pr_url_entry.insert(0, config['pr_url'])

    tk.Label(top, text="Token:").grid(row=2, column=0, padx=10, pady=5)
    token_entry = tk.Entry(top, width=50, show="*")
    token_entry.grid(row=2, column=1, padx=10, pady=5)
    token_entry.insert(0, config['token'])

    tk.Label(top, text="Loop Duration:").grid(row=3, column=0, padx=10, pady=5)
    loop_duration_entry = tk.Entry(top, width=50)
    loop_duration_entry.grid(row=3, column=1, padx=10, pady=5) 
    loop_duration_entry.insert(0, config['loop_duration'])
    
    notify_new_pr_var = tk.BooleanVar(value=config.get('notify_new_pr', False))
    tk.Checkbutton(top, text="Notify on New PR", variable=notify_new_pr_var).grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def on_save():
      new_api_url = api_url_entry.get()
      new_pr_url = pr_url_entry.get()
      new_token = token_entry.get()
      new_loop_duration = loop_duration_entry.get()
      notify_new_pr = notify_new_pr_var.get()
      
      if new_api_url and new_token and new_loop_duration:
        config['api_url'] = new_api_url
        config['pr_url'] = new_pr_url
        config['token'] = new_token
        config['loop_duration'] = int(new_loop_duration)
        config['notify_new_pr'] = notify_new_pr
        save_config(config)
        top.destroy()
    
    save_button = tk.Button(top, text="Save", command=on_save)
    save_button.grid(row=5, column=0, columnspan=2, pady=10)
    top.mainloop()
    new_pr.destroy()
  
  threading.Thread(target=show_modal).start()

def main():
  global token
  icon_image = Image.open("resources/github.png")
  icon = pystray.Icon("test_icon", icon_image, "PR Notifier")
  icon.menu = pystray.Menu(
    item('Details', on_details),  
    item('Config', on_edit_config),
    item('Close', on_stop)
  )
  
  icon_thread = threading.Thread(target=icon.run)
  icon_thread.start()

  while True:
    if not pause_flag.is_set() and token != "":
      prs = get_open_prs()
      print(seen_pr_numbers)
      if prs:
        if len(prs['items']) > 5:
          icon.icon = Image.open("resources/github_+5.png")
        else:
          icon.icon = Image.open("resources/github_"+str(len(prs['items']))+".png")
        for pr in prs['items']:
          print(f"Number of PRs: {len(prs['items'])}")
          print(pr['html_url'])
          if pr['html_url'] not in seen_pr_numbers:
            notify_new_pr(pr)
            seen_pr_numbers.append(pr['html_url'])
      else:
        print('No open PRs found.')
      time.sleep(config['loop_duration'])
    
if __name__ == '__main__':    
  main()
