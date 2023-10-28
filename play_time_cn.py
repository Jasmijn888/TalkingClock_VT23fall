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
    hour_file = f"CN_{hour_12}h.mp3"
    min_file = f"CN_{minute}m.mp3"
    period_file = f"CN_{period}.mp3"

    # 设置音频文件所在的文件夹路径
    folder_path = "CN_slicing"

	# 播放“上午/下午”音频
    pm_path = os.path.join(folder_path, period_file)
    pygame.mixer.music.load(pm_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():  # 确保音乐播放完毕
        time.sleep(1)


    # 播放“小时”音频
    hour_path = os.path.join(folder_path, hour_file)
    pygame.mixer.music.load(hour_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():  # 确保音乐播放完毕
        time.sleep(1)


    # 播放“分钟”音频
    min_path = os.path.join(folder_path, min_file)
    pygame.mixer.music.load(min_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # 确保音乐播放完毕
        time.sleep(1)

# 调用函数
play_current_time_audio()      