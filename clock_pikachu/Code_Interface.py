from tkinter import *
from PIL import Image, ImageTk, ImageFilter
import time
from datetime import datetime
from math import radians, sin, cos
from tkinter import Label, Button
from pyttsx3 import init
import pytz
import threading
from tkinter import ttk  # This imports the ttk module

master = Tk()
master.title("Pikachu Clock")

# Set the background color of the entire clock to black
master.configure(bg="black")  

#Background pictures
background_image1 = Image.open("pikaqiu.png")
background_image1 = ImageTk.PhotoImage(background_image1)
background_image2 = Image.open('class.jpg')
background_image2 = background_image2.resize((480, 480))
background_image2 = ImageTk.PhotoImage(background_image2)


current_style=1

def switch_clock_style():
    global current_style
    if current_style == 1:
        canvas.create_image(0, 0, anchor="nw", image=background_image2)
        current_style = 2
    else:
        canvas.create_image(0, 0, anchor="nw", image=background_image1)
        current_style = 1

# Switch style Button
"""style_button = Button(master, text='Switch Style', command=switch_clock_style, font=('Helvetica', 24), bg='light goldenrod')
style_button.pack()"""


# Adjust the place of pictures
canvas = Canvas(master, bg="black", width=480, height=450)
canvas.pack(pady=20)  # Add some padding to separate the canvas from the buttons

canvas.create_image(0, 0, anchor="nw", image=background_image1)

# Digital time clock
time_label = Label(master, font=('Helvetica', 24), bg='black', fg='white')  # Set the background to black and font color to white
time_label.pack()




# digital time clock
time_label = Label(master, font=('Helvetica', 24), bg='light blue')
time_label.pack()

# Initialize the text-to-speech engine from pyttsx3
engine = init()

def update_clock_pointer():
    current_time = time.localtime()
    now = datetime.now()
    digital_time = now.strftime("%I:%M:%S %p")
    time_label.config(text=digital_time)
    hours = current_time.tm_hour
    minutes = current_time.tm_min
    seconds = current_time.tm_sec
    # Angle of three hands
    hour_angle = 90 - (hours % 12 + minutes / 60) * 360 / 12
    minute_angle = 90 - minutes * 360 / 60
    second_angle = 90 - seconds * 360 / 60


    # Three pointers' middle place
    center_x = 237
    center_y = 237

    # Length of three hands
    hour_length = 130
    minute_length = 200
    second_length = 200
    hour_x = center_x + hour_length * cos(radians(hour_angle))
    hour_y = center_y - hour_length * sin(radians(hour_angle))
    minute_x = center_x + minute_length * cos(radians(minute_angle))
    minute_y = center_y - minute_length * sin(radians(minute_angle))
    second_x = center_x + second_length * cos(radians(second_angle))
    second_y = center_y - second_length * sin(radians(second_angle))

    # delete the old pointer
    canvas.delete("pointer")

    # Paint hands
    canvas.create_line(center_x, center_y, hour_x, hour_y, width=4, fill='Crimson', tags="pointer")
    canvas.create_line(center_x, center_y, minute_x, minute_y, width=4, fill='DodgerBlue', tags="pointer")
    canvas.create_line(center_x, center_y, second_x, second_y, width=4, fill='LimeGreen', tags="pointer")
    master.after(1000, update_clock_pointer)

#Speak time
def speak_time():
    now = datetime.now()
    speaking_time = now.strftime("%I:%M %p")

    engine.say(f"The current time is {speaking_time}")
    engine.runAndWait()

#World clock
def show_world_clocks():
    world_clock_window = Toplevel(master)
    world_clock_window.title("World Clocks")

    #Label Dict, including different time zones' lables
    world_clock_labels = {}

    # Add different places
    timezones = {
        'Netherlands': 'Europe/Amsterdam',
        'China': 'Asia/Shanghai',
        'USA': 'America/New_York',
        'Romania': 'Europe/Bucharest'
    }

    for location, tz_name in timezones.items():
        world_clock_labels[location] = Label(world_clock_window, font=('Helvetica', 16), bg='light blue')
        world_clock_labels[location].pack()

    # Update the world clocks
    def update_clocks():
        for location, tz_name in timezones.items():
            tz = pytz.timezone(tz_name)
            current_time = datetime.now(tz).strftime("%I:%M:%S %p")
            world_clock_labels[location].config(text=f"{location}: {current_time}")
        # 继续定期调用update_clocks
        master.after(1000, update_clocks)

    # 在按钮点击后立即开始更新
    update_clocks()

    # 启动一个线程来更新时钟
    update_thread = threading.Thread(target=update_clocks)
    update_thread.daemon = True
    update_thread.start()

def check_alarm_tone_path():
    """to ensure that the audio path file really exist"""
    tones = ["alarm.mp3", "ringtone.mp3", "tic-tac.mp3"]
    for tone in tones:
        if not os.path.isfile(tone):
            print(f"Warning: Audio file {tone} does not exist. Please provide the correct path.")
            return False
    return True


