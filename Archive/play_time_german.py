import os
import time
import pygame

pygame.mixer.init()

def play_current_time_audio():
    # 获取当前时间
    current_time = time.localtime()
    hour = current_time.tm_hour
    minute = current_time.tm_min

    # 转换12小时制
    period = "am" if hour < 12 else "pm"
    hour_12 = hour if 0 < hour <= 12 else abs(hour - 12)

    # 构建文件名
    hour_file = f"output_hour_{hour_12}.mp3"
    min_file = f"output_min_{minute}.mp3" if minute != 0 else ""
    period_file = f"output_{period}.mp3"  # 根据您提供的文件名，这里假设am和pm的文件名分别是output_am_1.mp3和output_pm_2.mp3
    # print(period_file)
    # 设置音频文件所在的文件夹路径
    
    folder_path = "German_slicing"

    # 播放“小时”音频
    hour_path = os.path.join(folder_path, hour_file)
    pygame.mixer.music.load(hour_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():  # 确保音乐播放完毕
        time.sleep(1)

    # 如果“分钟”不是0，播放“分钟”音频
    if min_file:
        min_path = os.path.join(folder_path, min_file)
        pygame.mixer.music.load(min_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():  # 确保音乐播放完毕
            time.sleep(1)

    # 播放“上午/下午”音频
    pm_path = os.path.join(folder_path, period_file)
    pygame.mixer.music.load(pm_path)
    pygame.mixer.music.play()
    # print(f"Playing file: {pm_path}")

    while pygame.mixer.music.get_busy():  # 确保音乐播放完毕
        time.sleep(1)
        
# 调用函数
play_current_time_audio()