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
import os
from pathlib import Path
import shutil
cwd=Path(__file__).parent
try:
    from pac import usr_signup,get_dirs
except:
    import usr_signup,get_dirs
SCOPES = ['https://mail.google.com/']
key=encryption.getkey()
usr_email = usr_signup.main(operation = "fetch", data_type = "email",key=key)
mail_path=get_dirs.PATH_EMAIL

if not os.path.exists(mail_path):
    os.mkdir(mail_path)
else:
    shutil.rmtree(mail_path)
    os.mkdir(mail_path)

def gmail_authenticate():
    creds = None
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
                flow = InstalledAppFlow.from_client_secrets_file(f'{cwd}\gmail_creds.json', SCOPES)
                creds = flow.run_local_server(port=0)
            elif ch=='2':
                return
            else:
                print("Invalid Input, Skipping!")
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


def send(type='email'):
    service=gmail_authenticate()
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
            message['from'] = usr_email
            message['subject'] = obj
        else:
            message = MIMEMultipart()
            message['to'] = destination
            message['from'] = usr_email
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
                print("\nThe Email was sent successfully!")
            else:
                for destination in destinations:
                    service.users().messages().send(
                    userId="me",
                    body=message(destination, sub, body, attachment)
                    ).execute()
                print("\nThe Emails were sent successfully!")

        except Exception as e:
            print("Uh-oh! Looks like I ran into some errors doing that, why don't you try that again later and incase the problem persists report it to the developers.")
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
            email(sub,body,destinations=destinations,attachment=atch)

        else:
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
                print("\nThe Feedback was sent successfully!")
            except Exception as e:
                print("Uh-oh! Looks like I ran into some errors doing that, why don't you try that again later and incase the problem persists report it to the developers.")
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
                feedback(sub,body,atch)
            else:
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
                feedback(sub,body,atch)
            else:
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
                feedback(sub,body,atch)
            else:
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
                feedback(sub,body,atch)
            else:
                feedback(sub,body)

        elif x=="5":
            print("Alright, come back again when you have something to say!")
        else:
            print("Invalid Input! Please try again!")

#------------------------------------------------------------------------------------------------------------


def read():
    service=gmail_authenticate()
    os.chdir(mail_path)
    """
    def search_messages(query):
        result = service.users().messages().list(userId='me',q=query,maxResults=25).execute()
        messages = []
        if 'messages' in result:
            messages.extend(result['messages'])
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
            if 'messages' in result:
                messages.extend(result['messages'])
        return messages
    """

    def list_messages(lblId=['INBOX'], query={'':''}):
        result = service.users().messages().list(userId='me',maxResults=25, q=query, labelIds=lblId).execute()
        messages = []
        if 'messages' in result:
            messages.extend(result['messages'])
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
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

    def parse_parts(parts, folder_name, message):
        if parts:
            for part in parts:
                filename = part.get("filename")
                mimeType = part.get("mimeType")
                body = part.get("body")
                data = body.get("data")
                file_size = body.get("size")
                part_headers = part.get("headers")
                if part.get("parts"):
                    parse_parts(service, part.get("parts"), folder_name, message)
                if mimeType == "text/plain":
                    if data:
                        text = urlsafe_b64decode(data).decode()
                        print(text)
                elif mimeType == "text/html":
                    if not filename:
                        filename = "index.html"
                    filepath = os.path.join(folder_name, filename)
                    print(f"Saving a HTML copy to {os.getcwd()}\\{filepath}")
                    with open(filepath, "wb") as f:
                        f.write(urlsafe_b64decode(data))
                else:
                    for part_header in part_headers:
                        part_header_name = part_header.get("name")
                        part_header_value = part_header.get("value")
                        if part_header_name == "Content-Disposition":
                            if "attachment" in part_header_value:
                                print(f"Saving the attachment file: {filename} size: {get_size_format(file_size)} to {os.getcwd()}\\{folder_name}\\{filename}")
                                attachment_id = body.get("attachmentId")
                                attachment = service.users().messages().attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                                data = attachment.get("data")
                                filepath = os.path.join(folder_name, filename)
                                if data:
                                    with open(filepath, "wb") as f:
                                        f.write(urlsafe_b64decode(data))

    def read_message(message):
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        payload = msg['payload']
        headers = payload.get("headers")
        parts = payload.get("parts")
        cur_folder = os.getcwd()
        folder_name = "email"
        has_subject = False
        if headers:
            for header in headers:
                name = header.get("name")
                value = header.get("value")
                if name.lower() == 'from':
                    print("From:", value)
                if name.lower() == "to":
                    print("To:", value)
                if name.lower() == "subject":
                    has_subject = True
                    folder_name = clean(value)
                    folder_counter = 0
                    while os.path.isdir(folder_name):
                        folder_counter += 1
                        # we have the same folder name, add a number next to it
                        if folder_name[-1].isdigit() and folder_name[-2] == "_":
                            folder_name = f"{folder_name[:-2]}_{folder_counter}"
                        elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                            folder_name = f"{folder_name[:-3]}_{folder_counter}"
                        else:
                            folder_name = f"{folder_name}_{folder_counter}"
                    os.chdir(cur_folder)
                    os.mkdir(folder_name)
                    print("Subject:", value)
                if name.lower() == "date":
                    print("Date:", value)

        if not has_subject:
            if not os.isdir(folder_name):
                os.chdir(cur_folder)
                os.mkdir(folder_name)
        parse_parts(parts, folder_name, message)
        print("="*50)

    
    #results = list_messages()
    #for msg in results:
        read_message(msg)



    def mark_as_read(service, query):
        messages_to_mark = search_messages(query)
        return service.users().messages().batchModify(
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

