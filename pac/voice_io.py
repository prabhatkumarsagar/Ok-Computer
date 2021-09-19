import os
import socket
import gtts
from playsound import playsound
import pyttsx3
import speech_recognition as sr

try:
    from pac import get_dirs
    
except ModuleNotFoundError:
    import get_dirs

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        pass
    return False

engine=pyttsx3.init()
voices=engine.getProperty('voices')
if os.name == "nt":
    engine.setProperty('voice',voices[0].id)
else:
    engine.setProperty('voice',voices[10].id)
engine.setProperty('rate',125) #Default Rate = 150

def voice_out(qry): 
    if is_connected():
        try:
            voice_ob = gtts.gTTS(qry)
            voice_ob.save(get_dirs.PATH_USR_DATA + "voice_output.mp3")
            playsound(get_dirs.PATH_USR_DATA + "voice_output.mp3")
            os.remove(get_dirs.PATH_USR_DATA + "voice_output.mp3")
        except:
            engine.say(qry) 
            engine.runAndWait()

    else:
        engine.say(qry) 
        engine.runAndWait()

def chng_voice_rate(newrate):
    engine.setProperty('rate',newrate)

def chng_voice_lang(x):
    engine.setProperty('voice',voices[x].id)

def voice_in():
    r = sr.Recognizer() 
    with sr.Microphone() as source:  
        audio = r.listen(source) 
    try:    
        query = r.recognize_google(audio, language ='en-in') 
        print(query)
        return query
    except: 
        print(False)  
        return False   

def show(*args, end = "\n", sep = " ", show_output = True):
    from pac.assistant_settings import loadSound
    sound = loadSound()
    st = ""
    for i in args:
        st = st + str(i) + sep
    st = st.rstrip()
    if sound:
        if show_output:
            print(st, end = end)
        voice_out(st)
    else:
        if show_output:
            print(st, end = end)
    if not show_output:
        return st