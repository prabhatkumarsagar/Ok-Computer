import datetime
import time as samay
try:
    from pac import voice_io

except ModuleNotFoundError:
    import voice_io

def date():
    x = datetime.datetime.now().strftime("%d/%m/%Y")  
    voice_io.show(f"Today's date is {x} (DD/MM/YYYY)")

def time():
    #x=datetime.datetime.now().strftime("%H:%M:%S")    
    localtime = samay.localtime()
    x = samay.strftime("%I:%M:%S %p", localtime)
    voice_io.show(f"The current time is {x}") 

def year():
    x=datetime.datetime.now().strftime("%Y")
    voice_io.show(f"The current year is {x}")

def month():
    x=datetime.datetime.now().strftime("%B")
    voice_io.show(f"The current month is {x}") 

def day():
    x=datetime.datetime.now().strftime("%A")
    voice_io.show(f"Today it is a {x}")
