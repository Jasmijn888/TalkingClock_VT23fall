from english_helpers import slice_silence_english, combine_audio_english
from pygame import mixer
mixer.init()


# Takes audio files and returns concatenated sound file to be played. Button takes 9 seconds to play sound after pushed.
# Button will continuously update time. Can be edited to fit other languages
def play_sound_english():
    hours = slice_silence_english("English Audio/hour_English.wav")
    minutes = slice_silence_english("English Audio/minutes_English.wav")
    indication = slice_silence_english("English Audio/am_pm_English.wav")
    sound = mixer.Sound(combine_audio_english(hours, minutes, indication))
    sound.play()
