import tabulate
import time as samay
import sqlite3 as sql
from plyer import notification

try:
    from pac import voice_io
    from pac import invoice
    from pac import get_dirs

except ModuleNotFoundError:
    import invoice
    import voice_io
    import get_dirs
    

def time_now():
    t = samay.localtime() 
    time_now = samay.strftime("%Y-%m-%d %H:%M:%S", t)
    return time_now



def note_rem_create():
    con = sql.connect(get_dirs.DB_NOTES_REMINDERS)
    cur = con.cursor()
    cur.execute("create table if not exists notes(date_added date, note longtext);")
    cur.execute("create table if not exists past_reminders(datetime_added date, reminder longtext, datetime_tbn date);")
    cur.execute("create table if not exists future_reminders(datetime_added date, reminder longtext, datetime_tbn date);")
    con.close()

def note_write():
    note_rem_create()
    con = sql.connect(get_dirs.DB_NOTES_REMINDERS)
    cur = con.cursor()
    voice_io.show("Okay so you wanna enter a new note? Here ya go!")
    x1=invoice.inpt("Enter Note Here: ", processed = False)
    cur.execute("insert into notes values(datetime('now', 'localtime'), '%s');"%x1)
    voice_io.show("Note Saved Successfully!")
    con.commit()
    con.close()


def reminder_write():
    note_rem_create()
    con = sql.connect(get_dirs.DB_NOTES_REMINDERS)
    cur = con.cursor()
    x1=invoice.inpt("Enter Reminder: ")
    x2=invoice.inpt("Enter Date to be Notified (YYYY-MM-DD): ")
    x3=input("Enter Time to be Notified (HH:MM:SS): ")
    x4=x2+' '+x3
    datetime_now=time_now()

    if x4<datetime_now:
        prmpt=input("Hey you are entering a reminder for a date and time that has already passed, are you sure you want to continue? ")
        prmpt=prmpt.lower()
        if prmpt in ['yeah','yep','yes', 'ok']:
            voice_io.show("Alright as you wish, master!")
            cur.execute("insert into past_reminders values(datetime('now', 'localtime'), '%s', '%s');"%(x1,x4))
            voice_io.show("Reminder Saved Successfully!")
            con.commit()
        elif prmpt in ['no','nah','nope','not really']:
            voice_io.show("Okay!")
        else:
            voice_io.show("Invalid Input!")
    
    elif x4>datetime_now:
        cur.execute("insert into future_reminders values(datetime('now', 'localtime'), '%s', '%s');"%(x1,x4))
        voice_io.show("Reminder Saved Successfully!")
        con.commit()
        #reminder_remind()
    
    else:
        voice_io.show("An internal error occurred while processing your request, please make sure you've entered the values correctly and try again!")
    
    con.close()


def note_read():
    note_rem_create()
    con = sql.connect(get_dirs.DB_NOTES_REMINDERS)
    cur = con.cursor()
    cur.execute("select rowid, date_added, note from notes;")
    c=cur.fetchall()
    if c==[]:
        voice_io.show("There are no notes to be shown, try making new notes! :)")
    else:
        voice_io.show("Here are all your notes: ")
        print()
        voice_io.show(tabulate.tabulate(c, headers = ["NoteID","Date and Time Added", "Note"]))
        print()
        prmpt=input("Would you like to delete or edit these notes? ")
        prmpt=prmpt.lower()
        if prmpt in ['yeah','yep','yes', 'ok']:
            ch=int(input("\nAnd what do you want to do really? \n1. Edit \n2. Delete \nEnter Choice: "))
            if ch==1:
                noteid=int(input("Please Enter the NoteID of the Note you wanna edit: "))
                newnote=input("Now enter the new updated note: ")
                try:
                    cur.execute("update notes set note='%s' where rowid=%i;"%(newnote,noteid))
                    con.commit()
                    voice_io.show("Note Updated Successfully!")
                except:
                    voice_io.show("Sorry i couldn't process your request at the moment, maybe because you're not entering a valid NoteID or something else, why don't you try again later!?")

            elif ch==2:
                noteid=int(input("Please Enter the NoteID of the Note you wanna delete: "))
                try:
                    cur.execute("delete from notes where rowid=%i;"%(noteid))
                    con.commit()
                    voice_io.show("Note Deleted Successfully!")
                except:
                    voice_io.show("Sorry i couldn't process your request at the moment, maybe because you're not entering a valid NoteID or something else, why don't you try again later!?")

            else:
                voice_io.show("Invalid Input!")

        elif prmpt in ['no','nah','nope','not really']:
            voice_io.show("Alright!")

        else:
            print("Okay!")

    con.close()


