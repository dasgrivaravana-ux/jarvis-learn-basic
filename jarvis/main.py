import webbrowser
import time
import pywhatkit
import os
import pyautogui
import pygetwindow as gw
import urllib.parse
import ollama
import pyttsx3
import shutil
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from datetime import datetime
import winsound
import threading
import requests
import sounddevice as sd
import numpy as np


#---------------present time-------------
def current_time(command):
    if ("present time"in command
        or 'time' in command):
        time=datetime.now().strftime("present time is %I %M %p").lstrip("0")
        speak(time)
        return True
    return False
def name(command):
    if ('name' in command
        or 'what is your name' in command):
        speak('my name is jarvis and i am your personal assistant')
        return True
    return False
#-----------------------------------------

#--------------future plan----------------
def future(command):
    if ('future' in command
        or 'future plan' in command
        or 'goal' in command):
        speak("My future goals are to improve my project by removing the need for typing, making it fully voice-controlled, and connecting it with IoT devices for smart automation.")
        return True        
    return False
#----------------------------------------

#-----------speak-----------------------
def speak(text):
    print("🤖 Jarvis:", text)
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate',180)
        engine.setProperty('volume',1.0)
        engine.say(str(text))
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"Speech error: {e}")
speak("Hello boss, checking all machines are ready and running perfectly...")
#---------------------------------------

#---------------browser target----------
def browser():
    browsers = ['chrome', 'edge', 'safari', 'firefox']

    for browser_name in browsers:
        windows = gw.getWindowsWithTitle(browser_name)

        if windows:
            win = windows[0]
            if win.isMinimized:
                win.restore()
                time.sleep(0.3)
            try:
                win.activate()
            except:
                pass
            time.sleep(0.3)
            return True
    return False
#-----------------------------------------------

#------------------work-----------------------
def work(command):
    if 'what will you do' in command or 'how much will you do' in command:
        speak(
"I can check the time, send whatsapp messages, open websites, "
"scroll Instagram reels, solve questions, play videos or songs, "
"adjust brightness and volume, create and delete folders, "
"open MyCamu, lock the screen, set alarms, and even shut down the computer. read news"
)
        return True   
    return False
#---------------------------------------------

#----------------alarm------------------------
def alarm(command):

    if 'set alarm' in command or 'alarm ' in command:
        alarm_time = command.replace('set alarm at', '').strip()

        try:
            alarm_time = datetime.strptime(
                alarm_time, "%H:%M"
            ).strftime("%I:%M %p")

        except ValueError:
            try:
                alarm_time = datetime.strptime(
                    alarm_time, "%I:%M %p"
                ).strftime("%I:%M %p")

            except ValueError:
                speak("Give me command like: set alarm at 06:51 PM")
                return True

        speak("Alarm set for " + alarm_time)

        threading.Thread(
            target=ring_alarm,
            args=(alarm_time,),
            daemon=True
        ).start()

        return True

    return False

def ring_alarm(alarm_time):
    while True:
        current_time = datetime.now().strftime("%I:%M %p")
        if current_time == alarm_time:
            end_time = time.time() + 10
            while time.time() < end_time:
                winsound.Beep(1000, 1000)
                time.sleep(0.2)
            print("Alarm stopped")
            break
        time.sleep(1)
#--------------------------------------------
        
#------------instgaram profile---------------
def instagram(command):
    command = command.strip().lower()
    if command.startswith("profile"):
        name = command.replace("profile", "", 1).strip()
        if not name:
            speak("Please provide an Instagram username.")
            return True
        speak(f" Searching Instagram profile {name}")
        username = urllib.parse.quote(name)
        url = f"https://www.instagram.com/{username}/"
        webbrowser.open(url)
        time.sleep(5)
        speak(f"Opened Instagram profile {name}")
        return True
    return False
#-----------------------------------------

#--------instagram scroll------------------
def instagram_scroll(command):
    command = command.lower().strip()
    if (
        "scroll instagram" in command
        or "instagram scroll" in command
        or "instagram auto scroll" in command
        or command == "scroll"
    ):
        speak("Opening Instagram Reels...")
        webbrowser.open("https://www.instagram.com/reels/")
        time.sleep(8)
        speak("Instagram auto-scroll started...")
        speak("Scrolling reels...")
        for i in range(10):
            pyautogui.scroll(-4)
            speak(f"Scrolling {i + 1} of 10")
            time.sleep(15)
        speak("Auto-scroll finished.")
        pyautogui.hotkey('ctrl','w')
        return True
    return False
