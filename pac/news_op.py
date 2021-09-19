import requests
import webbrowser
from iso3166 import countries
import time
import geocoder
import json
import os
from pathlib import Path
cwd=Path(__file__).parent


try:
    from pac import voice_io,invoice,clear

except ModuleNotFoundError:
    import voice_io,invoice,clear

g = geocoder.ip('me')
cnt=(g.country)

with open(f"{cwd}\creds.json", "r") as f:
     data = json.load(f)
api=data['apis'][2]['newsapi']

def cnt_iso3166(country):
    c=countries.get(country)
    return c[1]

cnt_code = cnt_iso3166(cnt)
#voice_io.show(cnt_code)

def headlines(cnt=cnt_code,catg='general'):
    url = ('https://newsapi.org/v2/top-headlines?'
        f'country={cnt}&'
        f'category={catg}&'
        f'apiKey={api}')
    #voice_io.show(url)
    response = requests.get(url)
    r=response.json()
    try:
        items=[]
        for i in r['articles']:
            item=(i['title'],i['description'],i['url'])
            items.append(item)

        if len(items)==0:
            voice_io.show("Sorry I couldn't find anything like that! Maybe you didn't specify it properly or maybe there just isn't anything regarding that right now, so try again later, maybe!?")

        else:
            for i in range(len(items)):
                clear.clear()
                voice_io.show(f'[{i+1}]',items[i][0])
                time.sleep(1)
                voice_io.show("\nWhat would you like to do? \n1. Expand this headline and read a little more about it. \n2. Open this news piece in your browser. \n3. Skip to the next headline. \n4. Print all news headlines at once. \n5. Go back.")
                ch=invoice.inpt("Enter Choice: ")
                if ch=='1':
                    voice_io.show(items[i][1])
                    time.sleep(3)
                    ch1=invoice.inpt("\nWould you like to know about this some more? I could open this up in your browser! (Y/N): ")
                    if ch1.lower()=='y':
                        voice_io.show("Here you go!\n")
                        webbrowser.open(items[i][2])
                    elif ch1.lower()=='n':
                        voice_io.show("Okay! Onto the next one! \n")
                    else:
                        voice_io.show("Invalid Input!")

                
                elif ch=='2':
                    voice_io.show("Here you go!")
                    webbrowser.open(items[i][2])
                    invoice.inpt("Press Enter to continue to the next story!")
                    continue

                elif ch=='3':
                    continue

                elif ch=='4':
                    while True:
                        clear.clear()
                        voice_io.show("Here you go!\n")
                        for j in range(len(items)):
                            voice_io.show(f'[{j+1}]',items[j][0])
                        time.sleep(3)
                        voice_io.show("\nWhat would you like to do now? \n1. Expand a specific headline and read a little more about it. \n2. Open a specific headline in your browser. \n3. Go back.")
                        ch2=invoice.inpt("Enter Choice: ")
                        if ch2=='1':
                            inp=int(invoice.inpt("Enter the index of the news headline you'd like to know more about: "))
                            voice_io.show(items[inp-1][0])
                            time.sleep(3)
                            ch3=invoice.inpt("\nWould you like to know about this some more? I could open this up in your browser! (Y/N): ")
                            if ch3.lower()=='y':
                                #voice_io.show("Here you go!\n")
                                webbrowser.open(items[inp-1][2])
                                continue
                            elif ch3.lower()=='n':
                                ch3=invoice.inpt("\nDo you want to go back and read more news? (Y/N): ")
                                if ch3.lower()=='y':
                                    continue
                                else:
                                    return
                            else:
                                voice_io.show("Invalid Input!")
                            time.sleep(5)
                            

                        elif ch2=='2':
                            inp=int(invoice.inpt("Enter the index of the news headline you'd like to open up in your browser: "))
                            voice_io.show("Here you go!")
                            webbrowser.open(items[inp-1][2])
                            ch3=invoice.inpt("\nDo you want to go back and read more news? (Y/N): ")
                            if ch3.lower()=='y':
                                continue
                            else:
                                return

                        elif ch2=='3':
                            return

                        else:
                            voice_io.show("Invalid Input!")

                elif ch=='5':
                    return

                else:
                    voice_io.show('Invalid Input!')

    except KeyError:
        voice_io.show("Uh-oh! Looks like i ran into some error doing that! You sure everything's alright? Why not try again later!?")

#headlines(cnt_code)

