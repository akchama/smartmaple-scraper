import datetime
import sys

import customtkinter as ctk
from pymongo import MongoClient

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

import subprocess
import signal

process = None

import os

def fetch_data():
    global process
    print_log("Fetch button clicked")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    spider_name = combobox_var.get()
    scrapy_path = os.path.join(current_dir, '..', 'venv', 'bin', 'scrapy')
    process = subprocess.Popen([scrapy_path, 'crawl', spider_name], start_new_session=True, cwd=current_dir)


def pause_data():
    global process
    print_log("Pause button clicked")

    if process is not None:
        os.killpg(os.getpgid(process.pid), signal.SIGSTOP)


def resume_data():
    global process
    print_log("Resume button clicked")

    if process is not None:
        os.killpg(os.getpgid(process.pid), signal.SIGCONT)


def reset_data():
    client = MongoClient('mongodb://localhost:27017')

    # Connect to the database
    db = client["smartmaple"]

    # Drop selected collection
    db[combobox_var.get()].drop()

    print_log(f"Collection {combobox_var.get()} dropped successfully")


def combobox_callback(choice):
    print_log("combobox dropdown clicked:", choice)


def on_close():
    global process
    print_log("Window is closing")

    # Check if the process is not None and is still running
    if process is not None:
        try:
            process.terminate()  # send SIGTERM
            process.wait(timeout=0.2)
            print("Subprocess terminated")
        except subprocess.TimeoutExpired:
            print("Subprocess did not terminate in time - sending SIGKILL")
            process.kill()  # send SIGKILL
        except Exception as e:
            print(f"Error while terminating subprocess: {e}")

    app.destroy()  # destroy the window

def print_log(*args, **kwargs):
    text = ' '.join(map(str, args)) + '\n'
    now = datetime.datetime.now()
    timestamp = now.strftime("[%Y-%m-%d %H:%M:%S] ")  # Format the timestamp

    # Make the textbox editable, insert the text, then make it read-only again
    log_textbox.configure(state='normal')
    log_textbox.insert('end', timestamp + text)  # Prepend the timestamp to the message
    log_textbox.see('end')  # Scroll to the end
    log_textbox.configure(state='disabled')

    print(timestamp + text, end='')  # print to console


app = ctk.CTk()  # Create CTk window
app.protocol("WM_DELETE_WINDOW", on_close)  # bind the on_close function to the window's close event
app.geometry("480x360")  # Increase the window size to make more room for the widgets
app.resizable(0, 0)
app.eval('tk::PlaceWindow . center')

fetch_button = ctk.CTkButton(master=app, text="Fetch", command=fetch_data)
fetch_button.place(relx=0.2, rely=0.2, anchor=ctk.CENTER)

reset_button = ctk.CTkButton(master=app, text="Reset", command=reset_data)
reset_button.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

pause_button = ctk.CTkButton(master=app, text="Pause", command=pause_data)
pause_button.place(relx=0.2, rely=0.3, anchor=ctk.CENTER)

resume_button = ctk.CTkButton(master=app, text="Resume", command=resume_data)
resume_button.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

combobox_var = ctk.StringVar(value="kitapyurdu")
combobox = ctk.CTkComboBox(app, values=["kitapyurdu", "kitapsepeti"],
                           command=combobox_callback, variable=combobox_var)
combobox.place(relx=0.2, rely=0.1, anchor=ctk.CENTER)  # Move the combobox up

log_textbox = ctk.CTkTextbox(app, height=200, width=460, state="disabled")
log_textbox.place(relx=0.02, rely=0.4)  # Move the log textbox down

try:
    app.mainloop()
except SystemExit:
    # User stopped the script, so stop the subprocess as well
    if process is not None and process.poll() is None:  # If the process is running
        if sys.platform == "win32":
            process.terminate()
        else:  # Unix-like system
            os.killpg(process.pid, signal.SIGTERM)