def open_alarm_settings():
    """let user set alarm time and save it in a new setting frame,
    add snooze time function"""
    def save_alarm():
        global alarm_time, alarm_tone, snooze_duration  
        # use globle var to store alarm setting values
        alarm_hour_val = alarm_hour.get()
        alarm_minute_val = alarm_minute.get()
        am_pm = alarm_period.get()
        alarm_tone = alarm_tone_var.get()

        if am_pm == "PM" and alarm_hour_val != "12":
            alarm_hour_val = str(int(alarm_hour_val) + 12)
        elif am_pm == "AM" and alarm_hour_val == "12":
            alarm_hour_val = "00"

        alarm_time = f"{alarm_hour_val}:{alarm_minute_val}"  # in the 24-hours format
        snooze_duration = snooze_duration_entry.get()  # get the snooze time that user inputs

        #alarm_settings.destroy()  # close the setting windows

    alarm_settings = Toplevel(master)  # create a new window
    alarm_settings.title("Set Alarm")

    # create a new frame for all the setting components
    settings_frame = ttk.Frame(alarm_settings)
    settings_frame.pack(pady=10)

    # place the components of the alarm function
    alarm_hour = ttk.Combobox(settings_frame, values=[f"{i:02d}" for i in range(1, 13)], width=5)
    alarm_hour.set("12")
    alarm_hour.pack(side="left", padx=5)

    alarm_minute = ttk.Combobox(settings_frame, values=[f"{i:02d}" for i in range(60)], width=5)
    alarm_minute.set("00")
    alarm_minute.pack(side="left", padx=5)

    alarm_period = ttk.Combobox(settings_frame, values=["AM", "PM"], width=5)
    alarm_period.set("AM")
    alarm_period.pack(side="left", padx=5)

    # setting the components of ringtones
    alarm_tone_var = StringVar()
    ttk.Radiobutton(settings_frame, text="clock-alarm", value="clock-alarm-8761.mp3", variable=alarm_tone_var).pack(side="left", padx=5)
    ttk.Radiobutton(settings_frame, text="ringtone", value="ringtone-126505.mp3", variable=alarm_tone_var).pack(side="left", padx=5)
    ttk.Radiobutton(settings_frame, text="tic-tac", value="tic-tac-27828.mp3", variable=alarm_tone_var).pack(side="left", padx=5)

    # setting the components of snooze time
    ttk.Label(settings_frame, text="Snooze duration (minutes):").pack(side="left")
    snooze_duration_entry = ttk.Entry(settings_frame, width=5)
    snooze_duration_entry.pack(side="left")
    snooze_duration_entry.insert(0, "5")  # initialize it to be 5 min

    # save the button
    ttk.Button(alarm_settings, text="Save Alarm", command=save_alarm).pack(pady=10)

    alarm_settings.mainloop()

def set_alarm():
    #global snooze_time, alarm_time, alarm_tone
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        if current_time == alarm_time:
            print("Alarm ringing...")
            if check_alarm_tone_path():
                playsound(alarm_tone)
                #I think it should play the sound but not
            snooze_time = now
            break

        time.sleep(30)

def snooze_alarm():
    global snooze_time, alarm_time
    if snooze_time:
        snooze_minutes = int(snooze_duration.get())  
        snooze_time = datetime.now() + timedelta(minutes=snooze_minutes)
        alarm_time = (datetime.now() + timedelta(minutes=snooze_minutes)).strftime("%H:%M")
        print(f"Snoozed for {snooze_minutes} minutes...")
    else:
        print("No alarm to snooze.")

def start_alarm_thread():
    alarm_thread = threading.Thread(target=set_alarm)
    alarm_thread.start()

# Create an instance of Frame in the 'master' window
frame = Frame(master)
frame.pack()  # This positions the frame within the 'master' window

# Button styling
button_font = ('Helvetica', 16)
button_bg = 'black'
button_fg = 'white'

# Now, create the 'Show World Clocks' button inside the 'frame'
show_clocks_button = Button(frame, text='Show World Clocks', command=show_world_clocks, font=button_font, bg=button_bg, fg=button_fg)
show_clocks_button.pack(side='left', padx=10)  # Add some padding to separate the buttons

# Create a button to speak the time, also inside the 'frame'
speak_button = Button(frame, text='Speak Time', command=speak_time, font=button_font, bg=button_bg, fg=button_fg)
speak_button.pack(side='left', padx=10)  # Add some padding to separate the buttons

# Add a button in the main window to open the alarm page, also inside the 'frame'
alarm_button = Button(frame, text="Set My Alarm", command=open_alarm_settings, font=button_font, bg=button_bg, fg=button_fg)
alarm_button.pack(side='left', padx=10)  # Add some padding to separate the buttons

# Move the 'Switch Style' button to be on the same line as the digital time
style_button = Button(master, text='Switch Style', command=switch_clock_style, font=('Helvetica', 24), bg='black', fg='white')
style_button.pack(pady=10)  # Add some padding to separate the button from the digital time






# Update the pointer
update_clock_pointer()

# 启动窗口循环
master.mainloop()