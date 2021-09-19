#from pac.get_dirs import FILE_USR_DATA
from pac.get_dirs import FILE_USR_DATA
import os
from pac import get_dirs
from pac import clear
#import get_dirs
#import clear
try:
    from pac import assistant_settings
except:
    pass

def inpt(text = ">>> ", audio_io = True, iterate = True, processed = True):
    if audio_io:
        from pac import voice_io
        #import voice_io
        
        while True:
            try:
                entered_data = input(text)
                # voice_io.show("input = ",entered_data)
                
                if processData(entered_data) == "voice":
                    i = 0
                    voice_data = False
                    while not voice_data:
                        try:
                            voice_io.show("I am listening......")
                            voice_data = entered_data = voice_io.voice_in()
                            i += 1
                            if i >= 1:
                                voice_io.show("\nSorry, could not get that! Please try again..\n")
                    
                        except KeyboardInterrupt:#stops voice input when ctrl+c is pressed 
                            voice_io.show("\nStopped listening")
                            entered_data = ""
                            voice_data = True

                elif entered_data == "":
                    if not iterate:
                        return ""                         
                    continue

                elif processData(entered_data).lower() == "disable sound":
                    assistant_settings.disableSound()
                    if not iterate:
                        return ""
                    
                    voice_io.show("Sound has been disabled! You can continue with your operation")
                    continue

                elif processData(entered_data).lower() == "enable sound":
                    assistant_settings.enableSound()
                    if not iterate:
                        return ""

                    voice_io.show("Sound has been enabled! You can continue with your operation")
                    continue

                elif "clear" in processData(entered_data).lower() or processData(entered_data).lower() in "clrcls":
                    return "clear"

                elif processData(entered_data).lower() in ["exit", "quit", "end", "bye", "good bye", "goodbye", "tata"]:
                    #voice_io.show(entered_data.lower() in "exitquitend")
                    voice_io.show("\nBye and have a nice day!")
                    exit()

                else:
                    if processed:
                        entered_data = processData(entered_data)

                    return entered_data

            except KeyboardInterrupt:#exits from the program when ctrl+c is pressed
                voice_io.show("\nBye and have a nice day!")
                exit()
            
    else:
        entered_data = input(text)
        if processed:
            entered_data = processData(entered_data)

        return entered_data

def processData(data):
    lst = data.split(" ")
    data = ""
    for i in lst:
        n = ""
        if i == " " or i == "":
            continue
        
        for j in i:
            if j.isalnum() or j in "+-*/%^.":
                n += j 

        data += " " + n
    
    return data.strip()