def search_news():
    clear.clear()
    voice_io.show("\nFor advanced news search please fill in the following (Note - Those fields with an asterisk before their names are optional and so are those with a default something specified, please leave them empty if you don't intend to use them!)")
    qry=invoice.inpt("""\nKeywords or phrases to search for in the news articles (Note - Surround phrases with quotes ('/\") for exact matches, 
Prepend words or phrases that must appear with a + symbol. Eg: +bitcoin, Prepend words that must not appear with a - symbol. Eg: -bitcoin. 
Alternatively you can use the AND / OR / NOT keywords, and optionally group these with parenthesis. Eg: crypto AND (ethereum OR litecoin) NOT bitcoin.): """)
    params={'q':qry}
    sort=input("Sort By ['relevancy', 'popularity', 'publishedAt'] (default is 'publishedAt', it is for the newest articles first): ")
    sort=sort.lower()
    if sort not in ['relevancy','popularity','publishedAt']:
        sort='publishedAt'
    params['sortBy']=sort
    catg=input("Category of the news articles ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology'] (default is 'general'): ")
    catg=catg.lower()
    if catg not in ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']:
        catg='general'
    params['category']=catg
    cnt=input("Country you want the articles to be about (default is your set location): ")
    if cnt=='':
        cnt=cnt_code
        params['country']=cnt
    else:
        cnt=cnt_iso3166(cnt)
        params['country']=cnt    
    incldom=input("*Include Domains (A comma-seperated string of domains (eg bbc.co.uk, techcrunch.com, engadget.com) to restrict the search to): ")
    if incldom!='':
        params['domains']=incldom
    excldom=input("*Exclude Domains (A comma-seperated string of domains (eg bbc.co.uk, techcrunch.com, engadget.com) to remove from the results.): ")
    if excldom!='':
        params['excludeDomains']=excldom
    frm=input("*Date and optional time for the oldest article (e.g. 2021-09-02 or 2021-09-02T03:29:09): ")
    if frm!='':
        params['from']=frm
    to=input("*Date and optional time for the newest article (e.g. 2021-09-02 or 2021-09-02T03:29:09): ")
    if to!='':
        params['to']=to
    
    url = 'https://newsapi.org/v2/top-headlines?'
    for i in params.keys():
        s=f'{i}={params[i]}&'
        url+=s
    url+=f"apiKey={api}"
    voice_io.show(url)
    response = requests.get(url)
    r=response.json()

    try:
        items=[]
        for i in r['articles']:
            item=(i['title'],i['description'],i['url'])
            items.append(item)
        
        if len(items)==0:
            voice_io.show("Sorry I couldn't find anything like that! Maybe you didn't specify it properly or maybe there just isn't anything regarding that right now, so try again later, maybe!?")
        
        else: 
            for i in range(len(items)):
                clear.clear()
                voice_io.show(f'[{i+1}]',items[i][0])
                time.sleep(1)
                voice_io.show("\nWhat would you like to do? \n1. Expand this headline and read a little more about it. \n2. Open this news piece in your browser. \n3. Skip to the next headline. \n4. Print all news headlines at once. \n5. Go back.")
                ch=invoice.inpt("Enter Choice: ")
                if ch=='1':
                    voice_io.show(items[i][1])
                    time.sleep(3)
                    ch1=invoice.inpt("\nWould you like to know about this some more? I could open this up in your browser! (Y/N): ")
                    if ch1.lower()=='y':
                        voice_io.show("Here you go!\n")
                        webbrowser.open(items[i][2])
                    elif ch1.lower()=='n':
                        voice_io.show("Okay! Onto the next one! \n")
                    else:
                        voice_io.show("Invalid Input!")

                
                elif ch=='2':
                    voice_io.show("Here you go!")
                    webbrowser.open(items[i][2])
                    invoice.inpt("Press Enter to continue to the next story!")
                    continue

                elif ch=='3':
                    continue

                elif ch=='4':
                    while True:
                        voice_io.show("Here you go!\n")
                        for j in range(len(items)):
                            voice_io.show(f'[{j+1}]',items[j][0])
                        time.sleep(3)
                        voice_io.show("\nWhat would you like to do now? \n1. Expand a specific headline and read a little more about it. \n2. Open a specific headline in your browser. \n3. Go back.")
                        ch2=invoice.inpt("Enter Choice: ")
                        if ch2=='1':
                            inp=int(invoice.inpt("Enter the index of the news headline you'd like to know more about: "))
                            voice_io.show(items[inp-1][0])
                            time.sleep(3)
                            ch3=invoice.inpt("Would you like to know about this some more? I could open this up in your browser! (Y/N): ")
                            if ch3.lower()=='y':
                                #voice_io.show("Here you go!\n")
                                webbrowser.open(items[inp-1][2])
                                invoice.inpt("Press Enter to continue to the next story!")
                                continue
                            elif ch3.lower()=='n':
                                ch3=invoice.inpt("\nDo you want to go back and read more news? (Y/N): ")
                                if ch3.lower()=='y':
                                    continue
                                else:
                                    return
                            else:
                                voice_io.show("Invalid Input!")
                            time.sleep(5)
                            

                        elif ch2=='2':
                            inp=int(invoice.inpt("Enter the index of the news headline you'd like to open up in your browser: "))
                            voice_io.show("Here you go!")
                            webbrowser.open(items[inp-1][2])
                            ch3=invoice.inpt("\nDo you want to go back and read more news? (Y/N): ")
                            if ch3.lower()=='y':
                                continue
                            else:
                                return

                        elif ch2=='3':
                            return

                        else:
                            voice_io.show("Invalid Input!")

                elif ch=='5':
                    return

                else:
                    voice_io.show('Invalid Input!')

    except KeyError:
        voice_io.show("Uh-oh! Looks like i ran into some error doing that! You sure everything's alright? Why not try again later!?")

#search_news()

def main():
    clear.clear()
    voice_io.show("*NOTE: The news feature is still under-development and so it might be prone to errors. Please report any such occurences if you find one! Thanks @Prabhat.\n")
    voice_io.show("Here comes the news boy! Haha How can i help you today? Please Press: ")
    voice_io.show("1. For Today's top headlines.")
    voice_io.show("2. For Top headlines in a category.")
    voice_io.show("3. For Top headlines in another country.")
    voice_io.show("4. To Search for News.")
    voice_io.show("5. To go back.")
    ch=invoice.inpt("Here: ")
    if ch=='1':
        headlines()

    elif ch=='2':
        catg=invoice.inpt("What Category trending news do you want to see? ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']: ")
        if catg not in ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']:
            voice_io.show("I'm not sure if i can do that! Anyway here's the general trending news!")
            headlines()
        else:
            headlines(catg=catg)
        
    elif ch=='3':
        cnt=invoice.inpt("Which Country's trending news do you want to see?: ")
        cnt_code=cnt_iso3166(cnt)
        headlines(cnt=cnt_code)

    elif ch=='4':
        search_news()

    elif ch=='5':
        return

    else:
        voice_io.show("Invalid Input!")