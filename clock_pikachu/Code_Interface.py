from tkinter import *
from PIL import Image, ImageTk, ImageFilter
import time
from datetime import datetime
from math import radians, sin, cos
from pyttsx3 import init
import pytz
import threading
from tkinter import ttk  # This imports the ttk module
from english_helpers import get_current_time, slice_silence_english, combine_audio_english
from german_helpers import play_sound_german
from play_sound import play_sound_english
from mandarin_helpers import play_sound_mandarin
from playsound import playsound

master = Tk()
master.title("Pikachu Clock")

# Set the background color of the entire clock to black
master.configure(bg="black")

#Background pictures
background_image1 = Image.open("bg1.png")
background_image1 = ImageTk.PhotoImage(background_image1)
background_image2 = Image.open('bg2.png')
background_image2 = background_image2.resize((700, 700))
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

# Adjust the place of pictures
canvas = Canvas(master, bg="black", width=720, height=600)
canvas.pack(pady=20)  # Add some padding to separate the canvas from the buttons

canvas.create_image(0, 0, anchor="nw", image=background_image1)

# Digital time clock
spacer_frame = Frame(master, bg='black') 
spacer_frame.pack(fill='x', pady=0) 
# digital time clock 
time_label = Label(master, font=('Helvetica', 30), bg='white') 
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
    center_x = 362
    center_y = 365

    # Length of three hands
    hour_length = 60
    minute_length = 100
    second_length = 150
    hour_x = center_x + hour_length * cos(radians(hour_angle))
    hour_y = center_y - hour_length * sin(radians(hour_angle))
    minute_x = center_x + minute_length * cos(radians(minute_angle))
    minute_y = center_y - minute_length * sin(radians(minute_angle))
    second_x = center_x + second_length * cos(radians(second_angle))
    second_y = center_y - second_length * sin(radians(second_angle))

    # delete the old pointer
    canvas.delete("pointer")

    # Paint hands
    canvas.create_line(center_x, center_y, hour_x, hour_y, width=8, fill='Black', tags="pointer")
    canvas.create_line(center_x, center_y, minute_x, minute_y, width=5, fill='Black', tags="pointer")
    canvas.create_line(center_x, center_y, second_x, second_y, width=2, fill='Black', tags="pointer")
    master.after(1000, update_clock_pointer)

#Speak time
def speak_time(language):
    """
    use self-made wav file to speak the time
    """
    
    if language == "German":
        play_sound_german()
    elif language == "Chinese":
        play_sound_mandarin()
    elif language == "English":  # english as initialized language
        play_sound_english()


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
        
        master.after(1000, update_clocks)

    # update the clock as long as the button being clicked
    update_clocks()

    # start a thread to update the time
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
        global alarm_time, alarm_tone
        # use globle var to store alarm setting values
        alarm_hour_val = alarm_hour.get()
        alarm_minute_val = alarm_minute.get()
        am_pm = alarm_period.get()
        alarm_tone = alarm_tone_var.get()

        if am_pm == "PM" and alarm_hour_val != "12":
            alarm_hour_val = str(int(alarm_hour_val) + 12)
        elif am_pm == "AM" and alarm_hour_val == "12":
            alarm_hour_val = "00"

        alarm_time = f"{alarm_hour_val}:{alarm_minute_val}:00"  # in the 24-hours format
        print("alarm time:",alarm_time)
        
        # set the alarm:
        try:
            datetime.strptime(alarm_time, "%H:%M:%S")
            # Create a thread to run the alarm function
            alarm_thread = threading.Thread(target=lambda: run_alarm(alarm_time)) # add further args if needed
            # doing the same without a lambda function:
            # alarm_thread = threading.Thread(target=run_alarm, args=(alarm_time,)) 
           
            alarm_thread.start()
        except ValueError:
            print("Invalid time format. Please use HH:MM:SS format.")
        
        alarm_settings.destroy()  # close the setting windows
        

    # Function to run the alarm in a separate thread
    def run_alarm(alarm_time):
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            if current_time == alarm_time:
                print("Time to wake up!")
                #choose which mp3 or synthesised text to play:
                playsound(alarm_tone)
                break
            time.sleep(1)

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



