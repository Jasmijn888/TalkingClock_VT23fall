import librosa

# 加载音频文件
audio_file = '1h.mp3'
y, sr = librosa.load(audio_file)

# 提取速度信息
tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
print(f"Tempo: {tempo} BPM")