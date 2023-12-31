import os
from pydub import AudioSegment
import numpy as np

# place
audio_folder = 'gg'

# upload
standard_audio = AudioSegment.from_file("1h.mp3")

# measure db
standard_db = np.mean(standard_audio.dBFS)

# get
for filename in os.listdir(audio_folder):
    if filename.endswith(".mp3"):
        audio_file = os.path.join(audio_folder, filename)

        audio = AudioSegment.from_file(audio_file)

        audio_db = np.mean(audio.dBFS)

        db_gain = standard_db - audio_db

        audio = audio + db_gain

        audio.export(audio_file, format="mp3")