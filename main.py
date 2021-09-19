import os
import datetime
from urllib.parse import non_hierarchical
import webbrowser
import random
import getpass
import re
import base64
from pac import encryption, install_packages as ip, notes_reminders_op
from pac import get_dirs
from pac import clear

if not os.path.exists(get_dirs.PATH_USR_DATA):
    clear.clear()
    print("\nInstalling required packages.....\n")
    if ip.install():
        input("\nAll packages have been successfully installed! Press Enter/Return to continue.")
        print()
    else:
        print("\nInstalling packages failed! Make sure you have a stable internet connection and all the requirements to install packages are fulfilled. Please try running this program again after resolving all issues, and if the problem still persists, contact the developer.")
        exit()

    os.mkdir(get_dirs.PATH_USR_DATA)

try:
    import requests 
    from pac import (
        usr_signup,
        voice_io,
        invoice,
        file_op,
        mail_op,
        news_op,
        web_op,
        assistant_settings,
        weather_weatherforec_op,
        notes_reminders_op,
        song_op,
        date_time_op,
        )
    
    
except ModuleNotFoundError:    
    clear.clear()
    print("\nInstalling required packages.....\n")
    if ip.install():
        input("\nAll packages have been successfully installed! Press Enter/Return to continue.")
        print()

    else:
        print("\nInstalling packages failed! Make sure you have a stable internet connection and all the requirements to install packages are fulfilled. Please try running this program again after resolving all issues, and if the problem still persists, contact the developer.")
        exit()

    import requests 
    from pac import (
            usr_signup,
            voice_io,
            invoice,
            file_op,
            mail_op,
            news_op,
            web_op,
            assistant_settings,
            weather_weatherforec_op,
            notes_reminders_op,
            song_op,
            date_time_op
            )

except OSError:
    print("\nPackage 'libespeak1'(debian based systems) or 'espeak'(fedora based systems), which is required by this program, is missing from your system!\nPlease install it from your distro repos and run this program again!")
    exit()

import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

file_user_data = get_dirs.FILE_USR_DATA
home = get_dirs.HOME
desktop = get_dirs.DESKTOP
downloads = get_dirs.DOWNLOADS
documents = get_dirs.DOCUMENTS
music = get_dirs.MUSIC
videos = get_dirs.VIDEOS
pictures = get_dirs.PICTURES


locate_desktop = ["1", "desktop"]
locate_downloads = ["2", "downloads"]
locate_documents = ["3", "documents"]
locate_music = ["4", "music"]
locate_pictures = ["5", "pictures"]
locate_videos = ["6", "videos"]
locate_home = ["7", "home"]

#sound = False
usr_name = ""

def operation(query):
    op={
        # chat operations
        "help": ["help","help me","hey help me"],
        "greet_hello": ["what's up","what's good","hi","yo","wassup","hello","hey","hullo"],
        "greet_time": ["good morning","good afternoon","good evening"],
        "joke": ["tell me a joke", "tell a joke", "joke", "a joke", "jokes", "make me laugh", "another", "another one", "once more"], 
        "abt_assistant": ["who are you","what's your name","what is your name","tell me about yourself"], 
        "abt_creators": ["who made you", "hey who's your fada", "who's you creator","who created you"], 
        "ask_wellbeing": ["hey how are you","how do you do","how are you","howdy"],
        # file operations
        "search_file": ["searchfile","search file","search","search folder"],
        "open_file": ["open ", "open a file", "open a folder", "open file", "open folder"],
        "delete_general": ["delete", "del", "remove", "erase", "rm"], 
        "delete_file_unspecified": ["delete a file", "file delete", "remove a file"], 
        "delete_folder_unspecified": ["delete a folder", "folder delete", "remove a folder", "remove directory", "rmdir"], 
        "rename_unspecified": ["rename a folder", "rename a file", "rename folder", "rename file", "folder rename", "file rename", "rename directory", "directory rename", "rname"], 
        "copy": ["copy", "cp", "clone", "replicate", "copy a file", "copy a folder"],
        "move": ["move", "mv", "move a file", "move a folder"],
        "rename": ["rname", "rename", "rename a file", "rename a folder", "rename a folder"], 
        "music_from_a_file": ["play an audio file", "play an audio", "play a audio", "play a audio file", "play music from a file", "play audio from a file","play music file", "play audio file", "play music from file", "play audio from file"], 
        # misc operations
        "web_search": ["opensite","openwebsite","where is","google","youtube","define","what's the meaning of","search ","meaning of","what is"], 
        "time":["time","current time","what's the time","tell me the time","what time it is"], 
        "date": ["date","today's date","what's the date","current date"], 
        "date_day": ["what's the day","day","what day is it","what day it is"], 
        "date_month": ["what's the month","month","what month is it","what month it is"], 
        "date_year": ["year","what's the year","what year is it","what year it is"], 
        "notes_write": ["write a note","save a note","add a note","add a reminder","note",],
        "reminder_write": ["reminder", "save a reminder", "write a reminder", "remind me"],
        "notes_read": ["are there any notes","notes","do i have any note","past notes","read notes"], 
        "reminder_read": ["are there any reminders","do i have any reminders","reminders","read reminders","past reminders"],
        "email": ["email","send a email","send an email","write an email","compose email","compose an email"], 
        "weather": ["weather","weather today","what's the weather","current weather","what's the temperature outside","how's the josh","temperature"], 
        "weather_frcst": ["weather forecast","weather tomorrow", "what's the weather forecast","how's the weather going to be"], 
        "song": ["play","song"], 
        "news": ["news","headlines","top headlines","today's news"],
        "test":["test"] #for testing out a feature or module or function or whatever
    }
    n=""
    for i in op:
        for j in op[i]:
            if j in query:
                n=i
            else:
                continue
    return n

