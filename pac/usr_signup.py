import pickle as pk
import time
import os
import getpass
from platform import processor
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pathlib import Path
cwd=Path(__file__).parent

try:
    from pac import get_dirs, clear, voice_io, invoice
except:
    import get_dirs,clear,voice_io,invoice

SCOPES = ['https://mail.google.com/']

def gmail_authentication():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pk.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(f'{cwd}\gmail_creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pk.dump(creds, token)

key = ""
def setNewUser():
    usr_info_dic={}
    clear.clear()
    voice_io.show("What shall I call you Master? ")
    nm = bytes(invoice.inpt(), encoding = "utf-8") #Name of the user i.e the name by which the assistant will call him/her
    voice_io.show("\nAnd you are, Master or Miss, master? ") #Gender of the user
    gnd = invoice.inpt()
    asst_pswd = bytes(getpass.getpass(voice_io.show("\nWhat should be your password for accessing me?",show_output = False) + "\nPassword: "), encoding = "utf-8")
    salt = b'$2b$12$3hbla5Xs2Ekx9SGVYfWQuO'
    hashed_pswd = bcrypt.hashpw(asst_pswd, salt)
    kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=salt,
                        iterations=100000,
                    )
    global key
    key = base64.urlsafe_b64encode(kdf.derive(hashed_pswd))
    #with open(get_dirs.FILE_ENCRYPT_KEY,'wb+') as f:
    #    f.write(key)
    voice_io.show("\nAnd now what would be your 'gmail' address? Note: Right now I support gmail (google) accounts only, so please make one if you don't have one already, to continue! ")
    eml = bytes(invoice.inpt(processed= False), encoding = "utf-8")
    print("\nLastly I need you to authenticate this with Daddy Google for me, you can skip this now but know that I will be needing this to perform Email Operations! Press: ")
    ch=input("\n1. To authenticate it right now, like a good master! ^o^\n2. To skip and not be cool to me, like a bad master! U_U\n")
    if ch=='1':
        gmail_authentication()
    elif ch=='2':
        pass
    else:
        print("Invalid Input, Skipping!")
    cipher_suite = Fernet(key)
    usr_info_dic['name']=cipher_suite.encrypt(nm)
    GND_FEMALE=["girl",'miss','missus','mrs','female','lady','woman']
    GND_MALE=["boy","master","mister","mr","male","lodu","man"]
    if gnd.lower() in GND_FEMALE:
        usr_info_dic['gender']=cipher_suite.encrypt(b"Female")
    elif gnd.lower() in GND_MALE:
        usr_info_dic['gender']=cipher_suite.encrypt(b"Male")
    else:
        usr_info_dic['gender']=cipher_suite.encrypt(b"Others")
    usr_info_dic["asst_password"] = cipher_suite.encrypt(hashed_pswd)
    usr_info_dic['email']=cipher_suite.encrypt(eml)
    info_in(usr_info_dic)
    voice_io.show("Well then you're good to go! Just press Enter/Return to continue!", end = "")
    invoice.inpt("", iterate = False)
    return key, nm.decode("utf-8")

def info_in(x):
    f2=open(get_dirs.FILE_USR_DATA,'wb+')
    pk.dump(x,f2)
    f2.close()


def info_out(key, x="all"):
    f=open(get_dirs.FILE_USR_DATA,'rb+')
    cipher_suite = Fernet(key)
    rd=pk.load(f)
    ch=x.lower()
    f.close()
    if ch=="name":
        name = ""
        try:
            name = bytes(cipher_suite.decrypt(rd[ch])).decode("utf-8")
            return name
        except:
            return False

    elif ch=="gender":
        return bytes(cipher_suite.decrypt(rd[ch])).decode("utf-8")

    elif ch=="email":
        return bytes(cipher_suite.decrypt(rd[ch])).decode("utf-8")

    elif ch=="all":
        nrd = {}
        for i in rd.keys():
            nrd[i] = bytes(cipher_suite.decrypt(rd[i])).decode("utf-8")
        return nrd

    else:
        return False

u=''

#dutta fix this shit up, this is so damn mindbendingly crappy
def in_upd_entr(key=key):
    global u
    cipher_suite = Fernet(key)
    usr_info1 = get_dirs.FILE_USR_DATA
    usr_info2 = get_dirs.PATH_USR_DATA + "/user_info1.dat"
    f1=open(usr_info1,"rb+")
    f2=open(usr_info2,"wb+")
    x=input("Enter new value : ")
    while True:
        r=pk.load(f1)
        r[u]=x
        pk.dump(r,f2)
        #f2.flush()
        break
    f1.close()
    f2.close()
    os.remove(usr_info2)
    os.rename("usr_info1.dat","usr_info.dat")
    f=open("./usr_info.dat","rb+")
    rd=pk.load(f)
    f3=open(get_dirs.FILE_USR_DATA,'wb+')
    pk.dump(rd,f3)
    f3.close()
    f.close()

def info_update():
    global u
    while True:
        voice_io.show("What do you wanna Update?")
        voice_io.show("1. Name")
        voice_io.show("2. Gender")
        voice_io.show("3. Email")
        voice_io.show("5. Nothing (Exit)")
        ch=input("What entry do you want to update? ")
        if ch=='1':
            u='name'
            in_upd_entr()
            break
        elif ch=='2':
            u='gender'
            in_upd_entr()
            break
        elif ch=='3':
            u='email'
            in_upd_entr()
            break
        elif ch=='4':
            u='password'
            in_upd_entr()
            break
        elif ch=='5':
            return
        else:
            voice_io.show("Invalid Input!")
            return
    voice_io.show("Data Updated Successfully!")

def main(**kwargs):
    if kwargs["operation"] == "new":
        return setNewUser()
    
    elif kwargs["operation"] == "fetch":
        return info_out(kwargs["key"], kwargs["data_type"])

    elif kwargs["operation"] == "update":
        info_update(kwargs["key"])
