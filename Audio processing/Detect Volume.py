import librosa
import numpy as np


audio_file = '1h.mp3'
y, sr = librosa.load(audio_file)

# db
db = librosa.amplitude_to_db(librosa.feature.rms(y=y), ref=np.max)
print(f"Max dB level: {db.max()}")