def reminder_read():
    note_rem_create()
    con = sql.connect(get_dirs.DB_NOTES_REMINDERS)
    cur = con.cursor()
    voice_io.show("Hey there! Here's where all your reminders are stored! Yes I Know, I Know that i am not notifying you of your set reminders when the date and time comes but that's not a bug you see, my developers are still working on that feature and you'll see it in the near future ;) so just for now you have to keep checking in here to keep up to date with your saved reminders. Sorry again for the inconvienience caused but anyway,")
    voice_io.show("\nWhat reminders do you want to read?")
    voice_io.show("1. Past Reminders")
    voice_io.show("2. Future/Upcoming Reminders")
    cho=input("Enter Choice: ")
    if cho=="1":
        cur.execute("select rowid, datetime_added, reminder, datetime_tbn from past_reminders;")
        c=cur.fetchall()
        if c==[]:
            voice_io.show("Well it looks like you don't have any past reminders. Is that a good thing or a bad thing? Hmmm")

        else:
            voice_io.show("Here are all your past reminders: ")
            print()
            voice_io.show(tabulate.tabulate(c, headers = ["ReminderID","Date and Time Added", "Reminder", "Date and Time to be Notified"]))
            print()

            prmpt=input("Would you like to delete past reminders? ")
            prmpt=prmpt.lower()
            if prmpt in ['yeah','yep','yes', 'ok']:
                remid=input("Please Enter the ReminderID of the Reminder you wanna delete or type 'all' if you want to delete all of them: ")
                if remid.isnumeric()!=True:
                    remid=remid.lower()
                    if remid=='all':
                        cur.execute("delete from past_reminders;")
                        con.commit()
                        voice_io.show("All past reminders deleted successfully!")
                    else:
                        voice_io.show("Invalid Input!")       

                else: 
                    remid=int(remid)
                    try:
                        cur.execute("delete from past_reminders where rowid=%i;"%(remid))
                        con.commit()
                        voice_io.show("Reminder Deleted Successfully!")
                    except:
                        voice_io.show("Sorry i couldn't process your request at the moment, maybe because you're not entering a valid ReminderID or something else, why don't you try again later!?")


            elif prmpt in ['no','nah','nope','not really']:
                voice_io.show("Alright!")

            else:
                print("Okay!")



    elif cho=="2":
        cur.execute("select rowid, datetime_added, reminder, datetime_tbn from future_reminders;")
        c=cur.fetchall()
        if c==[]:
            voice_io.show("Well it looks like you don't have any upcoming reminders. Is that a good thing or a bad thing? Hmmm")

        else:
            voice_io.show("Here are all your upcoming/future reminders: ")
            print()
            voice_io.show(tabulate.tabulate(c, headers = ["ReminderID","Date and Time Added", "Reminder", "Date and Time to be Notified"]))
            print()

            prmpt=input("Would you like to edit or delete these reminders? ")
            prmpt=prmpt.lower()
            if prmpt in ['yeah','yep','yes', 'ok']:
                ch=int(input("\nAnd what do you want to do really? \n1. Edit \n2. Delete \nEnter Choice: "))
                if ch==1:
                    remid=int(input("Please Enter the ReminderID of the Reminder you wanna edit: "))
                    ch2=int(input("And What exactly do you wanna edit? \n1. Reminder Content \n2. Reminder Date and Time \nEnter Choice: "))
                    if ch2==1:
                        newrem=input("Okay Enter the new updated Reminder: ")
                        try:
                            cur.execute("update future_reminders set reminder='%s' where rowid=%i;"%(newrem,remid))
                            con.commit()
                            voice_io.show("Reminder Updated Successfully!")
                        except:
                            voice_io.show("Sorry i couldn't process your request at the moment, maybe because you're not entering a valid NoteID or something else, why don't you try again later!?")

                    elif ch2==2:
                        newdatetime=input("Okay Enter the new Date and Time (YYYY-MM-DD HH:MM:SS): ")
                        try:
                            cur.execute("update future_reminders set datetime_tbn='%s' where rowid=%i;"%(newdatetime,remid))
                            con.commit()
                            voice_io.show("Reminder Updated Successfully!")
                        except:
                            voice_io.show("Sorry i couldn't process your request at the moment, maybe because you're not entering a valid NoteID or something else, why don't you try again later!?")

                    else:
                        voice_io.show("Invalid Input")
                    
                elif ch==2:
                    remid=input("Please Enter the ReminderID of the Reminder you wanna delete or type 'all' if you want to delete all of them: ")
                    if remid.isnumeric()!=True:
                        remid=remid.lower()
                        if remid=='all':
                            cur.execute("delete from future_reminders;")
                            con.commit()
                            voice_io.show("All future reminders deleted successfully!")
                        else:
                            voice_io.show("Invalid Input!")       

                    else: 
                        remid=int(remid)
                        try:
                            cur.execute("delete from future_reminders where rowid=%i;"%(remid))
                            con.commit()
                            voice_io.show("Reminder Deleted Successfully!")
                        except:
                            voice_io.show("Sorry i couldn't process your request at the moment, maybe because you're not entering a valid ReminderID or something else, why don't you try again later!?")


            elif prmpt in ['no','nah','nope','not really']:
                voice_io.show("Alright!")

            else:
                print("Okay!")



    else:
        voice_io.show('Invalid Input!')

    con.close()


def reminder_remind():
    def notify(reminder):
        notification.notify(
            title = "Reminder",
            app_name = "Kori",
            message = reminder,
            timeout=10)

    def time_now():
        t = samay.localtime() 
        time_now = samay.strftime("%Y-%m-%d %H:%M:%S", t)
        return time_now

    while True:
        con = sql.connect(get_dirs.DB_NOTES_REMINDERS)
        cur = con.cursor()
        cur.execute("select datetime_tbn, reminder from future_reminders;")
        c=cur.fetchall()
        d1={}
        for i in c:
            d1[i[0]]=i[1]

        d2={}
        for i in sorted(d1.keys()):
            d2[i]=d1[i]
        if d2=={}:
            #print("No Upcoming Reminders!")
            break
        else:
            print(d2)
            for i in d2.keys():
                if i==time_now():
                    notify(d2[i])
                    cur.execute("delete from future_reminders where datetime_tbn='%s';"%i)
                    cur.execute("insert into past_reminders values(datetime('now','localtime'),'%s','%s');"%(d2[i],i))
                    con.commit()
                elif i<time_now():
                    notify(d2[i])
                    cur.execute("delete from future_reminders where datetime_tbn='%s';"%i)
                    cur.execute("insert into past_reminders values(datetime('now','localtime'),'%s','%s');"%(d2[i],i))
                    con.commit()
                else:
                    samay.sleep(1)
                    continue
        con.close()