#----------------------------------------------

#--------------web browser--------------------
def web(command):
    urls = {
        "open youtube": ("YouTube", "https://www.youtube.com"),
        "open google": ("Google", "https://www.google.com"),
        "open instagram": ("Instagram", "https://www.instagram.com"),
        "open whatsapp": ("WhatsApp", "https://web.whatsapp.com"),
        "open chrome": ("Chrome", "https://www.google.com/chrome/"),
        "open chatgpt": ("ChatGPT", "https://chatgpt.com"),
        "open gemini": ("Gemini", "https://gemini.google.com"),
        "open github": ('Github',"https://github.com/")
    }
    if command in urls:
        name, url = urls[command]
        speak(f"Opening {name}")
        webbrowser.open(url)
        return True
    return False
#--------------------------------------------

#---------------chatgpt----------------------
# ----------------- CHATGPT -----------------
def chatgpt(command):
    if command == "chatgpt":
        speak("Opening ChatGPT...")
        webbrowser.open("https://chatgpt.com/")
        return True

    if command.startswith("chatgpt "):
        question = command.replace("chatgpt ", "", 1).strip()

        speak("Opening ChatGPT...")
        webbrowser.open("https://chatgpt.com/")
        time.sleep(6)

        pyautogui.write(question, interval=0.03)
        pyautogui.press("enter")
        return True
    return False
# -------------------------------------------

#----------------------------------------------

#-----------------camu------------------------
def camu(command):
    if command.startswith("mycamu"):
        speak("Opening mycamu profile")
        webbrowser.open("https://www.students.nivambu.asia/v2/profile")
        return True
    return False

def attend(command):
    if command.startswith("open attendence"):
        speak("Opening attendance in MyCAMU")
        webbrowser.open("https://www.students.nivambu.asia/v2/attendance")
        return True
    return False
#--------------------------------------------------

#---------------gemini-----------------------------
def gemini(command):
    if command == "gemini":
        speak("Opening Gemini...")
        webbrowser.open("https://gemini.google.com/")
        return True

    if command.startswith("gemini "):
        question = command.replace("gemini ", "", 1).strip()
        if not question:
            speak("Please tell me what you want to search.")
            return True
        speak("Opening Gemini...")
        webbrowser.open("https://gemini.google.com/")
        time.sleep(7)
        pyautogui.click(600, 700)
        time.sleep(1)
        pyautogui.write(question, interval=0.03)
        time.sleep(1)
        pyautogui.press("enter")
        speak("Question sent to Gemini.")
        return True
    return False
#-----------------------------------------------------

#-----------------chrome-----------------------------
def chrome(command):
    if command.startswith("chrome"):
        search = command.replace("chrome", "", 1).strip()
        if not search:
            speak("Please provide something to search.")
            return True
        speak("Searching...")
        pywhatkit.search(search)
        return True

    elif command in [
        "open private browsing",
        "private browsing",
        "private"
    ]:
        browser()
        speak("Opening private browsing...")
        pyautogui.hotkey("ctrl", "shift", "n")
        return True
    elif command in [
        "close tab",
        "close"
    ]:
        browser()
        speak("Closing tab...")
        pyautogui.hotkey("ctrl", "w")
        return True
    return False
#---------------------------------------------------

#--------------whatsapp-----------------------------
def whatsapp(command):
    if command.startswith("send message") or command.startswith("send whatsapp message"):

        data = command.replace("send whatsapp message", "", 1)
        data = data.replace("send message", "", 1).strip()

        try:
            if not data.startswith("to "):
                speak("Please say: send message to phone number and message")
                return True

            data = data.replace("to ", "", 1).strip()

            phone, message = data.split(" ", 1)

            if not phone.startswith("+"):
                phone = "+91" + phone

            print("Phone:", phone)
            print("Message:", message)

            speak("Opening WhatsApp")
            pywhatkit.sendwhatmsg_instantly(
                phone,
                message,
                wait_time=15,
                tab_close=True
            )
            speak("Message sent successfully.")
            return True
        except ValueError:
            speak("Please provide the phone number and message.")
            return True
        except Exception as e:
            print("WhatsApp error:", e)
            speak("There was an error sending the WhatsApp message.")
            return True

    return False
