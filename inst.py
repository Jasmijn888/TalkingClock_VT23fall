from tkinter import *
from PIL import Image, ImageTk, ImageFilter
import time
from datetime import datetime
from math import sin, cos, radians
from pyttsx3 import init
import pytz
import threading
from tkinter import ttk  # This imports the ttk module
#from english_helpers import get_current_time, slice_silence_english, combine_audio_english
#from german_helpers import play_sound_german
#from play_sound import play_sound_english
#from mandarin_helpers import play_sound_mandarin
#from playsound import playsound
import tkinter as tk

master = Tk()
master.title("Pikachu Clock")

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




# 全局变量
selected_timezone = "Asia/Shanghai"

# 函数：选择时区
def select_timezone(value):
    global selected_timezone
    selected_timezone = value
    update_time()

# 函数：播放当前时间
def read_time():
    current_time = get_current_time()
    play_audio(f"{current_time}_{selected_timezone}.wav")

# 函数：设置闹钟
def set_alarm():
    alarm_time = simpledialog.askstring("Set Alarm", "Enter the alarm time (HH:MM):")
    if alarm_time is not None:
        try:
            datetime.strptime(alarm_time, "%H:%M")
            messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter a valid time (HH:MM)")

# 函数：获取当前时间
def get_current_time():
    now = datetime.now(pytz.timezone(selected_timezone))
    current_time = now.strftime("%H:%M:%S")
    return current_time

##########################

# 函数：播放音频
def play_audio(audio_file):
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
#########################################################

# Create an instance of Frame in the 'master' window
frame = Frame(master)
frame.pack()  # This positions the frame within the 'master' window







# 创建下拉框来选择时区
timezones = {"China (Shanghai)": "Asia/Shanghai", "Germany (Berlin)": "Europe/Berlin", "USA (New York)": "America/New_York"}
timezone_var = tk.StringVar()
timezone_var.set(selected_timezone)
timezone_menu = tk.OptionMenu(frame, timezone_var, *timezones, command=lambda value: select_timezone(timezones[value]))
timezone_menu.grid(row=1, column=0)

# 创建按钮来读取当前时间
read_time_button = tk.Button(frame, text="Read the Time", command=read_time)
read_time_button.grid(row=1, column=1)

# 创建按钮来设置闹钟
set_alarm_button = tk.Button(frame, text="Set Alarm", command=set_alarm)
set_alarm_button.grid(row=1, column=2)

style_button = tk.Button(frame, text='Switch Style', command=switch_clock_style)
style_button.grid(row=0, column=0, columnspan=3)

# 创建标签来显示当前时间
#time_label = tk.Label(frame, text=get_current_time(), font=("Helvetica", 24))
#time_label.grid(row=2, column=0, columnspan=3)

# 启动定时器来更新时间
def update_time():
    current_time = get_current_time()
    time_label.config(text=current_time)
    master.after(1000, update_time)

def update_clock_pointer():
    now = datetime.now(pytz.timezone(selected_timezone))
    current_time = now.time()

    # 与之前代码保持一致，计算角度
    hours = current_time.hour
    minutes = current_time.minute
    seconds = current_time.second

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


update_time()
update_clock_pointer()

# 运行主程序
master.mainloop()