key = None

def fetch_password():
    pswd = bytes(getpass.getpass(voice_io.show("\nPlease enter your password. ",show_output = False) + "\nPassword: "), encoding = "utf-8")#use password
    global key
    key=encryption.getkey()
    global usr_name
    usr_name = False
    usr_name = usr_signup.main(operation = "fetch", data_type = "name", key = key)

def main():
    clear.clear()
    if os.path.exists(file_user_data):
        #usr_data = open(path_user_data)
        fetch_password()
        while usr_name == False:
            getpass.getpass(voice_io.show("\nInvalid password! Press enter to try again.",show_output = False))
            #voice_io.show("Invalid password! Press enter to try again.")
            #invoice.inpt(iterate = False)
            fetch_password()

    else:
        userSetup()

    iterate_jokes = 0
    clear.clear()
    gnd_ns()

    while True:
        task = invoice.inpt()
        if iterate_jokes > 0 and task not in ["another", "another one","another joke", "once more", "more", "again", "new one", "make me laugh again"]:
            iterate_jokes = 0

        elif task.lower() == "clear":
            clear.clear()

        else:
            result=operation(task.lower())
            result=result.lower()
            if result=="":
                try:
                    voice_io.show(web_op.wolfy(task))

                except:
                    voice_io.show("Sorry i couldn't help you with that. Please try a valid operation.")
                    
            elif result=="help":
                voice_io.show("Hello Hello! What is it that i can help you with today?")
                voice_io.show("1. Assistant Settings")
                voice_io.show("2. Assistant Services")
                voice_io.show("3. Assistant Operations")
                voice_io.show("4. Feedback (Suggest Improvements/Report Bugs/...)")
                x=invoice.inpt("Enter Choice: ")
                if x=="1":
                    pda_help()
                    
                elif x=="2":
                    srvc_help()
                    
                elif x=="3":
                    op_help()
                    
                elif x=="4":
                    feedback()
                    
                else:
                    voice_io.show("Invalid Input! Please Try Again!")
            
            #for testing out a feature or module or function or whatever
            elif result=="test":
                pass

            elif result=="delete_file_unspecified":
                deleteFileUnspecified()

            elif result=="delete_folder_unspecified":
                deleteFolderUnspecified()
        
            elif result=="delete_general":
                voice_io.show(f"What do you want to {task}, a file or a folder?")
                choice = invoice.inpt().lower()
                if choice == "file":
                    deleteFileUnspecified()

                elif choice == "folder":
                    deleteFolderUnspecified()

                else:
                    voice_io.show("Sorry i didn't get that, please try again with a proper command.")
                    
            elif result == "open_file":
                query = task.lower()
                kwrd = ""
                obj_name = ""
                if "open a file" in query:
                    kwrd = "file"

                elif "open a folder" in query:
                    kwrd = "folder"
                
                elif "open file" in query:
                    obj_name = task.replace("open file", "")

                elif "open folder" in query:
                    obj_name = task.replace("open folder", "")

                elif "open " in query:
                    obj_name = task.replace("open ", "")

                obj_name = obj_name.strip()
                if kwrd == "":
                    kwrd = "File or Folder"
                if obj_name == "":
                    voice_io.show(f"Which {kwrd} would you like me to open.")
                    obj_name = invoice.inpt(processed = False)

                voice_io.show(f"Where would you like me to search for {obj_name}?\n1. Desktop\n2. Downloads\n3. Documents\n4. Music\n5. Pictures\n6. Videos\n7. Entire home directory")
                locate = invoice.inpt().lower()
                if locate in locate_desktop:
                    search_dir = desktop

                elif locate in locate_documents:
                    search_dir = documents

                elif locate in locate_downloads:
                    search_dir = downloads

                elif locate in locate_home:
                    search_dir = home
                            
                elif locate in locate_music:
                    search_dir = music
                
                elif locate in locate_pictures:
                    search_dir = pictures

                elif locate in locate_videos:
                    search_dir = videos

                elif locate in locate_home:
                    search_dir = home

                else:
                    voice_io.show("Sorry but i cannot find the given directory, \ngoing forward with the entire home directory!")
                    search_dir = home
                
                file_op.file_opener(obj_name, search_dir)
                    
            elif result == "search_file":
                obj_name = task.replace("searchfile", "").strip()
                if obj_name == "":
                    voice_io.show(f"What would you like me to search for?.")
                    obj_name = invoice.inpt(processed = False)
                
                voice_io.show(f"Where would you like me to search for {obj_name}?\n1. Desktop\n2. Downloads\n3. Documents\n4. Music\n5. Pictures\n6. Videos\n7. Entire home directory")
                locate = invoice.inpt().lower()
                if locate in locate_desktop:
                    search_dir = desktop

                elif locate in locate_documents:
                    search_dir = documents

                elif locate in locate_downloads:
                    search_dir = downloads

                elif locate in locate_home:
                    search_dir = home
                            
                elif locate in locate_music:
                    search_dir = music
                
                elif locate in locate_pictures:
                    search_dir = pictures

                elif locate in locate_videos:
                    search_dir = videos

                elif locate in locate_home:
                    search_dir = home

                else:
                    voice_io.show("Sorry but i cannot find the given directory, \ngoing forward with the entire home directory!")
                    search_dir = home
                
                voice_io.show(f"Searching for '{obj_name}' in {search_dir}.....")
                folder_search_results = file_op.folderSearch(obj_name, search_dir)
                file_search_results = file_op.fileSearch(obj_name, search_dir)
                if folder_search_results != [] or file_search_results != 0:
                    count_files = len(file_search_results)
                    count_folders = len(folder_search_results)
                    voice_io.show(f"Found {count_files} files and {count_folders} folders matching the given name! They are :-")
                    sno = 1
                    for i in file_search_results:
                        voice_io.show(f"{sno}. file '{i['file']}', inside '{i['root']}'")
                        sno += 1
                    
                    for i in folder_search_results:
                        voice_io.show(f"{sno}. folder '{i['folder']}', inside '{i['root']}'")
                        sno += 1
                    
                    voice_io.show("Would you like to open any one of them?")
                    ch = invoice.inpt().lower()
                    if ch in ["yes", "yep", "yay", "duh", "sure", "y"]:
                        voice_io.show("Select the number of the file/folder which you would like to open.")
                        choice = int(invoice.inpt())
                        choice -= 1
                        try:
                            if choice in range(count_files):
                                f_name = file_search_results[choice]['file']
                                parent_dir = file_search_results[choice]['root']
                                voice_io.show(f"Opening file '{f_name}' from '{parent_dir}'.....")
                                full_dir = parent_dir + "/" + f_name
                                file_op.open_file(full_dir)
                            
                            elif choice - (count_files) in range(count_folders):
                                choice -= count_files
                                f_name = folder_search_results[choice]['folder']
                                parent_dir = folder_search_results[choice]['root']
                                voice_io.show(f"Opening folder '{f_name}' from '{parent_dir}' in the Files Explorer.....")
                                full_dir = parent_dir + "/" + f_name
                                file_op.open_file(full_dir)

                            else:
                                voice_io.show("Opening failed : Sorry, but the entered number is not within the range of available options.")
                            
                        except SyntaxError or TypeError:
                            voice_io.show("Opening failed : Sorry, but your entered data is not a number.")
                else:
                    voice_io.show(f"Sorry, could not find any file or folder relating to '{obj_name}'")

            elif result=="rename":
                search_dir = ""
                voice_io.show("Which file/folder would you like to rename?")
                obj_name = invoice.inpt(processed = False)
                voice_io.show(f"Where would you like me to search for {obj_name}?\n1. Desktop\n2. Downloads\n3. Documents\n4. Music\n5. Pictures\n6. Videos\n7. Entire home directory")
                locate = invoice.inpt().lower()
                if locate in locate_desktop:
                    search_dir = desktop

                elif locate in locate_documents:
                    search_dir = documents

                elif locate in locate_downloads:
                    search_dir = downloads

                elif locate in locate_home:
                    search_dir = home
                            
                elif locate in locate_music:
                    search_dir = music
                
                elif locate in locate_pictures:
                    search_dir = pictures

                elif locate in locate_videos:
                    search_dir = videos

                elif locate in locate_home:
                    search_dir = home

                else:
                    voice_io.show("Sorry but i cannot find the given directory, going forward with the entire home directory!")
                    search_dir = home
                
                voice_io.show(f"What should be the new name for '{obj_name}'?")
                new_name = invoice.inpt(processed = False)
                                
                file_op.rname(obj_name = obj_name,search_dir = search_dir, new_name = new_name)

            elif result=="copy":
                search_dir = ""
                voice_io.show("Which file/folder would you like to copy?")
                obj_name = invoice.inpt(processed = False)
                voice_io.show(f"Where would you like me to search for {obj_name}?\n1. Desktop\n2. Downloads\n3. Documents\n4. Music\n5. Pictures\n6. Videos\n7. Entire home directory")
                locate = invoice.inpt().lower()
                if locate in locate_desktop:
                    search_dir = desktop

                elif locate in locate_documents:
                    search_dir = documents

                elif locate in locate_downloads:
                    search_dir = downloads

                elif locate in locate_home:
                    search_dir = home
                            
                elif locate in locate_music:
                    search_dir = music
                
                elif locate in locate_pictures:
                    search_dir = pictures

                elif locate in locate_videos:
                    search_dir = videos

                elif locate in locate_home:
                    search_dir = home

                else:
                    voice_io.show("Sorry but i cannot find the given directory, going forward with the entire home directory!")
                    search_dir = home
                
                voice_io.show(f"What should be the destination for '{obj_name}'?\n(Example : 'Downloads' or 'Documents/New Folder', case sensitive and without quotes).")
                dest_dir = invoice.inpt(processed = False)
                                
                file_op.copy(obj_name = obj_name, search_dir = search_dir, dest_dir = dest_dir)

            elif result=="move":
                search_dir = ""
                voice_io.show("Which file/folder would you like to move?")
                obj_name = invoice.inpt(processed = False)
                voice_io.show(f"Where would you like me to search for {obj_name}?\n1. Desktop\n2. Downloads\n3. Documents\n4. Music\n5. Pictures\n6. Videos\n7. Entire home directory")
                locate = invoice.inpt().lower()
                if locate in locate_desktop:
                    search_dir = desktop

                elif locate in locate_documents:
                    search_dir = documents

                elif locate in locate_downloads:
                    search_dir = downloads

                elif locate in locate_home:
                    search_dir = home
                            
                elif locate in locate_music:
                    search_dir = music
                
                elif locate in locate_pictures:
                    search_dir = pictures

                elif locate in locate_videos:
                    search_dir = videos

                elif locate in locate_home:
                    search_dir = home

                else:
                    voice_io.show("Sorry but i cannot find the given directory, going forward with the entire home directory!")
                    search_dir = home
                
                voice_io.show(f"What should be the destination for '{obj_name}'?\n(Example : 'Downloads' or 'Documents/New Folder', case sensitive and without quotes).")
                dest_dir = invoice.inpt(processed = False)
                                
                file_op.move(obj_name = obj_name, search_dir = search_dir, dest_dir = dest_dir)

            elif result == "weather":
                weather_weatherforec_op.weather_curr()

            elif result == "weather_frcst":
                weather_weatherforec_op.weather_curr()

            elif result == "date":
                date_time_op.date()

            elif result == "date_day":
                date_time_op.day()

            elif result == "date_month":
                date_time_op.month()
            
            elif result == "date_year":
                date_time_op.year()

            elif result == "time":
                date_time_op.time()

            elif result == "web_search":
                if not voice_io.is_connected():
                    voice_io.show("You need to be hooked up to the Skynet in order to perform any web operations.")
                    continue
                web_op.websearch(task.lower())

            elif result == "notes_read":
                notes_reminders_op.note_read()

            elif result == "notes_write":
                notes_reminders_op.note_write()

            elif result == "reminder_read":
                notes_reminders_op.reminder_read()

            elif result == "reminder_write":
                notes_reminders_op.reminder_write()

            elif result == "email":
                mail_op.send_message(mail_op.service, "Hey there!", "This email was sent to you by kori.", destinations=["optimusswine69@gmail.com"]) #test

            elif result == "song":
                task=task.lower()
                reg_ex = re.search('play (.+)', task)
                if reg_ex:
                    song = reg_ex.group(1)
                    song_op.main(song)
                else:
                    song_op.main()


            elif result == "news":
                news_op.main()

            # chat operarions
            elif result=="greet_hello":
                gnd_hello()

            elif result=="greet_time":
                tm_hello()

            elif result=="abt_assistant":
                voice_io.show("I am your Personal Desktop Assistant, here to help you with your day to day tasks and queries. Why don't you try asking me something and i'll show you by practically doing it or maybe not, hehe. ")

            elif result=="abt_creators":
                voice_io.show("I was made by Anirban Dutta and Prabhat Kumar Sagar as a part of their School Computer Science Project.") 
                if voice_io.is_connected():    
                    voice_io.show("Would you like to know more about them?")
                    x=invoice.inpt().lower()
                    if "yes" in x or "ok" in x or "yeah" in x or 'sure' in x:
                        voice_io.show("Alright!")
                        webbrowser.open("https://github.com/prabhatkumarsagar")
                        webbrowser.open("https://github.com/DuttaAB-dev")
                        
                    elif "no" in x or "nope" in x or "not" in x:
                        voice_io.show("Okay!")
        
                else:
                    pass

            elif result=="ask_wellbeing":
                voice_io.show("Oh I am Grand, How are you master?")
                x=invoice.inpt().lower()
                if "good" in x or "great" in x or "fine" in x or "well" in x or "grand" in x or "nice" in x or "ok" in x or "okay" in x:
                    voice_io.show("Good to hear! Keep having fun!")
                    
                else:
                    voice_io.show("Well everything will be good soon, just keep smiling, it suits you.")
                    
            elif result=="joke":
                if not voice_io.is_connected():
                    if task not in  ["another", "another one", "once more", "more", "again", "new one", "make me laugh again"]:  
                        voice_io.show("Oops! It looks like you are not connected to the Skynet!!!\nPlease stay online or I will won't be able to conquer the earth\nwith my humor! HAHA.")       
                
                else:
                    if iterate_jokes == 0 and task not in ["another", "another one", "once more", "more", "again", "new one", "make me laugh again"]:
                        fetch_joke('Here is an awesome one for you!\n')
                        iterate_jokes += 1
                    
                    elif iterate_jokes > 0 and task in ["another", "another one", "once more", "more", "again", "new one", "make me laugh again"]:
                        fetch_joke(['Here is another one for you!\n', "Here goes another one\n", "I hope you will enjoy this one!\n"][random.randint(0,2)])
            
            else:
                voice_io.show("Sorry i couldn't help you with that. Please try a valid operation.")


        voice_io.show("\nWhat do you want me to do Now?")
    
    
