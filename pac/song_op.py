from selenium.webdriver import Chrome;
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 
import time
import os
from inputimeout import inputimeout, TimeoutOccurred


try:
    from pac import (voice_io,invoice,clear,get_dirs)

except ModuleNotFoundError:
    import voice_io,invoice,clear,get_dirs


FT=True

class SongPlayer():
    UpNextVideos={}
    PreviousVideos={}
    def __init__(self):
        self.FirstTrack = True
        self.ForwardBackwardTime = 10
        self.user_agent = '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
        self.options = Options()
        self.options.add_argument(self.user_agent)
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--log-level=3')
        self.Driver = Chrome(get_dirs.CDRIVERPATH,options=self.options)
        self.Driver.maximize_window()
        
    def CheckAD(self):
        try:
            self.Driver.find_element_by_xpath("//*[@id='skip-button:6']/")
            return True
        except:
            return False

    def ListVideos(self):
        print("\nHere's what I found: \n")
        Counter = 1
        Videos=[]
        for i in range(1,6):
            Video = WebDriverWait(self.Driver,5).until(EC.presence_of_element_located((By.XPATH,f'//*[@id="app"]/div[1]/ytm-search/ytm-section-list-renderer/lazy-list/ytm-item-section-renderer/lazy-list/ytm-compact-video-renderer[{i}]/div/div/a/h4')))
            Video=Video.text
            Videos.append(Video)

        for video in Videos:
                print(f'[{Counter}] {video}')
                Counter += 1

    def UpNext(self):
        self.UpNextVideos={}
        Count=1
        for i in range(1,6):
            VideoName=self.Driver.find_element_by_xpath(f'//*[@id="app"]/div[1]/ytm-watch/ytm-single-column-watch-next-results-renderer/ytm-item-section-renderer[2]/lazy-list/ytm-video-with-context-renderer[{i}]/ytm-large-media-item/div/div[2]/div/a/h3')
            VideoLink=self.Driver.find_element_by_xpath(f'//*[@id="app"]/div[1]/ytm-watch/ytm-single-column-watch-next-results-renderer/ytm-item-section-renderer[2]/lazy-list/ytm-video-with-context-renderer[{i}]/ytm-large-media-item/a')
            Name=VideoName.text
            Link=VideoLink.get_attribute('href')
            self.UpNextVideos[Name]=str(Link)
        
        print("\nUp Next: \n")
        for i in self.UpNextVideos.keys():
            print(f'[{Count}] {i}')
            Count+=1

    def VideoPlay(self):
        VideoTitle = self.Driver.title
        VideoTitle = VideoTitle.rstrip('- YouTube')
        VideoLink = self.Driver.current_url
        clear.clear()
        print(f'\nNow Playing {VideoTitle} ')
        Video = self.Driver.find_element_by_xpath('//*[@id="player-container-id"]')
        Video.click()
        time.sleep(0.75)
        Video.click()
        Autoplay = self.Driver.find_element_by_xpath('//*[@id="player-control-overlay"]/div/div[1]/button[1]')
        Autoplay.click()
        self.PreviousVideos[VideoTitle]=VideoLink
        self.UpNext()

    def PlaySong(self,Link):
        self.Driver.get(Link)
        if self.CheckAD():
            try:
                print("Please Wait...")
                AD = WebDriverWait(self.Driver,5).until(EC.presence_of_element_located((By.XPATH),"//*[@id='skip-button:6']/span/button"))
                AD.click()
                self.VideoPlay()
            except:
                print("Please Wait...")
                time.sleep(15)
                self.VideoPlay()
        else:
            self.VideoPlay()


    def Search(self,Song):
        print(f'\nSearching for {Song}! Please Wait... ')
        self.Driver.get(f'https://www.youtube.com/results?search_query={Song}')
        self.Driver.implicitly_wait(5)
        self.ListVideos()

    def SearchPlay(self,ID):
        VideoPlay = self.Driver.find_element_by_xpath(f'//*[@id="app"]/div[1]/ytm-search/ytm-section-list-renderer/lazy-list/ytm-item-section-renderer/lazy-list/ytm-compact-video-renderer[{ID}]/div/div/a')
        VideoPlay=VideoPlay.get_attribute('href')
        self.PlaySong(VideoPlay)

    def Replay(self):
        CurrentVideoUrl = self.Driver.current_url
        self.PlaySong(CurrentVideoUrl)

    def Forward(self):
        self.Driver.execute_script(f'document.getElementsByTagName(\'video\')[0].currentTime += {self.ForwardBackwardTime}')

    def Backward(self):
        self.Driver.execute_script(f'document.getElementsByTagName(\'video\')[0].currentTime -= {self.ForwardBackwardTime}')

    def Pause(self):
        self.Driver.execute_script("document.getElementsByTagName('video')[0].pause()")

    def Play(self):
        self.Driver.execute_script("document.getElementsByTagName('video')[0].play()")

    def Previous(self):
        pass

    def Next(self):
        print("\nUp Next: \n")
        count=1
        for i in self.UpNextVideos.keys():
            print(f'[{count}] {i}')
            count+=1

    def Close(self):
        self.Driver.close()

    def Console(self):
        status="Playing"
        VideoTitle = self.Driver.title
        VideoTitle = VideoTitle.rstrip('- YouTube')
        while True:
            Video = self.Driver.find_element_by_xpath('//*[@id="player-control-overlay"]')
            Action = ActionChains(self.Driver)
            Action.move_to_element_with_offset(Video,75,90).click().perform()
            Elapsed=self.Driver.find_element_by_xpath('//*[@id="player-control-overlay"]/div/div[4]/ytm-time-display/div/span[1]').text
            Duration=self.Driver.find_element_by_xpath('//*[@id="player-control-overlay"]/div/div[4]/ytm-time-display/div/span[3]').text
            TU=Duration.split(':')
            TE=Elapsed.split(':')
            if TU==[''] and TE==['']:
                continue
            else:
                if TU[-1]>='20':
                    TU[-1]=str(int(TU[-1])-10)
                elif TU[-1]>='10' and TU[-1]<='19':
                    TU[-1]='0'+str(int(TU[-1])-10)
                elif TU[-1]>='00' and TU[-1]<='09':
                    TU[-2]=str(int(TU[-2])-1)
                    TU[-1]=str(int(TU[-1])+50)

                if TE>=TU:
                    print("The Track is about to end and here's your queue and what you can do next: \n")
                    count=1
                    for i in self.UpNextVideos.keys():
                        print(f'[{count}] {i}')
                        count+=1
                    UNVnames=list(self.UpNextVideos.keys())
                    UNVlinks=list(self.UpNextVideos.values())
                    print("\n1. Play the next track!")
                    print("2. Play track # from the queue!")
                    print("3. Play this track once again!")
                    print("4. Search for another track!")
                    print("5. Quit Program")
                    ch=input("\nSo what do you wanna do? Enter Choice:  ")
                    if ch=='1':
                        print("\nAlright onto the next one!")
                        time.sleep(3)
                        clear.clear()
                        self.FirstTrack=False
                        self.PlaySong(UNVlinks[0])
                        self.Console()
                    elif ch=='2':
                        ch2=int(input("\nAlright but enter the track number you want to play next. Here: "))
                        time.sleep(3)
                        clear.clear()
                        self.FirstTrack=False
                        self.PlaySong(UNVlinks[ch2-1])
                        self.Console()
                    elif ch=='3':
                        print("Alrighty!")
                        time.sleep(3)
                        clear.clear()
                        self.Replay()
                        self.Console()
                    elif ch=='4':
                        clear.clear()
                        main()
                    elif ch=='5':
                        self.Close()
                        return
                    else:
                        print("Invalid Input!")

                else:
                    if status=='Playing':
                        x1='pause'
                        x2='pause the track'
                    elif status=='Paused':
                        x1='play'
                        x2='resume the track'
                    message=f"""

Currently {status} - {VideoTitle}

Here are the choices/commands to interact with the track:
1 / {x1} - {x2}
2 / stop - stop the track, search for something else
3 / next - next track
4 / previous - previous track (not available if this is your first track)
5 / forward - skip 10 seconds forward
6 / backward - skip 10 seconds backward
7 / quit - quit the song

                    """
                    print(message)
                    try:
                        inp=inputimeout("Enter choice/command - ", timeout=5)
                        if inp=='1' and status=='Playing' or inp.lower()=='pause' and status=='Playing':
                            self.Pause()
                            status="Paused"
                            clear.clear()
                            continue

                        elif inp=='1' and status=='Paused' or inp.lower()=='play' and status=='Paused':
                            self.Play()
                            status="Playing"
                            clear.clear()
                            continue

                        elif inp=='2' or inp.lower()=='stop':
                            self.Pause()
                            main()

                        elif inp=='3' or inp.lower()=='next':
                            count=1
                            for i in self.UpNextVideos.keys():
                                print("\nHere's your queue and what you can do ;) ")
                                print(f'[{count}] {i}')
                                count+=1
                            print("\n1. Play the next track!")
                            print("\n2. Play track # from the queue!")
                            print("\n3. Quit!")
                            UNVnames=list(self.UpNextVideos.keys())
                            UNVlinks=list(self.UpNextVideos.values())
                            ch=input("\nEnter Choice: ")
                            if ch=='1':
                                print("\nAlright onto the next one!")
                                time.sleep(3)
                                self.FirstTrack=False
                                clear.clear()
                                self.PlaySong(UNVlinks[0])
                                self.Console()
                            elif ch=='2':
                                ch2=int(input("\nAlright but enter the track number you want to play next. Here: "))
                                time.sleep(3)
                                clear.clear()
                                self.FirstTrack=False
                                self.PlaySong(UNVlinks[ch2-1])
                                self.Console() 

                            elif ch=='3':
                                self.Close()
                                return

                            else:
                                print("Invalid Input!")

                        elif inp=='4' or inp.lower()=='previous':
                            if self.FirstTrack!=True:
                                clear.clear()
                                print("Here are your previously played song(s) and what you can do with them: \n")
                                count=1
                                PVn=list(self.PreviousVideos.keys())
                                PVn.pop()
                                PVn=PVn[::-1]
                                for i in PVn:
                                    print(f"[{count}] {i}")
                                    count+=1
                                print("\n1. Play the last played track!")
                                print("\n2. Play track #")
                                print("\n3. Quit!")
                                ch=input("\nEnter Choice: ")
                                if ch=='1':
                                    print("\nAlright onto the previous one!")
                                    time.sleep(3)
                                    clear.clear()
                                    self.PlaySong(self.PreviousVideos[PVn[0]])
                                    self.Console()

                                elif ch=='2':
                                    ch2=int(input("\nAlright but please enter the track number. Here: "))
                                    time.sleep(3)
                                    clear.clear()
                                    self.PlaySong(self.PreviousVideos[PVn[ch2-1]])
                                    self.Console() 

                                elif ch=='3':
                                    self.Close()
                                    return

                                else:
                                    print("Invalid Input!")

                            else:
                                print("Hey there aren't any previous tracks since this is your very first track! Maybe try this after having played some!")
                                continue

                                
                        elif inp=='5' or inp.lower()=='forward':
                            self.Forward()
                            continue
                        
                        elif inp=='6' or inp.lower()=='backward':
                            self.Backward()
                            continue
                            
                        elif inp=='7' or inp.lower()=='quit':
                            self.Close()
                            return

                    except TimeoutOccurred:
                        clear.clear()
                        continue



