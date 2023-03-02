#! python3

import os
import sys
from argparse import ArgumentParser

from pydub import AudioSegment
from pydub.silence import split_on_silence

import whisper

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="mySourceAudio", help="Open specified file")
parser.add_argument("-o", "--output", dest="myOutputFolder", help="Specify destination directory")
args = parser.parse_args()
mySourceAudio = args.mySourceAudio
myOutputFolder = args.myOutputFolder

##Functions section

def source_splitting(mySourceAudio, myOutputFolder, chunks_list):
    os.mkdir(myOutputFolder)
    print("Processing file")
    split_source = AudioSegment.from_file(mySourceAudio)
    dBFS = split_source.dBFS
    splits = split_on_silence(split_source, min_silence_len=750, silence_thresh = dBFS-18)

    for i, split in enumerate(splits):
    # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        #print("Creating silence chunk")
        silence_chunk = AudioSegment.silent(duration=500)
        #print("Recombining chunk")
        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = silence_chunk + split + silence_chunk
        ##print("Exporting chunk{0}.wav".format(i))
        number = '0'+str(i)
        #print("Exporting chunk{00}.wav".format(number))
        # Export the audio chunk with new bitrate.
        audio_chunk.export(
            os.path.join(myOutputFolder, "chunk{00}.wav".format(number)),
            bitrate = "192k",
            format = "wav"
        )
        chunks_list.append("chunk{00}.wav".format(number))

def iterate_transcript(chunk_path):
    transcript = model.transcribe(chunk_path)
    ##print(transcript["text"])
    return (transcript["text"])

##Main loop starts here
chunks_list=[]
transcript=[]
print("Splitting sound file into chunks")
source_splitting(mySourceAudio, myOutputFolder, chunks_list)
print("Saving audio chunks list")

model = whisper.load_model("base")

print("Starting transcription loop")
print("Opening audio chunks list")
for chunk in chunks_list:
    chunk_path = os.path.join(myOutputFolder, chunk)
    transcript.append(iterate_transcript(chunk_path))

print("Here's a preview of your transcription!") 
for item in transcript:
    print(item)

print("Saving your transcription to disk!")
transcript_filename = input("What would you like to call your transcript?")
transcript_file = os.path.join(myOutputFolder, transcript_filename)

f = open(transcript_file, "a")
for item in transcript:
    f.write(str(item))
    f.write("\n\n")
f.close()

print("Your transcription is ready. Enjoy!")
