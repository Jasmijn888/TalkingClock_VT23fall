from pydub import AudioSegment
from pydub.silence import split_on_silence
#name
input_audio_file = "ampm.wav"

#read
audio = AudioSegment.from_file(input_audio_file)

# threshhold
min_silence_len = 140 # minimal silence time
silence_threshold = -50 # threshhold volume
audio_chunks = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_threshold)

# save
for i, chunk in enumerate(audio_chunks):
# output
    output_file = f"output_chunk_{i + 1}.mp3"

# save
    chunk.export(output_file, format="mp3")
    print(f"保存 {output_file}")

    print("finished")