import math
import wave
import struct
import sys, random, argparse
import numpy as np
import time

from configparser import ConfigParser
from pydub import AudioSegment
from pydub.utils import make_chunks
from PIL import Image

cfg = ConfigParser()
cfg.read("./config.ini")

audio = []
sample_rate = int(cfg.get("audio", "samplerate"))
chunk_length_ms = int(cfg.get("audio", "outchunklengthms"))

realTime = 0
fakeTime = 0
playbackSpeed = 1

def picSetup():
    fileFormat = ".jpg"
    blackAndWhite = int(cfg.get("image", "bw"))
    img_path = "dreams.jpg"
    new_width = int(cfg.get("image", "outwidth"))
    
    img_path = input('\nName of file (with extension): ')
    fileFormat = img_path.split('.')[-1]
    print('detected file format: ' + fileFormat)
    
    defaultPreset = int(input("Do you want to use your last saved config? Saying no will save this run's config to config.ini. (Type 0/1): "))
    
    if defaultPreset == 0:
        blackAndWhite = int(input('Colour or B&W (Type 0/1): '))

        new_width = int(input('Width of image (Flecks): '))
        
        sample_rate = int(input('Output audio sample rate (hz): '))
        chunk_length_ms = int(input('Output audio chunk length (ms): '))
        
        cfg.set("audio", "samplerate", str(sample_rate))
        cfg.set("audio", "outchunklengthms", str(chunk_length_ms))
        cfg.set("image", "outwidth", str(new_width))
        cfg.set("image", "bw", str(blackAndWhite))
        print("config saved to file")
    else:
        print("using config: ", "\nformat: ", fileFormat, "\nblack and white: ", blackAndWhite, "\nimage width: ", new_width)
    
    img_path = 'Pictures\\'+ img_path
    img = Image.open(img_path)
    if blackAndWhite == 1:
        img = img.convert('L') #Turn Pic Grey

    width, height = img.size
    aspect_ratio = height/width
    new_height = int(aspect_ratio * new_width)
    img_small = img.resize((new_width, new_height))
    # new size of image
    print('\nSize:', img_small.size, '(Width, Height)')
    print('Pixels:', new_width * new_height, '\n')
    
    '''
    if (new_width * new_height > 10650 and blackAndWhite == 1) or (new_width * new_height * 3 > 10650 and blackAndWhite == 0):
        print(f'\n{"*"*30}\n\tWarning!\nThe picture you are trying to print is too big to import to dreams!\nIts highly reccomended to choose a lower resolution.\n{"*"*30}')
    '''
    
    # Scale back up using NEAREST to original size
    result = img_small.resize(img.size,Image.NEAREST)

    # Save
    result.save('result.png')
    
    #Returns essential variables
    picValues = [new_width, new_height, aspect_ratio, img_small, blackAndWhite]
    return picValues


def append_silence(duration_milliseconds=500):
    """
    Adding silence is easy - we add zeros to the end of our array
    """
    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)): 
        audio.append(0.0)
        
    global realTime
    global fakeTime
    #First half pause
    realTime = duration/2
    fakeTime = len(audio) * (sample_rate)
    
    while ((1/sample_rate)+fakeTime) <= realTime:
        audio.append(0)
        print('hi')
        fakeTime = len(audio) * (1/sample_rate)
    return


def append_sinewave(
        freq=440.0 * playbackSpeed, 
        duration_milliseconds=500, 
        volume=1.0):

    global audio # using global variables isn't cool.
    global realTime
    global fakeTime
    
    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        audio.append(volume * math.sin(2 * math.pi * freq * ( x / sample_rate )))
    
    realTime += duration
    fakeTime = (len(audio) * (1/sample_rate))*1000
    
    while ((1/sample_rate)+fakeTime) <= realTime:
        audio.append(0)
        fakeTime = (len(audio) * (1/sample_rate))*1000
    
    return

def splitAudio():
    #Export all of the individual chunks as wav files
    if picValues[4] == 0: #Colour
        for iTwo in range(3):
            print('')
            if iTwo == 0:
                colour = '(RED)'
            if iTwo == 1:
                colour = '(GREEN)'
            elif iTwo == 2:
                colour = '(BLUE)'
            
            fileName = f'output{colour}.wav'
            myaudio = AudioSegment.from_file(fileName , "wav") 
            chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of 30* secs

            
            for i, chunk in enumerate(chunks):
                chunk_name = f"Chunks {colour}\\{colour}chunk_{i+1}.wav"
                print(f"exporting chunk {i+1}")
                chunk.export(chunk_name, format="wav")

    else: #B&W
        fileName = 'output.wav'
        myaudio = AudioSegment.from_file(fileName , "wav") 
        chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of 30* secs
        

        for i, chunk in enumerate(chunks): 
            chunk_name = f"Chunks (B&W)\\(B&W)chunk_{i+1}.wav"
            print(f"exporting chunk {i+1}")
            chunk.export(chunk_name, format="wav")

def save_wav(file_name):
    # Open up a wav file
    wav_file=wave.open(file_name,"w")

    # wav params
    nchannels = 1
    sampwidth = 2

    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

    wav_file.close()
    return


################# END DEFINITIONS ######################

pixelsOne = []
pixelsTwo = []
pixelsThree = []

picValues = picSetup() #picValues is just a list of pic info


pixels = list(picValues[3].getdata()) #pixel data

if picValues[4] == 1: #if B&W:
    for i in range(len(pixels)):
        pixelsOne.append(pixels[i]/255)
        #B&W pixel shades from 0-1
else:
    for i in range(len(pixels)):
        pixelsOne.append(pixels[i][0]/255)
        pixelsTwo.append(pixels[i][1]/255)
        pixelsThree.append(pixels[i][2]/255)
        #RGB pixel shades from 0-1 
        

filename = 'output.wav'
duration = 33.33333333333333/playbackSpeed #More accurate float than 1000/30

if picValues[4] == 1: #if B&W
    append_silence(duration_milliseconds=duration/2)
    for i in range(len(pixels)):
        append_sinewave(volume = pixelsOne[i], duration_milliseconds = duration)
    save_wav("output.wav")
    
else: #if colour
    for iTwo in range(3):
        append_silence(duration_milliseconds=duration/2)
        for i in range(len(pixels)):
            if iTwo == 0:
                append_sinewave(volume =float(pixelsOne[i]), duration_milliseconds = duration)  
            elif iTwo == 1:
                append_sinewave(volume = float(pixelsTwo[i]), duration_milliseconds = duration)
            elif iTwo == 2:
                append_sinewave(volume = float(pixelsThree[i]), duration_milliseconds = duration)
                
        if iTwo == 0:
            filename = "output(RED).wav"
        elif iTwo == 1:
            filename = "output(GREEN).wav"
        elif iTwo == 2:
            filename = "output(BLUE).wav"

        if iTwo == 0:
            save_wav("output(RED).wav")
            audio.clear()

        elif iTwo == 1:
            save_wav("output(GREEN).wav")
            audio.clear()

        elif iTwo == 2:
            save_wav("output(BLUE).wav")
            audio.clear()
            
splitAudio()