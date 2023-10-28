import librosa
import numpy as np

# 加载音频文件
audio_file = '1h.mp3'
y, sr = librosa.load(audio_file)

# 计算音频的分贝级别
db = librosa.amplitude_to_db(librosa.feature.rms(y=y), ref=np.max)
print(f"Max dB level: {db.max()}")
