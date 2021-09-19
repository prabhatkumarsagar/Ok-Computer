import os

if os.name == 'nt':
	HOME =  os.environ['USERPROFILE']
	seq="\\"
	CDRIVERPATH = os.getcwd()
	CDRIVERPATH = CDRIVERPATH+'\pac\chromedriver_win.exe'
        
elif os.name == 'posix':
	HOME = os.getenv("HOME")
	seq="/"
	CDRIVERPATH = os.getcwd()
	CDRIVERPATH = CDRIVERPATH+'/pac/chromedriver_win.exe'

#important user directories
CUR_DIR = os.getcwd()
DESKTOP =  HOME + f"{seq}Desktop"
DOWNLOADS = HOME + f"{seq}Downloads"
DOCUMENTS = HOME + f"{seq}Documents"
MUSIC = HOME + f"{seq}Music"
PICTURES = HOME + f"{seq}Pictures"
VIDEOS = HOME + f"{seq}Videos"

#Assistant data directories
PATH_USR_DATA = HOME + f"{seq}Documents{seq}Kori{seq}"
FILE_ASSISTANT_SETTINGS = PATH_USR_DATA + f"{seq}assistant_settings.dat"
FILE_SOUND_VALUE = PATH_USR_DATA + 'ass_sound_val.dat'
FILE_USR_DATA = PATH_USR_DATA + 'user_info.dat'
FILE_ENCRYPT_KEY = PATH_USR_DATA + 'key.bin'
DB_NOTES_REMINDERS = PATH_USR_DATA + 'notes_reminders.db'