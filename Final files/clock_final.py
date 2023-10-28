from tkinter import *
from PIL import Image, ImageTk, ImageFilter
import os
import time
from datetime import datetime
from math import sin, cos, radians
from pyttsx3 import init
import pytz
import pygame
import threading
from tkinter import ttk  # This imports the ttk module
import tkinter as tk

pygame.mixer.init()

# Create main Tkinter window
master = Tk()
master.title("Talking Clock")

# Set the background color of the entire clock to black
master.configure(bg="black")

# Background pictures
background_image1 = Image.open("bg1.png")
background_image1 = ImageTk.PhotoImage(background_image1)
background_image2 = Image.open('bg2.png')
background_image2 = background_image2.resize((720, 730))
background_image2 = ImageTk.PhotoImage(background_image2)
current_style = 1


def switch_clock_style():
    '''
    Switch the clock style between background images.
    '''
    global current_style
    if current_style == 1:
        canvas.create_image(0, 0, anchor="nw", image=background_image2)
        current_style = 2
    else:
        canvas.create_image(0, 0, anchor="nw", image=background_image1)
        current_style = 1

# Create a canvas and display background images
canvas = Canvas(master, bg="black", width=720, height=600)
canvas.pack(pady=20)  # Add some padding to separate the canvas from the buttons

canvas.create_image(0, 0, anchor="nw", image=background_image1)

# Create a frame to separate the digital clock from other elements
spacer_frame = Frame(master, bg='black')
spacer_frame.pack(fill='x', pady=0)

# Create a label to display the digital time
time_label = Label(master, font=('Helvetica', 30), bg='white')
time_label.pack()


# Set default time zone to Shanghai
selected_timezone = "Asia/Shanghai"

def select_timezone(value):
    '''
    Update time zone selection.
    '''
    global selected_timezone
    selected_timezone = value
    update_time()

def open_alarm_settings():
    """
    Open a window for setting the alarm time and configuring the alarm sound.
    Additional option to set snooze time.
    """
    def save_alarm():
        global alarm_time, alarm_tone
        # Use global var to store alarm setting values
        alarm_hour_val = alarm_hour.get()  # Assuming this is now in 24-hour format
        alarm_minute_val = alarm_minute.get()
        alarm_tone = alarm_tone_var.get()

        alarm_time = f"{alarm_hour_val}:{alarm_minute_val}:00"  # in the 24-hours format
        print("Alarm time:", alarm_time)

        # Set the alarm:
        try:
            datetime.strptime(alarm_time, "%H:%M:%S")
            # Create a thread to run the alarm function
            alarm_thread = threading.Thread(target=lambda: run_alarm(alarm_time)) # add further args if needed
            
            alarm_thread.start()
        except ValueError:
            print("Invalid time format. Please use the HH:MM:SS format.")

        alarm_settings.destroy()  # close the setting windows
          


    # Function to run the alarm in a separate thread
    def run_alarm(alarm_time):
        # Initialize the pygame mixer
        # You should call this once before you use any other pygame sound functions
        pygame.mixer.init()
        
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            if current_time == alarm_time:
                print("Time to Wake up!")
                # Load sound (alarm tone)
                pygame.mixer.music.load(alarm_tone)  
                # Play the sound
                pygame.mixer.music.play()
                                
                break  # Exit the loop once the alarm sound has been played
                
            time.sleep(1)  # Check the current time every second

    alarm_settings = Toplevel(master)  # create a new window
    alarm_settings.title("Set Alarm")

    # Create a new frame for all the setting components
    settings_frame = ttk.Frame(alarm_settings)
    settings_frame.pack(pady=10)

    # Add components for setting the alarm time
    alarm_hour = ttk.Combobox(settings_frame, values=[f"{i:02d}" for i in range(1, 25)], width=5)
    alarm_hour.set("1")
    alarm_hour.pack(side="left", padx=5)

    alarm_minute = ttk.Combobox(settings_frame, values=[f"{i:02d}" for i in range(60)], width=5)
    alarm_minute.set("00")
    alarm_minute.pack(side="left", padx=5)


    # Setting the components for choosing alarm ringtones
    alarm_tone_var = StringVar()

    # Create buttons for different alarm tones
    ttk.Radiobutton(settings_frame, text="clock-alarm", value="clock-alarm-8761.mp3", variable=alarm_tone_var).pack(side="left", padx=5)
    ttk.Radiobutton(settings_frame, text="ringtone", value="ringtone-126505.mp3", variable=alarm_tone_var).pack(side="left", padx=5)
    ttk.Radiobutton(settings_frame, text="tic-tac", value="tic-tac-27828.mp3", variable=alarm_tone_var).pack(side="left", padx=5)

    # Create 'Save alarm' button
    ttk.Button(alarm_settings, text="Save Alarm", command=save_alarm).pack(pady=10)

    # Alarm setting window main loop
    alarm_settings.mainloop()