def start_alarm_thread():
    """for snooze time function"""
    alarm_thread = threading.Thread(target=set_alarm)
    alarm_thread.start()

def countdown_timer(snooze_seconds):
    """
    run a count down，and play the ring sound after it
    :param snooze_seconds: int ()  in second
    """
    while snooze_seconds:
        # update the remaining time
        print(f"Time remaining: {snooze_seconds} seconds") 
        time.sleep(1)  # wait for one second
        snooze_seconds -= 1

    # now play the sound
    ## I think it is where it doesn't work
    print("Time's up! Playing alarm sound...")
    playsound(alarm_tone)  

    # show a message box to tell the user that the snooze time already finished,
    # but it doesn't work
    messagebox.showinfo("Alarm Notification", "Time's up! Wake up!")

def on_snooze_button_clicked():
    global snooze_duration  # make sure we can access global para: snooze_duration

    # to check if the snooze time already set
    if snooze_duration and int(snooze_duration) > 0:
        snooze_seconds = int(snooze_duration) * 60  # change it to seconds, users input in minute
        print(f"Snooze for {snooze_duration} minutes activated.")

        # create a new tread to process the count-down，to ensure it wont obstruct main thread of GUI 线程
        countdown_thread = threading.Thread(target=countdown_timer, args=(snooze_seconds,))
        countdown_thread.daemon = False  # set it as false
        countdown_thread.start()  # start the thread
    else:
        print("Snooze duration not set or invalid. Please set a valid snooze time first.")
        
def popup_menu(event):
    # 创建一个菜单，然后为每种语言添加一个命令
    menu = Menu(master, tearoff=0)
    menu.add_command(label="English", command=lambda: speak_time("English"))
    menu.add_command(label="German", command=lambda: speak_time("German"))
    menu.add_command(label="Chinese", command=lambda: speak_time("Chinese"))

    # 在鼠标点击的位置显示菜单
    menu.post(event.x_root, event.y_root)  # 这里使用了event对象的x和y坐标

# Create an instance of Frame in the 'master' window
frame = Frame(master)
frame.pack()  # This positions the frame within the 'master' window

# Button styling
button_font = ('Helvetica', 16)
button_bg = 'black'
button_fg = 'white'

# Now, create the 'Show World Clocks' button inside the 'frame'
show_clocks_button = Button(frame, text='Show World Clocks', command=show_world_clocks, font=button_font, bg=button_bg,
                            fg=button_fg)
show_clocks_button.pack(side='left', padx=10)  # Add some padding to separate the buttons

# Create a button to speak the time, also inside the 'frame'
speak_button = Button(frame, text='Speak Time', font=button_font, bg=button_bg, fg=button_fg)
speak_button.pack(side='left', padx=10)  # Add some padding to separate the buttons

# 绑定按钮的点击事件到popup_menu函数
# 当按钮被点击时，popup_menu会接收到关于点击的信息，包括位置等
speak_button.bind("<Button-1>", popup_menu)


# Add a button in the main window to open the alarm page, also inside the 'frame'
alarm_button = Button(frame, text="Set My Alarm", command=open_alarm_settings, font=button_font, bg=button_bg,
                      fg=button_fg)
alarm_button.pack(side='left', padx=10)  # Add some padding to separate the buttons

# Move the 'Switch Style' button to be on the same line as the digital time
style_button = Button(master, text='Switch Style', command=switch_clock_style, font=('Helvetica', 24), bg='black',
                      fg='white')
style_button.pack(pady=10)  # Add some padding to separate the button from the digital time

# Update the pointer
update_clock_pointer()

master.mainloop()
