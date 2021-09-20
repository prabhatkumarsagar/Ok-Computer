from re import A
from pac import encryption
import pickle
from sys import path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from base64 import urlsafe_b64decode, urlsafe_b64encode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import MimeTypes, guess_type as guess_mime_type
import os,time
from pathlib import Path
import shutil

try:
    from pac import usr_signup,get_dirs,file_op,clear
except:
    import usr_signup,get_dirs,file_op,clear

"""
SCOPES = ['https://mail.google.com/']
key=encryption.getkey()
usr_email = usr_signup.main(operation = "fetch", data_type = "email",key=key)
mail_path=get_dirs.PATH_EMAIL

if not os.path.exists(mail_path):
    os.mkdir(mail_path)
else:
    shutil.rmtree(mail_path)
    os.mkdir(mail_path)
"""


class mail:
    def __init__(self,key):
        self.mkdir=True
        self.FT=True
        self.cwd=Path(__file__).parent
        self.SCOPES = ['https://mail.google.com/']
        self.key=key
        self.usr_email = usr_signup.main(operation = "fetch", data_type = "email",key=self.key)
        self.mail_path=get_dirs.PATH_EMAIL
        if not os.path.exists(self.mail_path):
            os.mkdir(self.mail_path)
        else:
            shutil.rmtree(self.mail_path)
            os.mkdir(self.mail_path)


    def gmail_authenticate(self):
        creds = None
        os.chdir(self.cwd)
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print("Looks like you didn't authenticate my Email Services when signing up, would you like to do that now? You know I will be needing this to continue, right? Press: ")
                ch=input("\n1. To authenticate it right now, like a good master! ^o^\n2. To skip and not be cool to me, like a bad master! U_U\n")
                if ch=='1':
                    flow = InstalledAppFlow.from_client_secrets_file(f'{self.cwd}\gmail_creds.json', self.SCOPES)
                    creds = flow.run_local_server(port=0)
                elif ch=='2':
                    return
                else:
                    print("Invalid Input, Skipping!")
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds)


    def send(self,type='email'):
        service=self.gmail_authenticate()
        def atchmnt(message, filename):
            content_type, encoding = guess_mime_type(filename)
            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split('/', 1)
            if main_type == 'text':
                fp = open(filename, 'rb')
                msg = MIMEText(fp.read().decode(), _subtype=sub_type)
                fp.close()
            elif main_type == 'image':
                fp = open(filename, 'rb')
                msg = MIMEImage(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'audio':
                fp = open(filename, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=sub_type)
                fp.close()
            else:
                fp = open(filename, 'rb')
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(fp.read())
                fp.close()
            filename = os.path.basename(filename)
            msg.add_header('Content-Disposition', 'attachment', filename=filename)
            message.attach(msg)

        def message(destination, obj, body, attachments=[]):
            if not attachments:
                message = MIMEText(body)
                message['to'] = destination
                message['from'] = self.usr_email
                message['subject'] = obj
            else:
                message = MIMEMultipart()
                message['to'] = destination
                message['from'] = self.usr_email
                message['subject'] = obj
                message.attach(MIMEText(body))
                for filename in attachments:
                    atchmnt(message, filename)
            return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

        def email(sub,body,destinations=[],attachment=[]):
            try:
                if len(destinations)==1:
                    service.users().messages().send(
                    userId="me",
                    body=message(destinations[0], sub, body, attachment)
                    ).execute()
                    print("\nDone! Your Email was sent successfully!")
                else:
                    for destination in destinations:
                        service.users().messages().send(
                        userId="me",
                        body=message(destination, sub, body, attachment)
                        ).execute()
                    print("\nDone! Your Emails were sent successfully!")

            except Exception as e:
                print("Uh-oh! Looks like I ran into some errors doing that, why don't you try that again later and incase the problem persists report it to the developers!?")
                print('\nError Message: ', e)

        def atchcheck():
            x=input("\nDo you want to add any attachment(s) to the email or not?\n")
            x_y=["yes","yep","ok","yeah","yeap"]
            if x.lower() in x_y:
                return True
            else:
                return False

        if type.lower()=='email':
            destinations=input("\nWho do you want to send the email to? (for more than one recipients separate by commas like - 'rec1@mail.com,rec2@mail.com,...') \n")
            destinations=destinations.split(sep=',')
            print("\nNow enter the subject of the email!")
            sub=input("Here: ")
            print("\nand the body!")
            body=input("Here: ")  
            if atchcheck():
                atch=[]
                while True:
                    atch1=input("\nEnter the file name with the full path: \n")
                    atch.append(atch1)
                    ch=input("\nDo you want to add any more attachment(s)? \n1. Yes \n2. No\n")
                    if ch=='1':
                        continue
                    else:
                        break
                print("Please wait...")
                email(sub,body,destinations=destinations,attachment=atch)

            else:
                print("Please wait...")
                email(sub,body,destinations=destinations)

        if type.lower()=='feedback':
            destinations=['korihelpdesk@gmail.com','duttashaan102@gmail.com','sagarprabhatkumar9733@gmail.com']
            def feedback(sub,body,destinations=destinations,attachment=[]):
                try:
                    for destination in destinations:
                        service.users().messages().send(
                        userId="me",
                        body=message(destination,sub,body,attachment)
                        ).execute()
                    print("\nDone! Your Feedback was sent successfully!")
                except Exception as e:
                    print("Uh-oh! Looks like I ran into some errors doing that, why don't you try that again later and incase the problem persists report it to the developers!?")
                    print('\nError Message: ', e)
            
            print("\nHere's what you can do: ")
            print("1. Report a bug")
            print("2. Suggest improvement(s)")
            print("3. Get in touch with the developers")
            print("4. Something else")
            print("5. Nothing (Exit)\n")
            x=input("Enter Choice: ")
            if x=="1":
                sub="Kori User Feedback - Bug Report"
                body=input("Please specify the bug you've encountered: ")
                if atchcheck():
                    atch=[]
                    while True:
                        atch1=input("\nEnter the file name with the full path: \n")
                        atch.append(atch1)
                        ch=input("\nDo you want to add any more attachment(s)? \n1. Yes \n2. No\n")
                        if ch=='1':
                            continue
                        else:
                            break
                    print("Please wait...")
                    feedback(sub,body,atch)
                else:
                    print("Please wait...")
                    feedback(sub,body)

            elif x=="2":
                sub="Kori User Feedback - Suggestions"
                body=input("Please explain what improvement would you like to see in the future updates: ")
                if atchcheck():
                    atch=[]
                    while True:
                        atch1=input("\nEnter the file name with the full path: \n")
                        atch.append(atch1)
                        ch=input("\nDo you want to add any more attachment(s)? \n1. Yes \n2. No\n")
                        if ch=='1':
                            continue
                        else:
                            break
                    print("Please wait...")
                    feedback(sub,body,atch)
                else:
                    print("Please wait...")
                    feedback(sub,body)

            elif x=="3":
                sub="Kori User Feedback - Contact"
                body=input("What do you want to say to my developers: ")
                if atchcheck():
                    atch=[]
                    while True:
                        atch1=input("\nEnter the file name with the full path: \n")
                        atch.append(atch1)
                        ch=input("\nDo you want to add any more attachment(s)? \n1. Yes \n2. No\n")
                        if ch=='1':
                            continue
                        else:
                            break
                    print("Please wait...")
                    feedback(sub,body,atch)
                else:
                    print("Please wait...")
                    feedback(sub,body)

            elif x=="4":
                sub="Kori User Feedback - Misc."
                body=input("What would you like to say: ")
                if atchcheck():
                    atch=[]
                    while True:
                        atch1=input("\nEnter the file name with the full path: \n")
                        atch.append(atch1)
                        ch=input("\nDo you want to add any more attachment(s)? \n1. Yes \n2. No\n")
                        if ch=='1':
                            continue
                        else:
                            break
                    print("Please wait...")
                    feedback(sub,body,atch)
                else:
                    print("Please wait...")
                    feedback(sub,body)

            elif x=="5":
                print("Alright, come back again when you have something to say!")

            else:
                print("Invalid Input! Please try again!")

    def read(self):
        service=self.gmail_authenticate()
        os.chdir(self.mail_path)
        if self.FT==True:
            y=input("Hey before I do anything I just wanted to let you know that, I by default save the emails, that I read, locally in your 'Documents/Kori/Emails' folder, but you can turn this feature off if you're concerned about your privacy! But again I'd recommend not to as I also save and open the attachments (if any) from your emails using that feature so... yeah. You can also ask me to clear out the folder whenever you want though. So what do you wanna do? \n1. Keep local email saving turned on (you can turn this off later from Kori Settings) \n2. Turn off local email saving (you can turn this on later from Kori Settings)\n")
            if y=='1':
                print("\nAlright, alright!")
                self.mkdir=True
            elif y=='2':
                print("\nAlright, as you wish!")
                self.mkdir=False
            else:
                print("\nInvalid Input! Turning it off! If you wanna keep it on, you can do that from Kori Settings.")
        self.FT=False

        def list_messages(lblId=['INBOX'], query='', max=10):
            if query!='':
                result = service.users().messages().list(userId='me',maxResults=max, q=query, labelIds=lblId).execute()
            else:
                result = service.users().messages().list(userId='me',maxResults=max, labelIds=lblId).execute()
            messages = []
            if 'messages' in result:
                messages.extend(result['messages'])
            return messages

        def get_size_format(b, factor=1024, suffix="B"):
            for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                if b < factor:
                    return f"{b:.2f}{unit}{suffix}"
                b /= factor
            return f"{b:.2f}Y{suffix}"

        def clean(text):
            return "".join(c if c.isalnum() else "_" for c in text)

        def parse_parts(parts, folder_name, message, main):
            if parts:
                for part in parts:
                    filename = part.get("filename")
                    mimeType = part.get("mimeType")
                    body = part.get("body")
                    data = body.get("data")
                    file_size = body.get("size")
                    part_headers = part.get("headers")
                    if part.get("parts"):
                        parse_parts(service, part.get("parts"), folder_name, message, main)

                    if mimeType == "text/plain":
                        if data:
                            text = urlsafe_b64decode(data).decode()
                            print("\nTo:",main['to'])
                            print("From:",main['from'])
                            print("Date:",main['date'])
                            print("Subject:",main['sub'])
                            print(text)

                    elif mimeType == "text/html":
                        print("-"*50)
                        yn=input("\nI know that was pretty weird, I'm sorry for that but you see this was a HTML email and I'm still learning how to handle those, so what I recommend right now is you save it as a HTML file and view it in your default browser and know what? I can do that for you! So may I? \n1. Yes \n2. No\n")
                        if yn=='1' or yn.lower() in ['yes','yep','yeah','ok']:
                            if self.mkdir:
                                if not filename:
                                    filename = "index.html"
                                filepath = os.path.join(folder_name, filename)
                                
                                print(f"\nSaving the HTML file to {os.getcwd()}\\{filepath} and opening.\nPlease Wait...")
                                with open(filepath, "wb") as f:
                                    f.write(urlsafe_b64decode(data))
                                file_op.open_file(filepath)
                            else:
                                print("\nHey you've disabled the local email saving setting, please turn that on to continue!")
                                return
                        else:
                            print("\nAlright!")

                    else:
                        for part_header in part_headers:
                            part_header_name = part_header.get("name")
                            part_header_value = part_header.get("value")
                            if part_header_name == "Content-Disposition":
                                if "attachment" in part_header_value:
                                    print("-"*50)
                                    yn=input("Found an attachment inside the email! Would you like to save it and see it? \n1. Yes \n2. No\n")
                                    if yn=='1' or yn.lower() in ['yes','yep', 'yeah', 'ok']:
                                        print(f"\nSaving the attachment file: {filename} size: {get_size_format(file_size)} to {os.getcwd()}\\{folder_name}\\{filename} and opening.\nPlease wait...")
                                        attachment_id = body.get("attachmentId")
                                        attachment = service.users().messages().attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                                        data = attachment.get("data")
                                        filepath = os.path.join(folder_name, filename)
                                        if data:
                                            with open(filepath, "wb") as f:
                                                f.write(urlsafe_b64decode(data))
                                        file_op.open_file(filepath)

                                    else:
                                        print("Alright!\n")

        def read_messages(message):
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            payload = msg['payload']
            headers = payload.get("headers")
            parts = payload.get("parts")
            cur_folder = os.getcwd()
            folder_name = "null emails"
            has_subject = False
            main={}
            if headers:
                for header in headers:
                    name = header.get("name")
                    value = header.get("value")
                    if name.lower() == 'from':
                        main["from"] = value
                    if name.lower() == "to":
                        main["to"] = value
                    if name.lower() == "subject":
                        has_subject = True
                        folder_name = clean(value)
                        folder_counter = 0
                        while os.path.isdir(folder_name):
                            folder_counter += 1
                            if folder_name[-1].isdigit() and folder_name[-2] == "_":
                                folder_name = f"{folder_name[:-2]}_{folder_counter}"
                            elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                                folder_name = f"{folder_name[:-3]}_{folder_counter}"
                            else:
                                folder_name = f"{folder_name}_{folder_counter}"
                        if self.mkdir:
                            os.chdir(cur_folder)
                            os.mkdir(folder_name)
                        main["sub"] = value
                    if name.lower() == "date":
                        main["date"] = value

            if not has_subject and self.mkdir:
                if not os.isdir(folder_name):
                    os.chdir(cur_folder)
                    os.mkdir(folder_name)
            parse_parts(parts, folder_name, message, main)
            print("="*75,"\n")
            time.sleep(5)
            #input("Press Enter/Return to continue.")
            #clear.clear()

        

        print("\Here are the 10 latest emails from your Inbox: (Note this is the default email reading schema, if you wish to read specific emails with advanced search options you can do that by going to the main email screen by typing 'email' in the Kori console and choosing the 3rd option there or, by simpy typing 'advanced email' or 'search email') ")
        time.sleep(3)
        mails=list_messages()
        for mail in mails:
            read_messages(mail)
"""
    def qry_parser():
        print(#
This is the search query format/parameters:

To specify the sender -
from:               Example: from:david@gmail.com

To specify a recipient	-
to:                 Example: to:amy@gmail.com

Words in the subject line -
subject:            Example: subject:cs project

Messages that match multiple terms -	
OR                  Example: from:amy OR from:david

Remove messages from your results -
-                   Example: dinner -movie

Messages that have a certain label -	
label:              Example: label:friends

Messages that have an attachment -	
has:attachment      Example: has:attachment

Search for an exact word or phrase -
" "                 Example: "dinner and movie tonight"

Group multiple search terms together -
( )                 Example: subject:(dinner movie)

Messages in any folder, including Spam and Trash -
in:                 Example: in:anywhere 

Search for messages that are marked as important, starred, snoozed, unread, or read messages -
is:                 Example: is:important

Search for messages sent during a certain time period -
after:              Example: after:2004/04/16
before:             Example: before:04/18/2004

Search for messages older or newer than a time period using d (day), m (month), and y (year) -
older_than:         Example: older_than:1m
newer_than:         Example: newer_than:2d

Search by email for delivered messages -
deliveredto:        Example: deliveredto:username@gmail.com

Messages in a certain category (primary,social,promotions,updates,forums,reservations,purchases) -
category:           Example: category:updates

Results that match a word exactly -
+                   Example: +unicorn

No of results -
NR:                 Example: NR:25
#)
    q=[]
    while True:
        param=input("Enter search query using the above format: ")
        try:
            params=param.split(':')
            q.append((params[0],params[1]))
        except:
            print("Looks like the query is not proper'y")
        q.append(param)
        c=input("\nPress:\n1. To add another query\n2. To continue\n")
        if c=='1':
            continue
        elif c=='2':
            qry=""
            #for i in q:
             #   if 
        else:
            print("Invalid Input!")

    def search_param(self,query):
        print("Here are your search parameters: ")
        

    def mark_as_read(self):
        messages_to_mark = self.read().search_messages(self.qry_parser)
        return self.service.users().messages().batchModify(
        userId='me',
        body={
            'ids': [ msg['id'] for msg in messages_to_mark ],
            'removeLabelIds': ['UNREAD']
        }
        ).execute()

    def mark_as_unread(service, query):
        messages_to_mark = search_messages(query)
        return service.users().messages().batchModify(
            userId='me',
            body={
                'ids': [ msg['id'] for msg in messages_to_mark ],
                'addLabelIds': ['UNREAD']
            }
        ).execute()

    def delete_messages(service, query):
        messages_to_delete = search_messages(service, query)
        # it's possible to delete a single message with the delete API, like this:
        # service.users().messages().delete(userId='me', id=msg['id'])
        # but it's also possible to delete all the selected messages with one query, batchDelete
        return service.users().messages().batchDelete(
        userId='me',
        body={
            'ids': [ msg['id'] for msg in messages_to_delete]
        }
        ).execute()
"""
def main(key):
    x=mail(key)
    mes='?'
    while True:
        y=input(f"Hi! What do you want me to do{mes} Press: \n1. To send out email(s) \n2. To read out the latest email(s) from your Inbox \n3. To search for specific email(s) and read them \n4. To mark as read/unread email(s) \n5. To delete email(s) \n6. To send feedback \n7. To clear local email repository \n8. To go back.\n")
        mes=' now?'
        if y=='1':
            clear.clear()
            x.send()
        elif y=='2':
            clear.clear()
            x.read()
        elif y=='3':
            pass
        elif y=='4':
            pass
        elif y=='5':
            pass
        elif y=='6':
            clear.clear()
            x.send('feedback')
        elif y=='7':
            return
        else:
            print("Invalid Input!")




"""
    def etc(self):



        m={}
>>> m['in']='sent' 
>>> m['to']='pk' 
>>> m['after']='2014/01/01' 
>>> m
{'in': 'sent', 'to': 'pk', 'after': '2014/01/01'}
>>> m.items()
dict_items([('in', 'sent'), ('to', 'pk'), ('after', '2014/01/01')])
>>> l=m.items()
>>> l
dict_items([('in', 'sent'), ('to', 'pk'), ('after', '2014/01/01')])
>>> l=list(l) 
>>> l
[('in', 'sent'), ('to', 'pk'), ('after', '2014/01/01')]
>>> s=""     
>>> for i in l:
...     x,y=i
...     z=f"{x} : {y} "
...     s+=z
... 
>>> s
'in : sent to : pk after : 2014/01/01 '
>>> s=""        
>>> for i in l:
...     x,y=i
...     z=f"{x}:{y} "   
...     s+=z    
... 
>>> s
'in:sent to:pk after:2014/01/01 '
>>> s.rstrip()
'in:sent to:pk after:2014/01/01'
"""