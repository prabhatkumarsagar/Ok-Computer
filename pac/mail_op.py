import smtplib
import webbrowser

try:
    from pac import voice_io, usr_signup
    
except:
    import voice_io, usr_signup

def sendMail(sndr_mail,sndr_pw,rcpnt,msg_sub,msg_body):
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        try:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(sndr_mail, sndr_pw)
            subject=msg_sub
            body=msg_body
            msg=f'Subject: {subject}\n\n{body}'
            smtp.sendmail(sndr_mail,rcpnt,msg)
            voice_io.show("Email Sent Successfully!")
        except:
            voice_io.show("Uh-oh! It looks like i ran into some trouble doing that, my best guess would be that, either your email credentials don't work, which if is the case then you can always go to the help section and to the user data one and update your email and/or password, or maybe you're just entering a wrong recepient's email, or, and this one is a big OR, \"Less Secure Apps\" is not turned on for your google account!\n")
            y=input("Which if you want i can do it for you now, just enter 'YES' or 'OK' and a webpage will be prompted with an option to turn on \"Less Secure Apps\" for your google account and just by doing that, the program will be good to go! Otherwise enter 'NO' and you can always do it later. (If you've already have that turned on, please ignore this by entering 'NO' and check whether your problem is one of the other potential problems that i've mentioned) \n>>> ")
            if y.lower()=="yes" or y.lower()=="ok" or y.lower()=="okay" or y.lower()=="":
                voice_io.show("Great! Here you go!")
                webbrowser.open("https://myaccount.google.com/lesssecureapps?")
                return
            elif y.lower()=="no" or y.lower()=="nope":
                voice_io.show("Alright then later it is!")
                return


def mail_sender():
    sender=usr_signup.info_out("email")
    sender_pass=usr_signup.info_out("password")
    recepient=input("Enter the recepient's email: ")
    x=input("Will there be a subject in the email? ")
    x_y=["yes","yep","yeas","yeah","yeap"]
    if x.lower() in x_y:
        voice_io.show("Alright, enter the subject of the email then!")
        sub=input("Here: ")
        voice_io.show("and the body!")
        body=input("Here: ")  
    else:
        voice_io.show("Alright then, no subject it is, enter the body of the email though!")
        sub=""
        body=input("Here: ")
    sendMail(sender,sender_pass,recepient,sub,body)

#mail_sender()

def feedback_sender():
    sender=usr_signup.info_out("email")
    sender_pass=usr_signup.info_out("password")
    def pda_feedback(x,y):
        sendMail(sender,sender_pass,["korihelpdesk@gmail.com","sagarprabhatkumar@gmail.com","sagarprabhatkumar13@gmail.com","duttashaan107@gmail.com","duttashaan102@gmail.com"],x,y)
        #sendMail(sender,sender_pass,["sagarprabhatkumar@gmail.com","sagarprabhatkumar13@gmail.com"],x,y)
        return
    while True:
        voice_io.show("\nWhat do you wanna feed-back? xD")
        voice_io.show("1. Report a bug")
        voice_io.show("2. Suggest Improvement")
        voice_io.show("3. Get in touch with the developers")
        voice_io.show("4. Something Else")
        voice_io.show("5. Nothing (Exit)")
        x=input("Enter Choice: ")
        if x=="1":
            subject="Kori Feedback - Bug Report"
            body=input("Please specify the bug you've encountered: ")
            try:
                pda_feedback(subject,body)
            except:
                voice_io.show("Uh-oh! It looks like i ran into some trouble doing that, you mind doing it later?")
                return
        elif x=="2":
            subject="Kori Feedback - Improvements Suggestion"
            body=input("Please explain verbosely what improvement would you like to see in the future updates: ")
            try:
                pda_feedback(subject,body)
            except:
                voice_io.show("Uh-oh! It looks like i ran into some trouble doing that, you mind doing it later?")
                return
        elif x=="3":
            subject="Kori Feedback - User Contact"
            body=input("What would you want to say to my developers: ")
            try:
                pda_feedback(subject,body)
            except:
                voice_io.show("Uh-oh! It looks like i ran into some trouble doing that, you mind doing it later?")
                return
        elif x=="4":
            subject="Kori Feedback - Feedback"
            body=input("What would you like to say: ")
            try:
                pda_feedback(subject,body)
            except:
                voice_io.show("Uh-oh! It looks like i ran into some trouble doing that, you mind doing it later?")
                return
        elif x=="5":
            voice_io.show("Alright, come back again when you have something to say!")
            break
        else:
            voice_io.show("Invalid Input! Please try again!")
            continue
            
#feedback_sender()