def set_alarm():
    global alarm_time, alarm_tone
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        if current_time == alarm_time:
            print("Alarm ringing...")
            if check_alarm_tone_path():
                playsound(alarm_tone)       
            break

        time.sleep(30)



def start_alarm_thread():
    """
    Start a separate thread to handle the alarm.
    """
    alarm_thread = threading.Thread(target=set_alarm)
    alarm_thread.start()


def get_current_time():
    '''
    Get the current time based on the selected time zone.
    '''
    now = datetime.now(pytz.timezone(selected_timezone))
    current_time = now.strftime("%H:%M:%S")
    return current_time

def play_current_time_audio():
    '''
    Play audio of current time.
    '''
    global audio_folder
    
    # Berlin
    if selected_timezone == "Europe/Berlin":
        current_time = datetime.now(pytz.timezone("Europe/Berlin")).time()
        hour = current_time.hour
        minute = current_time.minute
        period = "am" if hour < 12 else "pm"
        hour_12 = hour if 0 < hour <= 12 else abs(hour - 12)
        hour_file = f"DE_{hour_12}h.mp3"
        min_file = f"DE_{minute}m.mp3" if minute != 0 else ""
        period_file = f"DE_{period}.mp3"

        folder_path = "DE_slicing"

        hour_path = os.path.join(folder_path, hour_file)
        pygame.mixer.music.load(hour_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(1)

        if min_file:
            min_path = os.path.join(folder_path, min_file)
            pygame.mixer.music.load(min_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                    time.sleep(1)

        pm_path = os.path.join(folder_path, period_file)
        pygame.mixer.music.load(pm_path)
        pygame.mixer.music.play()
        # print(f"Playing file: {pm_path}")

        while pygame.mixer.music.get_busy():
            time.sleep(1)

    # Shanghai
    if selected_timezone == "Asia/Shanghai":
        current_time = datetime.now(pytz.timezone("Asia/Shanghai")).time()
        hour = current_time.hour
        minute = current_time.minute
        period = "am" if hour < 12 else "pm"
        hour_12 = hour if 0 < hour <= 12 else abs(hour - 12)
        hour_file = f"CN_{hour_12}h.mp3"
        min_file = f"CN_{minute}m.mp3"
        period_file = f"CN_{period}.mp3"

        folder_path = "CN_slicing"

        pm_path = os.path.join(folder_path, period_file)
        pygame.mixer.music.load(pm_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(1)

        hour_path = os.path.join(folder_path, hour_file)
        pygame.mixer.music.load(hour_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(1)

        if min_file:
            min_path = os.path.join(folder_path, min_file)
            pygame.mixer.music.load(min_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():  
                    time.sleep(1)



    # New York
    if selected_timezone == "America/New_York":
        current_time = datetime.now(pytz.timezone("America/New_York")).time()
        hour = current_time.hour
        minute = current_time.minute
        period = "am" if hour < 12 else "pm"
        hour_12 = hour if 0 < hour <= 12 else abs(hour - 12)
        hour_file = f"EN_{hour_12}h.mp3.mp3"
        min_file = f"EN_{minute}m.mp3.mp3" if minute != 0 else ""
        period_file = f"EN_{period}.mp3.mp3"

        folder_path = "EN_slicing"

        hour_path = os.path.join(folder_path, hour_file)
        pygame.mixer.music.load(hour_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(1)

        if min_file:
            min_path = os.path.join(folder_path, min_file)
            pygame.mixer.music.load(min_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                    time.sleep(1)

        pm_path = os.path.join(folder_path, period_file)
        pygame.mixer.music.load(pm_path)
        pygame.mixer.music.play()
        # print(f"Playing file: {pm_path}")

        while pygame.mixer.music.get_busy():
            time.sleep(1)

    # Local
    local = "Europe/Amsterdam"
    if selected_timezone == local:
        current_time = datetime.now(pytz.timezone("Europe/Amsterdam")).time()
        hour = current_time.hour
        minute = current_time.minute
        period = "am" if hour < 12 else "pm"
        hour_12 = hour if 0 < hour <= 12 else abs(hour - 12)
        hour_file = f"EN_{hour_12}h.mp3.mp3"
        min_file = f"EN_{minute}m.mp3.mp3" if minute != 0 else ""
        period_file = f"EN_{period}.mp3.mp3"

        folder_path = "EN_slicing"

        hour_path = os.path.join(folder_path, hour_file)
        pygame.mixer.music.load(hour_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(1)

        if min_file:
            min_path = os.path.join(folder_path, min_file)
            pygame.mixer.music.load(min_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(1)

        pm_path = os.path.join(folder_path, period_file)
        pygame.mixer.music.load(pm_path)
        pygame.mixer.music.play()
        # print(f"Playing file: {pm_path}")

        while pygame.mixer.music.get_busy():
            time.sleep(1)



# Create an instance of Frame in the 'master' window
frame = Frame(master)
frame.pack() 


# Create a dict of timezones with corresponding labels
timezones = {"Asia/Shanghai": "Asia/Shanghai", "Europe/Berlin": "Europe/Berlin", "America/New_York": "America/New_York", "local":"Europe/Amsterdam"}

# Create a StringVar to store the timezone and set it to the initial value
timezone_var = tk.StringVar()
timezone_var.set(selected_timezone)

# Create an OptionMenu widget to display the list of timezones
timezone_menu = tk.OptionMenu(frame, timezone_var, *timezones, command=lambda value: select_timezone(timezones[value]))
timezone_menu.grid(row=1, column=0)

# Create a button to read the time
read_time_button = tk.Button(frame, text="Read the Time", command=play_current_time_audio)
read_time_button.grid(row=1, column=1)

# Create a button to set the alarm
set_alarm_button = tk.Button(frame, text="Set Alarm", command=open_alarm_settings)
set_alarm_button.grid(row=1, column=2)

# Create a button to switch clock styles
style_button = tk.Button(frame, text='Switch Style', command=switch_clock_style)
style_button.grid(row=0, column=0, columnspan=3)

def update_time():
    '''
    Update the time and configure the time label.
    '''
    current_time = get_current_time()
    time_label.config(text=current_time)
    master.after(1000, update_time)

def update_clock_pointer():
    '''
    Update clock pointer based on selected timezone.
    '''
    now = datetime.now(pytz.timezone(selected_timezone))
    current_time = now.time()

    # Pointer angle calculation
    hours = current_time.hour
    minutes = current_time.minute
    seconds = current_time.second

    hour_angle = 90 - (hours % 12 + minutes / 60) * 360 / 12
    minute_angle = 90 - minutes * 360 / 60
    second_angle = 90 - seconds * 360 / 60

    # Pointers' center
    center_x = 362
    center_y = 365

    # Length of pointers
    hour_length = 60
    minute_length = 100
    second_length = 150
    hour_x = center_x + hour_length * cos(radians(hour_angle))
    hour_y = center_y - hour_length * sin(radians(hour_angle))
    minute_x = center_x + minute_length * cos(radians(minute_angle))
    minute_y = center_y - minute_length * sin(radians(minute_angle))
    second_x = center_x + second_length * cos(radians(second_angle))
    second_y = center_y - second_length * sin(radians(second_angle))

    # Delete the old clock pointers
    canvas.delete("pointer")

    # Paint new clock pointers
    canvas.create_line(center_x, center_y, hour_x, hour_y, width=8, fill='Black', tags="pointer")
    canvas.create_line(center_x, center_y, minute_x, minute_y, width=5, fill='Black', tags="pointer")
    canvas.create_line(center_x, center_y, second_x, second_y, width=2, fill='Black', tags="pointer")

    # Schedule function to be called agin after 1 second
    master.after(1000, update_clock_pointer)

# Update time and clock pointers
update_time()
update_clock_pointer()

# Enter main loop for GUI application
master.mainloop()