def main(op=''):
    if op=='':
        global FT
        x=SongPlayer()
        clear.clear()
        ft_message="""
Welcome to Kori Songs Player! Please note that this feature is still under development and 
might be prone to errors, which if you happen to encounter please report it to the developers.
"""
        m_message="""{}
What song would you like to play?
        """.format(ft_message if FT==True else "")
        print(m_message)
        try:
            FT=False
            song=input("Please Search Here - ")
            if song!='':
                x.Search(song)  
                songid=input("\nEnter the number of the song that you want me to play? or Press Enter to search for something else: ")
                if songid=='':
                    x.Close()
                    main()

                elif songid <= '5' and songid >= '1':
                    x.SearchPlay(songid)
                    x.Console()

                else:
                    print("Invalid Input! Please Try Again") 
                    main()
            else:
                print("Invalid Input! Please Try Again!")
                main()  

        except Exception as e:
            print("\nAn Error Occurred while trying to do that please try again later and if the problem persists report it to the developers, the following error message.")
            print(e)

    else:
        x=SongPlayer()
        clear.clear()
        try:
            x.Search(op)
            songid=input("\nEnter the number of the song that you want me to play? or Press Enter to search for something else: ")
            if songid=='':
                x.Close()
                main()

            elif songid <= '5' and songid >= '1':
                x.SearchPlay(songid)
                x.Console()

            else:
                print("Invalid Input! Please Try Again") 
                main()

        except Exception as e:
            print("\nAn Error Occurred while trying to do that please try again later and if the problem persists report it to the developers, the following error message.")
            print(e)


#main()
