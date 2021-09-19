import importlib.util
import sys
import os
import subprocess
import socket
import pip

def install(packages = {}):
    if packages == {}:
        commands = {
            "gtts": "pip3 install gTTS",
            "playsound": "pip3 install playsound",
            "pyttsx3": "pip3 install pyttsx3",
            "speech_recognition": "pip3 install SpeechRecognition",
            "bs4": "pip3 install bs4",
            "wolframalpha": "pip3 install wolframalpha",
            "wikipedia": "pip3 install wikipedia",
            "pyaudio": "pip install https://download.lfd.uci.edu/pythonlibs/r4tycu3t/PyAudio-0.2.11-cp310-cp310-win_amd64.whl",
            "pyowm": "pip3 install pyowm",
            "geocoder": "pip3 install geocoder",
            "cryptography": "pip3 install cryptography",
            "lxml": "pip3 install lxml",
            "tabulate": "pip3 install tabulate",
            "plyer": "pip3 install plyer",
            "bcrypt": "pip3 install bcrypt",
            "gmail": "pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib"
        }
    else:
        commands = packages

    for name in commands.keys():
        if name in sys.modules:
            pass
        elif (spec := importlib.util.find_spec(name)) is not None:
            pass
        else:
            if name == "pipwin" and os.name != "nt":
                continue
            if name == "pyaudio" and os.name == "posix":
                print("Your system is missing the python package PyAudio which is required by this program for voice functions.")
                print("Please install 'python3-pyaudio' manually from your distro repos and run this program again.")
                return False
            try:
                subprocess.check_output(commands[name], shell = True)
            except subprocess.CalledProcessError:
                if os.name == "nt":
                    print("Installation of required packages failed!\nPIP has either not been installed in your system or not been added to the PATH. Please do it that ASAP to continue.")
                
                else :
                    print("PIP3 is not installed in your system! \nPlease do it that ASAP to continue.")
                
                return False

            except pip._vendor.urllib3.exceptions.ReadTimeoutError or socket.timeout:
                print("Unable to download the required packages.\nTry connecting to the internet or using a faster connection.")
                return False
                
    return True
