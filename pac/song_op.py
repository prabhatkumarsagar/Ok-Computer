import re, os, webbrowser

try:
    from pac import voice_io, get_dirs

except ModuleNotFoundError:
    import voice_io, get_dirs
    

def song_offline():
    voice_io.show("Alright, fetching your offline music playlist right away!")
    music_dir = get_dirs.MUSIC
    songs = os.listdir(music_dir)
    voice_io.show(songs)
    random = os.startfile(os.path.join(music_dir, songs[1]))
        
def song_online(query):    
    reg_ex = re.search('play (.+)', query)
    if reg_ex:
        song = reg_ex.group(1)
        url="https://www.youtube.com/results?search_query="
        url1=song.split()
        for i in range(len(url1)):
            url+=url1[i]
            if i!=-1:
                url+="+"
        voice_io.show("Your requested song will now be searched on youtube in your default browser! Make sure to click the first video link to play it. SORRY FOR THE INCONVINIENCE, We're Working on it.")
        webbrowser.open(url)
    else:
        voice_io.show("Uh-oh looks like i can't perform this operation right now, maybe try again later!")
