#german_helpers
from pydub import AudioSegment, silence
import time

# Gets current time and indication of day (am/pm)
def get_current_time():
    current_time = time.strftime("%I:%M %p")
    replace_time = current_time.replace(":", " ")
    split_time = replace_time.split(" ")
    return int(split_time[0]), int(split_time[1]), str(split_time[2])

# Takes variable of audio file for German, determines length, and returns audio clip based on time-turned-index
def slice_silence_german(audio_file):
    hour, minute, indication = get_current_time()
    audio = AudioSegment.from_wav(audio_file)
    split_audio = silence.split_on_silence(audio, silence_thresh=-45, keep_silence=400)
    if len(split_audio) == 12:
        part = split_audio[hour - 1]
        part.export("sound_1.wav", format="wav")
        return "sound_1.wav"
    elif len(split_audio) > 12:
        if minute == 0:
            pass
        else:
            part = split_audio[minute - 1]
            part.export("sound_2.wav", format="wav")
            return "sound_2.wav"
    elif len(split_audio) == 2:
        if indication == "AM":
            part = split_audio[0]
            part.export("sound_3.wav", format="wav")
            return "sound_3.wav"
        elif indication == "PM":
            part = split_audio[1]
            part.export("sound_3.wav", format="wav")
            return "sound_3.wav"

# Takes 3 audio files, and constructs them based on German conventions
def combine_audio_english(audio_1, audio_2, audio_3):
    sound1 = AudioSegment.from_file(audio_1, format="wav")
    sound2 = AudioSegment.from_file(audio_2, format="wav")
    sound3 = AudioSegment.from_file(audio_3, format="wav")
    combined = sound1 + sound2 + sound3
    combined.export("final_sound.wav", format="wav")
    return "final_sound.wav"

#german_play_sound 
from pygame import mixer
mixer.init()

# Takes audio files and returns concatenated sound file to be played. Button takes 9 seconds to play sound after pushed.
# Button will continuously update time. Can be edited to fit other languages
def play_sound_german():
    hours = slice_silence_german("hours_German.wav")
    minutes = slice_silence_german("minutes_German.wav")
    indication = slice_silence_german("am_pm_German.wav")
    sound = mixer.Sound(combine_audio_german(hours, minutes, indication))
    sound.play()
    
