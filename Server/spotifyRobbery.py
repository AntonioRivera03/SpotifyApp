from selenium import webdriver 
from spotify import Song
import sys
from selenium.webdriver.common.by import By
from time import sleep
import asyncio
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

xpaths = {'usr' : '//*[@id="login-username"]', #username  
          'pwd' : '//*[@id="login-password"]', #password
          'lgn' : '//*[@id="login-button"]', #Login button
          'wbp' : '//*[@id="root"]/div/div[2]/div/div/button[2]', #WebPlayer button
          'ttl' : '//*[@id="main"]/div/div[2]/div[2]/footer/div[1]/div[1]/div/div[2]/div[1]/div/div/div/div/span/a', #Song Title
          'art' : '//*[@id="main"]/div/div[2]/div[2]/footer/div[1]/div[1]/div/div[2]/div[3]/div/div/div/div', #Artist
          'pst' : '//*[@id="main"]/div/div[2]/div[2]/footer/div[1]/div[2]/div/div[1]/button',  #PlayState
          'tim' : '//*[@id="main"]/div/div[2]/div[2]/footer/div[1]/div[2]/div/div[2]/div[1]',  #Current time in song
          'dur' : '//*[@id="main"]/div/div[2]/div[2]/footer/div[1]/div[2]/div/div[2]/div[3]' #Duration
          }

caps = DesiredCapabilities.CHROME

caps['goog:loggingPrefs'] = {'performance': 'ALL'}


driver = webdriver.Chrome()

def main():
    login() #Logs in and starts redirect to spotify webplayer

    redirect() #Waits for redirect so that spotify webplayer can load

    monitor()


def login():
    username = ""
    driver.implicitly_wait(.5)

    driver.get("https://accounts.spotify.com/en/login")

    print("Waiting for load..")
    sleep(3)

    driver.find_element(By.XPATH, xpaths['usr']).send_keys(username)
    driver.find_element(By.XPATH, xpaths['pwd']).send_keys('<password>')
    driver.find_element(By.XPATH, xpaths['lgn']).click()

    print(f"LOGGED IN AS {username}..")
    sleep(1)
    driver.find_element(By.XPATH, xpaths['wbp']).click()
    pass

def monitor():
    title = driver.find_element(By.XPATH, xpaths['ttl']).text
    playstate = driver.find_element(By.XPATH, xpaths['pst']).get_attribute('aria-label')
    artist = driver.find_element(By.XPATH, xpaths['art']).text
    duration = driver.find_element(By.XPATH, xpaths['dur']).text

    playstateHash = {"Play": "Paused", "Pause" : "Playing"}
    uptime = 0

    imgPrefix = 'https://i.scdn.co/image/'

    song = Song(song=title, playstate=playstate, artist=artist)
    img = ''
    while(True):
        sleep(1)
        uptime += 1
        curTime = driver.find_element(By.XPATH, xpaths['tim']).text
        
        if checkSong(song):
            
            song.song = driver.find_element(By.XPATH, xpaths['ttl']).text
            song.artist = driver.find_element(By.XPATH, xpaths['art']).text
            duration = driver.find_element(By.XPATH, xpaths['dur']).text
            sys.stdout.write(f"\rSong: {song.song}{' '*(30-len(song.song))}Artist: {song.artist}{' '*(30-len(song.artist))}PlayState: {playstateHash[song.playstate]}{' '*(15-len(song.playstate))}Time Elapsed: {curTime}{' '*(4-len(curTime))} / {duration}           ")
            sys.stdout.flush()

            sleep(1)
            browser_log = driver.get_log('performance') 

            events = [process_browser_log_entry(entry) for entry in browser_log]
            events = [event for event in events if 'Network.response' in event['method']]
            
            
            for x in events:
                try:
                    if x['params']['type'] == 'Fetch':
                        tpe = x['params']['type']
                        if 'https://spclient.wg.spotify.com/metadata/4/track' in x['params']['response']['url'] :
                            
                            try:
                                dataJson = json.loads(driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': x["params"]["requestId"]})['body'])
                                if dataJson['name'] == song.song:
                                    img = dataJson['album']['cover_group']['image'][2]['file_id']
                                    #Something like, if response[title] is == to song.song, update image and break
                                    break
                            except Exception as e:
                                a = e
                                nothing()  
                            

                except Exception as e:
                    pass
                 

            #print(f"Song Changed -> {song.song}")

        elif checkPst(song):
            song.playstate = driver.find_element(By.XPATH, xpaths['pst']).get_attribute('aria-label')

            sys.stdout.write(f"\rSong: {song.song}{' '*(30-len(song.song))}Artist: {song.artist}{' '*(30-len(song.artist))}PlayState: {playstateHash[song.playstate]}{' '*(15-len(song.playstate))}Time Elapsed: {curTime}{' '*(4-len(curTime))} / {duration}            ")
            sys.stdout.flush()
        else:
            sys.stdout.write(f"\rSong: {song.song}{' '*(30-len(song.song))}Artist: {song.artist}{' '*(30-len(song.artist))}PlayState: {playstateHash[song.playstate]}{' '*(15-len(song.playstate))}Time Elapsed: {curTime}{' '*(4-len(curTime))} / {duration}            ")
            sys.stdout.flush()






def nothing():
    pass













def checkSong(song):
    try:
        return song.song != driver.find_element(By.XPATH, xpaths['ttl']).text
    except:
        return True

def checkPst(song):
    try:
        return song.playstate != driver.find_element(By.XPATH, xpaths['pst']).get_attribute('aria-label')
    except:
        return True




def redirect():
    countdown = 7
    sys.stdout.write(f"\rRedirecting to webplayer in : {countdown}<        >")
    sys.stdout.flush()
    for i in range(8):
        
        sys.stdout.write(f"\rRedirecting to webplayer in : {countdown} <{'='*i}")
        sys.stdout.flush()
        countdown -= 1
        sleep(1)
    sys.stdout.flush()
    sys.stdout.write("\r                                ..REDIRECTING..                                \n")
    sys.stdout.flush()
    


def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

if __name__ == '__main__':
    main()