#----------------------------------------------------------

#--------------------youtube------------------------------
def vide(command):
    global yt
    if command.startswith("play"):
        songs = command.replace("play", "", 1).strip()
        if not songs:
            speak("boss,  i cant understand Please tell me what to play.")
            return True
        speak(f"Playing {songs} on youtube")
        pywhatkit.playonyt(songs)
        yt = True
        time.sleep(4)
        return True

    elif command in ["start video","start","start song"]:
        browser()
        pyautogui.press("k")
        speak("Play video")
        return True

    elif command in ["stop","stop video","stop song"]:
        browser()
        pyautogui.press('k')
        speak('stop video')
        return True

    elif command in ["close tab","close video"]:
        browser()
        pyautogui.hotkey("ctrl", "w")

        speak("Closing tab...")
        return True

    elif command in ["previous video","play previous","previous"]:
        browser()
        pyautogui.hotkey("shift", "p")
        speak("Playing previous video")
        return True
    elif command in ["next video","next","next song","play next video","play next song"]:
        browser()
        pyautogui.hotkey("shift", "n")
        speak("Playing next video")
        return True

    elif command in["full screen",'full']:
        browser()
        pyautogui.hotkey('f')
        speak("full screen ")
        return True

    return False
#--------------------------------------------------------

#-------------------folder-----------------------------
def folder(command):
    arr = ["create folder","folder"]
    name = ""
    matched = False
    for item in arr:
        if command.startswith(item):
            name = command.replace(item, "", 1).strip()
            matched = True
            break

    if matched:
        if not name:
            speak("Please specify a folder name.")
            return True
        if os.path.exists(name):
            speak("📁 Folder already exists.")
            return True
        speak("📁 Creating folder")
        os.makedirs(name, exist_ok=True)
        speak(f"📁 folder created by name {name}")
        return True
    return False

def delete_folder(command):
    if command.startswith("delete folder"):
        folder_name = command.replace("delete folder", "").strip()

        if (os.path.exists(folder_name) and os.path.isdir(folder_name)):
            shutil.rmtree(folder_name)
            speak(f" folder deleted by name {folder_name}")
            return True
        else:
            speak(f"folder does not exist by name {folder_name}")
            return True
    return False
#-------------------------------------------------------------

