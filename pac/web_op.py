import re, wikipedia, wolframalpha, webbrowser

try:
    from pac import voice_io

except ModuleNotFoundError:
    import voice_io
    
def wolfy(question):    
    app_id = "AT3YLY-P2L67K557P"
    client = wolframalpha.Client(app_id) 
    res = client.query(question) 
    answer = next(res.results)["subpod"]["plaintext"]
    return answer

def websearch(query):
    query=query.lower()
    if 'what is' in query:
        try:
            voice_io.show(wolfy(query))

        except:
            try:
                voice_io.show('Searching Wikipedia...\n')
                query1 = query.replace("what is ","")
                results = wikipedia.summary(query1)
                voice_io.show("According to Wikipedia,")
                voice_io.show(results)
            except:
                voice_io.show(f"Could not find any results relating to {query1}, \nplease make sure you're entering a valid input!")


    elif 'meaning of' in query:
        try:
            voice_io.show('Searching Wikipedia...')
            query1 = query.replace("meaning of ","")
            results = wikipedia.summary(query1,sentences=1)
            voice_io.show("According to Wikipedia")
            voice_io.show(results)
        except:
            try:
                voice_io.show(wolfy(query))
            except:
                voice_io.show(f"Could not find any results relating to {query1}, \nplease make sure you're entering a valid input!")
    
    elif 'define' in query:
        try:
            voice_io.show('Searching Wikipedia...')
            query1 = query.replace("define ","")
            results = wikipedia.summary(query1,sentences=1)
            voice_io.show("According to Wikipedia")
            voice_io.show(results)
        except:
            try:
                voice_io.show(wolfy(query))
            except:
                voice_io.show(f"Could not find any results relating to {query1}, \nplease make sure you're entering a valid input!")

    elif 'search' in query:
        query = query.replace("search ", "")
        voice_io.show(f"Searching google for '{query}'")
        query = query.replace(" ", "+")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "where is" in query:
        query = query.replace("where is ", "")
        voice_io.show(f"Searching google maps for '{query}'")
        location = query
        voice_io.show("You asked to locate",location,"and here you go!")
        webbrowser.open("https://www.google.nl/maps/place/" + location + "")

    elif "open website" in query:
        reg_ex = re.search('open website (.+)', query)
        if reg_ex:
            domain = reg_ex.group(1)
            url='https://www.'+domain+".com"
            webbrowser.open(url)
            voice_io.show('The website you have requested will now be opened for you.')
        else:
            pass

    elif 'youtube' in query:
        voice_io.show("Alright, opening Youtube right away!\n")
        webbrowser.open("https://www.youtube.com")

    elif 'google' in query:
        voice_io.show("Alright, opening Google right away!\n")
        webbrowser.open("https://www.google.com")

    elif 'instagram' in query:
        voice_io.show("Alright, opening Instagram right away!")
        webbrowser.open("https://www.instagram.com")
    
    elif 'twitter' in query:
        voice_io.show("Alright, opening Twitter right away!")
        webbrowser.open("https://www.twitter.com")
    
    elif 'reddit' in query:
        voice_io.show("Alright, opening Reddit right away!")
        webbrowser.open("https://www.reddit.com")
    
    elif 'facebook' in query:
        voice_io.show("Alright, opening Facebook right away!")
        webbrowser.open("https://www.facebook.com")

    else:
        try:
            voice_io.show(wolfy(query))
        except:
            voice_io.show("Uh-oh! It looks like i ran into some problems, why don't you try again later?")