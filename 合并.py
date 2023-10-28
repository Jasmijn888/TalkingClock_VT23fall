from pydub import AudioSegment

# choose
audio_file1 = "output_chunk_50.mp3"
audio_file2 = "output_chunk_51.mp3"
#audio_file3 = "output_chunk_11.mp3"
#audio_file4 = "path_to_audio_file4.mp3"
#audio_file5 = "path_to_audio_file5.mp3"

# pydub-audio
audio1 = AudioSegment.from_file(audio_file1)
audio2 = AudioSegment.from_file(audio_file2)
#audio3 = AudioSegment.from_file(audio_file3)
#audio4 = AudioSegment.from_file(audio_file4)
#audio5 = AudioSegment.from_file(audio_file5)

# combine together
combined_audio = audio1 + audio2

# save
combined_audio.export("combined_audio.mp3", format="mp3")