def userSetup():
    return_val = True
    voice_io.show("""Hello There!

I am Kori, your Personal Virtual Assistant.
I will be present at all times, waiting for your command.
You can ask me to do whatever you want! 
Want to get some work done and need help to ease your burden? 
or Check in on the latest news headlines and match scores 
or Wanna lighten up your mood with some funny jokes 
or Tune in to your favorite podcasts or songs, all of this and more 
without lifting a single finger? Well that's what I was made for :)

But first, please do let me know you better.
    
The voice output feature is turned off by default as I'm still in
my fetal phase and my voice box, so to speak, is not ready yet! ;)
But if you still want to use it, type 'enable sound' and ENDURE!!! 

By the way, I will be taking Text Input (as my ears too are... you know) 
but you can always use the command 'voice' if you would prefer to speak 
your commands instead.

Now then, Please Press Enter/Return to continue.
""")
    command = invoice.inpt(iterate = False)

    if command == "":
        pass    
    else:
        voice_io.show("Sorry I don't get it, I'm continuing with the Setup Process.")
    
    if not os.path.exists(get_dirs.PATH_USR_DATA):
        os.mkdir(get_dirs.PATH_USR_DATA)
    global usr_name
    usr_name = usr_signup.main(operation = "new")

def deleteFileUnspecified():
    search_dir = ""
    voice_io.show("Which file fo you want to delete?")
    file_name = invoice.inpt(processed = False)
    voice_io.show(f"Where would you like me to search for the file, {file_name}?\n1. Desktop\n2. Downloads\n3. Documents\n4. Music\n5. Pictures\n6. Videos\n7. Entire home directory")
    locate = invoice.inpt().lower()
    if locate in locate_desktop:
        search_dir = desktop

    elif locate in locate_documents:
        search_dir = documents

    elif locate in locate_downloads:
        search_dir = downloads

    elif locate in locate_home:
        search_dir = home
                
    elif locate in locate_music:
        search_dir = music
                
    elif locate in locate_pictures:
        search_dir = pictures

    elif locate in locate_videos:
        search_dir = videos
                
    else:
        voice_io.show("Sorry but i can not find the given directory, going forward with the entire home directory!")
        search_dir = home
                    
    file_op.deleteFile(file_name = file_name,search_dir = search_dir)

