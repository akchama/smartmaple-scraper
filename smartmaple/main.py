import os
import subprocess

import customtkinter as ctk
from pymongo import MongoClient

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


import os
import subprocess
import sys
import psutil  # pip install psutil

# Determine OS
if sys.platform.startswith('win'):
    is_windows = True
elif sys.platform.startswith('linux'):
    is_windows = False
else:
    print("Unsupported operating system. Only Windows and Linux are supported.")
    sys.exit(1)

process = None

def fetch_data():
    global process
    print("Fetch button clicked")

    os.chdir('/home/abdullah/PycharmProjects/smartmaple-scraper/smartmaple')

    # This command is equivalent to "scrapy crawl kitapyurdu" in the terminal
    process = subprocess.Popen('scrapy crawl kitapyurdu', shell=True)

def pause_data():
    global process
    print("Pause button clicked")

    if process is not None:
        if is_windows:
            p = psutil.Process(process.pid)
            for proc in p.children(recursive=True):
                proc.suspend()
        else:
            process.send_signal(subprocess.signal.SIGSTOP)

def resume_data():
    global process
    print("Resume button clicked")

    if process is not None:
        if is_windows:
            p = psutil.Process(process.pid)
            for proc in p.children(recursive=True):
                proc.resume()
        else:
            process.send_signal(subprocess.signal.SIGCONT)


def reset_data():
    client = MongoClient('mongodb://localhost:27017')

    # Connect to the database
    db = client["smartmaple"]

    # Drop selected collection
    db[combobox_var.get()].drop()

    print(f"Collection {combobox_var.get()} dropped successfully")

def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

app = ctk.CTk()  # Create CTk window
app.geometry("400x240")

fetch_button = ctk.CTkButton(master=app, text="Fetch", command=fetch_data)
fetch_button.place(relx=0.2, rely=0.5, anchor=ctk.CENTER)

reset_button = ctk.CTkButton(master=app, text="Reset", command=reset_data)
reset_button.place(relx=0.8, rely=0.5, anchor=ctk.CENTER)

pause_button = ctk.CTkButton(master=app, text="Pause", command=pause_data)
pause_button.place(relx=0.2, rely=0.7, anchor=ctk.CENTER)

resume_button = ctk.CTkButton(master=app, text="Resume", command=resume_data)
resume_button.place(relx=0.8, rely=0.7, anchor=ctk.CENTER)

combobox_var = ctk.StringVar(value="kitapyurdu")
combobox = ctk.CTkComboBox(app, values=["kitapyurdu", "kitapsepeti"],
                            command=combobox_callback, variable=combobox_var)
combobox.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

app.mainloop()