#---------------------ollama------------------------------
def ai_command(command):
    if ("ollama" in command or "explain" in command):
        question = command.replace("ollama", "").replace("explain", "").replace("ask", "").strip()

        if question:
            try:
                response = ollama.chat(
                    model="llama3.2",
                    messages=[
                        {
                            "role": "system",
                            "content": "you are jarvis, a patient socratic tutor.Your goal is to help the user understand a topic throughly and giving example,After answering a question,ask a follow-up question to check their understanding and guide them to think deeper.Wait for user response before moving on."
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ],
                    options={
                        "num_predict": 100,
                        "temperature": 0.3
                    }
                )

                answer = response["message"]["content"]

                answer = answer.replace("**", "")
                answer = answer.replace("*", "")
                answer = answer.replace("#", "")

                speak(answer)
                return True

            except Exception as e:
                speak(f"Ollama error: {e}")
                return True

    return False
#-------------------------------------------------------

#---------------------------brightness------------------
def brightness(command):
    command = command.lower().strip()

    if "increase brightness" in command:
        try:
            value = int(command.replace("increase brightness", "", 1).strip())
            current = sbc.get_brightness()[0]
            new = min(100, current + value)
            sbc.set_brightness(new)
            speak(f"Brightness increased to {new} percent")
            print(f"☀️ Brightness increased to {new}%")
        except ValueError:
            speak("Please provide a number. Example: increase brightness 50")
        except Exception as e:
            speak(f"Brightness error: {e}")
        return True

    elif "decrease brightness" in command:
        try:
            value = int(command.replace("decrease brightness", "", 1).strip())
            current = sbc.get_brightness()[0]
            new = max(0, current - value)
            sbc.set_brightness(new)
            speak(f"Brightness decreased to {new} percent")
            print(f"☀️ Brightness decreased to {new}%")
        except ValueError:
            speak("Please provide a number. Example: decrease brightness 20")
        except Exception as e:
            speak(f"Brightness error: {e}")
        return True
    return False
#----------------------------------------------------------

#-------------lock screen--------------------------------
def lock(command):
    if ('lock' in command):
       speak("Locking your computer")
       os.system("rundll32.exe user32.dll,LockWorkStation")
       return True
    return False

def shutdown_pc(command):
    if "shutdown" in command or "shut down" in command:
        speak("Shutting down the computer")
        os.system("shutdown /s /t 5")
        return True

    return False
#------------------------------------------------

#--------------news------------------------
def news(command):
    if "news" in command:
        API_KEY = "2fc7a506b4924753b591e1323b74b8e2"
        url = "https://newsapi.org/v2/everything"
        params = {
     "q": "India",
     "language": "en",
     "sortBy": "publishedAt",
    "apiKey": API_KEY,
    "pageSize": 5
     }
        try:
            response = requests.get(url, params=params)
            print("STATUS:", response.status_code)
            data = response.json()
            if data["status"] != "ok":
                print("ERROR:", data)
                speak("Sorry, I could not get the news.")
                return True
            articles = data["articles"]
            if len(articles) == 0:
                speak("No news was found.")
                return True
            speak("Here are the latest news headlines.")
            for article in articles:
                title = article["title"]
                print("📰", title)
                speak(title)
            return True
        except Exception as e:
            print("NEWS ERROR:", e)
            speak("There was an error getting the news.")
            return True
    return False
#-----------------------------------------------

#----------------volume--------------------------
def get_volume_control():
    devices = AudioUtilities.GetSpeakers()
    return devices.EndpointVolume

def volume(command):
    command = command.lower().strip()
    if "volume" not in command:
        return False

    try:
        volume_control = get_volume_control()
        current = int(volume_control.GetMasterVolumeLevelScalar() * 100)
        if ("increase volume" in command or "up volume" in command):
            try:
                value = int(command.split()[-1])
            except ValueError:
                speak("Please say a number. Example: increase volume 20")
                return True

            new_value = min(
                100,
                current + value
            )
            volume_control.SetMasterVolumeLevelScalar(
                new_value / 100,
                None
            )
            speak(f"Volume increased to {new_value} percent")
            print(f"🎵 Current volume: {new_value}%")
            return True
        elif ("decrease volume" in command or "down volume" in command):
            try:
                value = int(command.split()[-1])
            except ValueError:
                speak("Please say a number. Example: decrease volume 20")
                return True

            new_value = max(
                0,
                current - value
            )
            volume_control.SetMasterVolumeLevelScalar(
                new_value / 100,
                None
            )
            speak(f"Volume decreased to {new_value} percent")
            print(f"🎵 Current volume: {new_value}%")
            return True
        else:
            speak("not understand Example: increase volume 20 like this")
            return True
    except Exception as e:
        speak(f"Volume error: {e}")
        return True
    return False
#------------------------------------------------------------        

while True:
    try:
        command = input("\n👤 Enter command here: ").strip().lower()

        if "exit" in command or "bye" in command:
            speak("jarvis is Shutting down. Thank you for using me")
            print("❌ Exiting program... bye")
            break
        if vide(command):
            continue
        if web(command):
            continue
        if folder(command):
            continue
        if whatsapp(command):
            continue
        if chrome(command):
            continue
        if chatgpt(command):
            continue
        if gemini(command):
            continue
        if instagram_scroll(command):
            continue
        if instagram(command):
            continue
        if ai_command(command):
            continue
        if camu(command):
            continue
        if attend(command):
            continue
        if delete_folder(command):
            continue
        if brightness(command):
            continue
        if volume(command):
            continue
        if current_time(command):
            continue
        if work(command):
            continue
        if name(command):
            continue
        if future(command):
            continue
        if lock(command):
            continue
        if shutdown_pc(command):
            continue
        if alarm(command):
            continue
        if news(command):
            continue

#----------------------------------------------
        speak("Sorry boss, I did not understand that command.")
    except KeyboardInterrupt:
        speak("Emergency shutdown triggered. Goodbye!   ")
        print("Emergency shutdown triggered. Goodbye!")
        break