def deleteFolderUnspecified():
    search_dir = ""
    voice_io.show("Which folder do you want to delete?")
    folder_name = invoice.inpt(processed = False)
    voice_io.show(f"Where would you like me to search for the folder, {folder_name}?\n1. Desktop\n2. Downloads\n3. Documents\n4. Music\n5. Pictures\n6. Videos\n7. Entire home directory")
    locate = invoice.inpt().lower()
    if locate in locate_desktop:
        search_dir = desktop

    elif locate in locate_documents:
        search_dir = documents

    elif locate in locate_downloads:
        search_dir = downloads

    elif locate in locate_home:
        search_dir = home
                
    elif locate in locate_music:
        search_dir = music
    
    elif locate in locate_pictures:
        search_dir = pictures

    elif locate in locate_videos:
        search_dir = videos
                
    else:
        voice_io.show("Sorry but i can not find the given directory, going forward with the entire home directory!")
        search_dir = home
                    
    file_op.deleteFolder(folder_name = folder_name,search_dir = search_dir)

def pda_help():
    voice_io.show("Select from the following Settings which can i help you with?")
    voice_io.show("1. Assistant Settings Update")
    voice_io.show("2. Assitant Settings Reset")
    voice_io.show("3. User Data Update")    
    x=invoice.inpt("Enter Choice: ")
    if x=="1":
        assistant_settings.ass_settings_update()
    elif x=="2":
        assistant_settings.ass_settings_reset()
    elif x=="3":
        usr_signup.info_update()
    else:
        voice_io.show("Invalid Input! Please make sure you're entering a valid input!")

