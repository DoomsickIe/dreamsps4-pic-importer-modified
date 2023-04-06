import math
import wave
import struct
import dearpygui.dearpygui as dpg

from os import getcwd, path
from tkinter import filedialog
from pydub import AudioSegment
from pydub.utils import make_chunks
from PIL import Image

audio = []
sample_rate = 0
chunk_length_ms = 0

realTime = 0
fakeTime = 0
playbackSpeed = 1

blackAndWhite = 0
img_path = getcwd() + "\\delete_this.jpg"
new_width = 50

def get_path() -> None:
    global img_path
    img_path = filedialog.askopenfilename(initialdir="C:\\", filetypes=[("Static Image Files", ".jpg .jpeg .png .jfif .bmp")])
    generate_preview()

def update_config() -> None:
    global sample_rate, chunk_length_ms, blackAndWhite, new_width
    if(dpg.get_value("bw") == "Black and white"):
        blackAndWhite = 1
    else:
        blackAndWhite = 0
    sample_rate = dpg.get_value("smpr")
    chunk_length_ms = dpg.get_value("chnkl")

    generate_preview()
    
def generate_preview() -> None: 
    if(path.isfile(img_path)):
        dpg.enable_item("exp")
    dpg.set_value("prt", "output preview (generating)")
    npath = img_path
    img = Image.open(npath)
    if blackAndWhite == 1:
        img = img.convert('L') #Turn Pic Grey

    res = dpg.get_value("resolution")
    width, height = img.size
    aspect_ratio = height/width
    new_height = int(aspect_ratio * int(res))
    img_small = img.resize((int(res), new_height))
    
    result = img_small.resize(img.size,Image.NEAREST)
    result.save('last_pre.png')

    w, h, c, d = dpg.load_image("last_pre.png")
    with dpg.texture_registry(show=False):
        if(dpg.does_alias_exist("preview_img_tex")):
            dpg.remove_alias("preview_img_tex")
        dpg.add_static_texture(width=w, height=h, default_value=d, tag="preview_img_tex")
    dpg.delete_item("preview_img")
    dpg.add_image("preview_img_tex", parent="preview", width=400, height=400, tag="preview_img")
    dpg.set_value("image_path", npath)
    
    dpg.set_value("prt", "output preview")

def GUI_Init() -> None:
    dpg.create_context()
    dpg.create_viewport(title='Dreams Image Importer', width=1200, height=700)

    with dpg.font_registry():
        default_font = dpg.add_font("./assets/SourceSansPro-Regular.ttf", 20)

    with dpg.window(tag="main"):
        with dpg.group(horizontal=True):
            with dpg.child_window(tag="config", border=True, width=450): 
                dpg.add_text("image settings")
                dpg.add_button(label="set image path", callback=get_path)
                dpg.add_input_text(readonly=True, tag="image_path", label="path", default_value="%s" % getcwd() + "\\delete_this.jpg")
                dpg.add_combo(label="fleck resolution", tag="resolution", items=[50, 150, 300, 450, 900], default_value=150, callback=generate_preview)
                dpg.add_combo(["Colored", "Black and white"], tag="bw", label="color", default_value="Colored", callback=update_config)
                
                dpg.add_text("output audio settings")
                dpg.add_input_int(label="sample rate", default_value=8000, min_clamped=True, max_clamped=True, min_value=4000, max_value=12000, tag="smpr", callback=update_config)
                dpg.add_input_int(label="chunk length (ms)", default_value=30000, min_clamped=True, max_clamped=True, min_value=5000, max_value=60000, tag="chnkl", callback=update_config)
                dpg.add_button(label="export", tag="exp", enabled=False, callback=exportAudio)
                dpg.add_text("idle", tag="status")
            with dpg.child_window(tag="preview", border=True):
                dpg.add_text("output preview", tag="prt")
    dpg.set_frame_callback(20, generate_preview)
    dpg.bind_font(default_font)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

def picSetup():
    global img_path
    global blackAndWhite
    global new_width
    global sample_rate
    global chunk_length_ms
    
    img = Image.open(img_path)
    if blackAndWhite == 1:
        img = img.convert('L') 

    width, height = img.size
    aspect_ratio = height/width
    new_height = int(aspect_ratio * new_width)
    img_small = img.resize((new_width, new_height))
    
    picValues = [new_width, new_height, aspect_ratio, img_small, blackAndWhite]
    return picValues


def append_silence(duration_milliseconds=500):
    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)): 
        audio.append(0.0)
        
    global realTime
    global fakeTime

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

    global audio 
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
    if picValues[4] == 0: 
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
            chunks = make_chunks(myaudio, chunk_length_ms) 

            
            for i, chunk in enumerate(chunks):
                chunk_name = f"Chunks {colour}\\{colour}chunk_{i+1}.wav"
                print(f"exporting chunk {i+1}")
                chunk.export(chunk_name, format="wav")

    else: 
        fileName = 'output.wav'
        myaudio = AudioSegment.from_file(fileName , "wav") 
        chunks = make_chunks(myaudio, chunk_length_ms) 
        

        for i, chunk in enumerate(chunks): 
            chunk_name = f"Chunks (B&W)\\(B&W)chunk_{i+1}.wav"
            print(f"exporting chunk {i+1}")
            chunk.export(chunk_name, format="wav")

def save_wav(file_name):
    wav_file=wave.open(file_name,"w")

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

picValues = picSetup() 

pixels = list(picValues[3].getdata()) 

if picValues[4] == 1: #if B&W:
    for i in range(len(pixels)):
        pixelsOne.append(pixels[i]/255)
else:
    for i in range(len(pixels)):
        pixelsOne.append(pixels[i][0]/255)
        pixelsTwo.append(pixels[i][1]/255)
        pixelsThree.append(pixels[i][2]/255)

filename = 'output.wav'
duration = 33.33333333333333/playbackSpeed 

def exportAudio():
    update_config()
    if picValues[4] == 1: #if B&W
        dpg.set_value("status", "black and white: generating audio")
        append_silence(duration_milliseconds=duration/2)
        for i in range(len(pixels)):
            append_sinewave(volume = pixelsOne[i], duration_milliseconds = duration)
        save_wav("output.wav")
        dpg.set_value("status", "finished generating audio")
    else: #if colour
        for iTwo in range(3):
            dpg.set_value("status", "color: preparing audio")
            append_silence(duration_milliseconds=duration/2)
            for i in range(len(pixels)):
                if iTwo == 0:
                    dpg.set_value("status", "color: generating red audio")
                    append_sinewave(volume =float(pixelsOne[i]), duration_milliseconds = duration)  
                elif iTwo == 1:
                    dpg.set_value("status", "color: generating blue audio")
                    append_sinewave(volume = float(pixelsTwo[i]), duration_milliseconds = duration)
                elif iTwo == 2:
                    dpg.set_value("status", "color: generating green audio")
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
                dpg.set_value("status", "finished generating audio")
                
    splitAudio()
    
if __name__ == "__main__":
    GUI_Init()