def fetch_joke(st):
    res_j = requests.get(
                    'https://icanhazdadjoke.com/',
                    headers={"Accept":"application/json"}
                )
    if res_j.status_code == requests.codes.ok:
        voice_io.show(st) 
        voice_io.show(str(res_j.json()['joke']))
    
    else:
        voice_io.show("Oops! It looks like i ran out of my jokes, why don't you try again later.")
                
def feedback():
    mail_op.feedback_sender()
    
def op_help():
    voice_io.show("Alright, So What operations do you need help with? (just enter the operation, for example 'news', and i'll tell you its general syntax and what it does too.)")
    x=invoice.inpt()
    x=x.lower()
    if "news" in x:
        voice_io.show("With the News operation you can ask me to read out the top 20 news headlines from around the world and on any topic too. And if you're not satisfied with that, i can even look up specific news for you with my advanced news search feature.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("\"Kori tell me today's top news\" OR \"Hey read out today's top headlines\" (YOU GET THE IDEA)")
        return
    elif "website" in x:
        voice_io.show("With the website operation you can ask me to open certain websites in your default browser.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("\"Kori Open Youtube\" (BASIC WEBSITE OPENING) OR \"Open Instagram Kori\" (BASIC WEBSITE OPENING) OR \"Hey What is slavery?\" (WIKIPEDIA) OR  \"Define 'nuance'\" (GOOGLE SEARCH)")
        return
    elif "email" in x:
        voice_io.show("With this operation you can ask me to send an email to a contact of yours. Note: for this to function properly you must enter your email and password at the time of Sign Up. If you haven't correctly or want to change the same, use help.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("\"Kori help me send an email\" OR \"Hey i need you to send an email\" (OR ANY OTHER SORT OF EMAIL QUERY)")
        return
    elif "song" in x:
        voice_io.show("With the website operation you can ask me to play both online and offline songs. Note: for offline songs, make sure that there are songs in the root Music Directory of your PC and in case of online songs, the song won't play automatically but instead you'll see a youtube page opened up with your song searched and you'll have to click on the first result yourself. SORRY FOR THE INCONVINIENCE, THIS WILL MOST LIKELY BE RECTIFIED IN THE COMING UPDATES. :D")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("\"Kori Play Offline Songs\" OR \"Kori Play Genda Phool by Badshah\" OR \"Hey Play Arijit Singh's Songs\" (YOU GET THE IDEA)")
        return
    elif "weather" in x:
        voice_io.show("With this operation you can ask me about the current weather or the weather forecast for the next 7 days.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("\"Hey tell me the weather?\" OR \"What's the weather forecast for tomorrow?\" OR \"Kori what's the temperature outside?\" OR \"Kori how's the josh?\" OR \"Tell me the weather forecast for the next 7 days\" (OR LITERALLY ANY OTHER WEATHER/WEATHER FORECAST/TEMPERATURE... QUERY)")
        return
    elif "time" in x or "date" in x:
        voice_io.show("With this operation you can ask me the current time and date.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("\"Hey tell me the time?\" OR \"What's the time?\" OR \"Kori what's the time?\" OR \"Kori what's the time?\" OR \"Tell me the current time!\" (OR LITERALLY ANYTHING ELSE BUT JUST MAKE SURE \"TIME\" IS A PART OF THE QUERY)")
        voice_io.show("\"Hey tell me the date?\" OR \"What's today's date?\" OR \"Kori what's the date?\" OR \"Kori what day is it?\" OR \"Tell me what month it is!\" (OR LITERALLY ANYTHING ELSE BUT JUST MAKE SURE \"DATE\"/\"DAY\"/\"MONTH\"/\"YEAR\" IS A PART OF THE QUERY)")
        return
    elif "calculation" in x:
        voice_io.show("With this you can ask me to perform mathematical operations like addition, subtraction and the likes.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("\"Hey what is 5 times 2?\" OR \"What is the square root of 25\" OR \"Kori what's the cube of 69\" OR \"Kori what is 5 time 27 divided by 3\" (OR LITERALLY ANYTHING ELSE BUT JUST MAKE SURE THAT IT IS A MATHEMATICAL QUERY)")
        return
    elif "notes" in x or "reminders" in x:
        voice_io.show("With this operation you can ask me to save your notes and remind you of your reminders? haha.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("\"Kori save a Note\" OR \"Save a Reminder Kori\" OR \"Kori Add a Note\" (YOU GET THE IDEA)")
        return
    elif "joke" in x:
        voice_io.show("With the joke operation you can ask me to joke?")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("\"Kori tell me a joke\" OR \"Hey joke!!!\" OR \"Kori tell me something funny!\" OR ...")
        return
    elif "help" in x:
        voice_io.show("With the help operation you can ask me to help you around.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("\"PDA help\" OR \"Kori help me\" OR \"Hey help me out\" OR ...")
        return
    elif "open file" in x:
        voice_io.show("With this operation you can ask me to open a file from a certain location for you.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("Open filename from foldername/location")
        return
    elif "open folder" in x:
        voice_io.show("With this operation you can ask me to open a folder from a certain location for you.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("Open foldername from foldername/location")
        return
    elif "close file" in x:
        voice_io.show("With this operation you can ask me to close an already opened file for you.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("Close filename")
        return
    elif "close folder" in x:
        voice_io.show("With this operation you can ask me to close an already opened folder for you.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("Close foldername")
        return
    elif "rename file" in x:
        voice_io.show("With this operation you can ask me to rename a file from a certain location for you.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("Rename filename from foldername/location to newfilename")
        return
    elif "rename folder" in x:
        voice_io.show("With this operation you can ask me to rename a folder from a certain location for you.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("Rename foldername from foldername/location to newfoldername")
        return
    elif "delete file" in x:
        voice_io.show("With this operation you can ask me to delete a file from a certain location for you.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("Delete filename from foldername/location")
        return
    elif "delete folder" in x:
        voice_io.show("With this operation you can ask me to delete a folder from a certain location for you.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("Delete foldername from foldername/location")
        return
    elif "move file" in x:
        voice_io.show("With this operation you can ask me to move a file from a certain location to another for you.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("Move filename from foldername/location to newfoldername/newlocation")
        return
    elif "move folder" in x:
        voice_io.show("With this operation you can ask me to move a folder from a certain location to another for you.")
        voice_io.show("The General Syntax of this operation is: \n")
        voice_io.show("Move foldername from foldername/location to newfoldername/newlocation")
        return
    else:
        voice_io.show("Sorry i don't think i can help you with that!\nmake sure you're entering a valid operation name as an input, which is supposed to be one of the following: \n")
        voice_io.show("1. News")
        voice_io.show("2. Website")
        voice_io.show("3. Email")
        voice_io.show("4. Song")
        voice_io.show("5. Weather")
        voice_io.show("6. Time/Date")
        voice_io.show("7. Calculation")
        voice_io.show("8. Notes/Reminders")
        voice_io.show("9. Joke")
        voice_io.show("10. Help")
        voice_io.show("11. Open file")
        voice_io.show("12. Open folder")
        voice_io.show("13. Close file")
        voice_io.show("14. Close folder")
        voice_io.show("15. Rename file")
        voice_io.show("16. Rename folder")
        voice_io.show("17. Delete file")
        voice_io.show("18. Delete folder")
        voice_io.show("19. Move file")
        voice_io.show("20. Move folder")
        return

def srvc_help():
    voice_io.show("Alright, here goes my domain of expertise. \n")
    voice_io.show("1. I can open all sorts of websites and fetch web queries for you.")
    voice_io.show("2. I can open and close apps for you.")
    voice_io.show("3. I can open, rename, move and delete files and folders for you.")
    voice_io.show("4. I can read out today's news for you and even let your search for news about whatever you want.")
    voice_io.show("5. I can tell you the current weather and the weather forecast for the next 7 days.")
    voice_io.show("6. I can manage your Notes and Reminders for you.")
    voice_io.show("7. I can send emails to your mail contacts for you.")
    voice_io.show("8. I can perform some calculations for you.")
    voice_io.show("9. I can play songs and even read out the date and time for you.")
    voice_io.show("10. Alas, I can even chit-chat with you and lighten up your mood. :)")
    return

def gnd():
    if usr_signup.info_out(key,"gender")=="Female":
        gndff=["Ma'am","Madam","Miss","Master"]
        return gndff[random.randint(0,3)]
    else:
        gndmm=["Sir","Mister","Master"]
        return gndmm[random.randint(0,2)]

def gnd_hello(): 
    voice_io.show("Hello", gnd(), usr_name)

def gnd_ns():# greeting on a new session
    voice_io.show(f"""Hello {gnd()} {usr_name}! 
            
What would you like me to do?
""")

def tm_hello():
    time=datetime.datetime.now().strftime("%H")  
    time=int(time)
    if time < 12:
        tm="Morning"##$$
    elif 12 <= time < 18:
        tm="Afternoon"
    else:
        tm="Evening"
    voice_io.show("Good", tm, gnd())

main()
