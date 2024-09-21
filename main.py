import cv2
import numpy as np
import os
from Alpha import AlphaAssistant
import re
from Alpha.features.LoginRegGUI import LoginWindow
import random
import csv
from Alpha.aitalks.Brain import generate_response
from Alpha.features.loc import find_location_and_distance as loc
import datetime
import requests
from PIL import Image    
from time import sleep
import sys 
import time
import pyautogui
import subprocess
import webbrowser
from Alpha.features.close import close
from bs4 import BeautifulSoup
import pywhatkit
import wolframalpha
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Alpha.features.gui import Ui_MainWindow
from Alpha.features.message import messages
from Alpha.config import config
from Alpha.features.News import latestNews
from Alpha.features.Listen import takecommand


obj = AlphaAssistant()

# ================================ MEMORY ===========================================================================================================

GREETINGS = ["hello Alpha", "Alpha", "wake up Alpha", "you there Alpha", "time to work Alpha", "hey Alpha",
             "ok Alpha", "are you there"]
GREETINGS_RES = ["always there for you sir", "i am ready sir",
                 "your wish my query", "how can i help you sir?", "i am online and ready sir"]

CONTACTS={"mom":"9873007432", "dad":"9999757862","utkrisht":"7042190090","shreyansh":"7487852929","rahuljain":"7982434689","bhargvi":"8130057784","krishnaditya":"8178591113","srishti":"8368179705","shalinimam":"8527061661","soumil":"8527461177","satyam":"8766224264","anisha":"8920289719","sanya":"9310539510","akalpmishra":"9354945823","omeetsir":"9528886877","eshaan":"8920512631","harsh":"9818175124","stutee":"9818279299","rashmima'am":"9871373739","aditya":"9891956161","vikassir":"9315770001","pizzarelation":"8800889753","shresthsinghal":"7827798412","mehtab":"7530905801","aman":"9899177921","cAbdriver":"7982500625","saksham":"8887541530","himanshubhaiya":"7905075869","nirupmadi":"9794431101","nishank":"8799731973","ankur":"9315062734","aditya9g":"9205617627","anurag":"9354731750","ashishsir":"9971847685","akansha":"9315781782","ishita":"9716247207","mohnish":"9955771990","abhinavsaini":"9718189622","rahulsir":"9891674718","ainesh":"9910578575","shayan":"9971178731","anushkarana":"9870353559","saumya":"8882627326","vansh":"9971170520","himanshu":"9310057810","anuja":"8882582199","kshitij":"9911462392","diksha":"9289217383","ishaankumar":"8700199128","bpsir":"9811468156","janvidi":"9559715075","kanik":"7428926813","soumilclassmate":"8527461177","javedsir":"9828916967","deepalimam":"8586977069","neelammam":"9873212804","ishanupadhyay":"7678155706","siddhi":"8595868262","krishna":"8882938086","harry":"7408232595"}
CALENDAR_STRS= ["what do i have", "do i have plans", "am i busy"]
# =======================================================================================================================================================
history=[]
def speak(text):
    print("Alpha : ", text)
    print("")
    obj.tts(text)
def onlyspeak(text):
    obj.tts(text)
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {"Authorization": "Bearer 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"}

def query_img(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

app_id = config.wolframalpha_id

def computational_intelligence(question):
    try:
        client = wolframalpha.Client(app_id)
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except:
        speak("Sorry sir I couldn't fetch your question's answer. Please try again ")
        data = "Sorry sir I couldn't fetch your question's answer. Please try again "
        return data 
    
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning")
    elif hour>12 and hour<18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    c_time = obj.tell_time()
    speak(f"Currently it is {c_time}")
    speak("I am Alpha. Online and ready sir.")

def chat_generation(user_input):
    response = generate_response(user_input)
    return response

def chat_interaction(user_input):
    with open("Alpha\\aitalks\\all_responses.txt", "a", encoding="utf-8") as file:
        while True:

            if user_input == 'exit' or user_input == 'quit':
                break
            else:
                response = chat_generation(user_input)
                file.write(f"User Input: {user_input}\n")
                file.write(f"Response: {response}\n\n")  
                file.flush() 
                return response

def call(person):
    global CONTACTS
    if person in CONTACTS : 
        ph_no= CONTACTS[person] 
        command1='adb shell am start -a android.intent.action.CALL -d tel:+91'+ph_no
        time.sleep(2)   
        pyautogui.press("super")
        time.sleep(1)
        pyautogui.write("cmd")
        pyautogui.press("enter")
        time.sleep(2)
        pyautogui.typewrite(command1)
        pyautogui.press("enter")
        time.sleep(2) 
        pyautogui.hotkey('alt', 'f4')
    else:
        print('no saved contact')

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()
        self.known_faces = []
        self.known_face_names = []
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def load_known_faces(self, path):
        for file in os.listdir(path):
            img = cv2.imread(os.path.join(path, file))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            if len(faces) > 0:
                self.known_faces.append(gray)
                self.known_face_names.append(os.path.splitext(file)[0])

    def recognize_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_region = gray[y:y+h, x:x+w]

            for i, known_face in enumerate(self.known_faces):
                if self.compare_faces(face_region, known_face):
                    return self.known_face_names[i]
        return "Unknown"
    
    def compare_faces(self, face1, face2):
        hist1 = cv2.calcHist([face1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([face2], [0], None, [256], [0, 256])
        return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL) > 0.5

    def register(self, username, camera_index=0):
        cap = cv2.VideoCapture(camera_index)
        for i in range(10):
            ret, frame = cap.read()
        ret, frame = cap.read()
        if not ret:
            return False

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_region = gray[y:y+h, x:x+w]
            self.known_faces.append(face_region)
            self.known_face_names.append(username)
            cv2.imwrite(f"faces/{username}.jpg", face_region)
            cap.release()
            cv2.destroyAllWindows()
            return True
        return False

    def login(self,email_id ,camera_index=0):
        cap = cv2.VideoCapture(camera_index)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            name = self.recognize_face(frame)
            cv2.imshow('Face Recognition Login', frame)
            cv2.putText(frame, f"Recognized: {name}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            if name != "Unknown":
                print("<-------ACCESS GRANTED------->")
                current_datetime = datetime.datetime.now()
                if not os.path.exists("logindata.csv"):
                    with open("logindata.csv", 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(["Email", "Login_Time"])
                with open('logindata.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([email_id.lower(), current_datetime])
                self.TaskExecution()
                break
            elif name == "Unknown":
                print("<-------UNAUTORISED ACCESS------->")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def FaceRec(self):
        print("")
        print("Welcome to Face Recognition Login!")
        choice = input("Do you want to login or register? (login/register): ")

        if choice.lower() == "login":
            self.load_known_faces("faces")
            LoginMail = input("Enter your Email-ID: ")
            
            with open("users.csv", 'r') as file:
                reader = csv.reader(file)
                users = list(reader)
                try:
                    for user in users:
                        if user[0] == LoginMail.lower():
                            self.login(LoginMail)
                    else:
                        print("User not found. Please register first.")
                        print("")
                        self.FaceRec()
                except Exception as e:
                    print(e)
                    print("No User Found.")
                    self.FaceRec()

        elif choice.lower() == "register":
            username = input("Enter your username: ")
            RegMail = input("Enter your Email-ID: ")
            current_datetime = datetime.datetime.now()
            if not os.path.exists("users.csv"):
                with open("users.csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Email", "RegesDate","Username"])
            with open("users.csv", 'r') as file:
                reader = csv.reader(file)
                users = list(reader)
                if RegMail.lower() in [user[0] for user in users]:
                    print("Email-ID already exists. Please try another one.")
                    print("")
                    self.FaceRec()
                else:
                    with open("users.csv", 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([RegMail.lower(), current_datetime ,username])
                    self.register(username)
                    print("Registration Successful!")
                    print("")
                    self.FaceRec()
        else:
            print("Invalid choice. Please try again.")
            self.FaceRec()

    def wakeup(self):
        while True:
            query = input("Enter Query: ").lower()
            print("")
            if 'wake up' in query or 'hello' in query or 'wakeup' in query or 'daddy is here' in query:
                self.TaskExecution()
    def run(self):
        self.FaceRec()

    def TaskExecution(self):
        wish()
        while True:
            query = input("Enter Query: ").lower()
            print("")
            if query == "none":
                data = "none"
                pass
            else:
                try:
                    if re.search('date', query):
                        date = obj.tell_me_date()
                        speak(date)
                        data = date

                    elif "what is the time" in query or "tell me the time" in query or "what's the time" in query:
                        time_c = obj.tell_time()
                        speak(f"Sir the time is {time_c}")
                        data = time_c
                    
                    elif query in GREETINGS:
                        speak(random.choice(GREETINGS_RES))
                        data = "GREATINGS!!!"

                    elif re.search('weather', query):
                        city = query.split(' ')[-1]
                        weather_res = obj.weather(city=city)
                        speak(weather_res)
                        data = weather_res
                    elif re.search('tell me about', query):
                        topic = query.split(' ')[-1]
                        if topic:
                            wiki_res = obj.tell_me(topic)
                            speak(wiki_res)
                            data = wiki_res
                        else:
                            speak("Sorry sir. I couldn't load your query from my database. Please try again")
                            data = "Sorry sir. I couldn't load your query from my database. Please try again"

                    elif "buzzing" in query or "news" in query or "headlines" in query:
                        onlyspeak("Which type of news do you want? (e.g., sports, technology): ")
                        category = input("Which type of news do you want? (e.g., sports, technology): ").strip().lower()
                        latestNews(category)
                        data = 'These were the top headlines, Have a nice day Sir!!..'

                    elif "email" in query or "send email" in query:
                        sender_email = config.email
                        sender_password = config.email_password
                        try:
                            speak("Please enter the email ID sir ?")
                            receiver_email = input("Enter Email ID: ")
                            if "@gmail.com" in receiver_email:
                                print("")
                                speak("What is the subject sir ?")
                                subject = input("Enter Subject: ")
                                print("")
                                speak("What should I say?")
                                message = input("Enter Message: ")
                                print("")
                                msg = 'Subject: {}\n\n{}'.format(subject, message)
                                obj.send_mail(sender_email, sender_password,receiver_email, msg)
                                speak("Email has been successfully sent")
                                time.sleep(2)
                                data = "Email has been successfully sent"
                            else:
                                speak("please enter a valid email id")
                                data = "I coudn't find the requested person's email in my database. Please try again with a different name"

                        except:
                            speak("Sorry sir. Couldn't send your mail. Please try again")
                            data = "Sorry sir. Couldn't send your mail. Please try again"

                    elif "calculate" in query:
                        speak("what do you want to calculate")
                        question = input("Enter Query: ").lower()
                        answer = computational_intelligence(question)
                        speak(answer)
                        data = answer

                    elif "play" in query and "song" in query:
                        query = query.replace("play","")
                        pywhatkit.playonyt(query)
                        speak("playing "+ query)
                        data="playing "+ query

                    elif "temperature" in query:
                        search = "temperature"
                        url = f"https://www.google.com/search?q={search}"
                        r = requests.get(url)
                        data = BeautifulSoup(r.text,"html.parser")
                        temp = data.find("div",class_="BNeawe").text
                        speak(f"current {search} is {temp}")
                        data = temp

                    elif "code" in query and "open" in query:
                        file_path = "D:/Alpha Main/Alpha.py"
                        subprocess.Popen(['start', file_path], shell=True)
                        time.sleep(3)
                        pyautogui.typewrite("code .")
                        time.sleep(3)
                        pyautogui.press("enter")
                        data = "openned code"

                    elif "open" in query:
                        query = query.replace("open", "")
                        query = query.replace("Alpha", "")
                        pyautogui.press("super")
                        pyautogui.typewrite(query)
                        pyautogui.sleep(1)
                        pyautogui.press("enter")
                        speak("Openning " + query+ " for you sir")
                        data = "openned" + query

                    elif "close" in query:
                        query=query.replace("close","")
                        query=query.replace("Alpha","")
                        close(query)
                        data = "closed"+query

                    elif "message" in query:
                        query1 = query.replace("message","")
                        query1 = query1.replace("to","")
                        query1 = query1.replace(" ","")
                        query1 = query1.replace("whatsapp","")
                        query1 = query1.replace("Alpha","")
                        query1 = query1.replace("send","")
                        name = query1
                        b = CONTACTS.keys()
                        if name in b:
                            num= CONTACTS[name]
                            speak(f"What's the message for {name}")
                            mess=input("Enter Query: ")
                            messages(num,mess)
                            speak("i have sent the message")
                        else:
                            speak(f"there is no one in the CONTACTS with name {name}")
                        data="sent message"

                    elif "youtube search" in query:
                        speak("ok sir,  This is what i found for your search!")
                        query1=query.replace("Alpha","")
                        query1=query1.replace("youtube search","")
                        web= "https://www.youtube.com/results?search_query="+query1
                        webbrowser.open(web)
                        data="searched youtube"

                    elif "google search" in query:
                        speak("ok sir,  This is what i found for your search!")
                        query=query.replace("Alpha","")
                        query=query.replace("google search","")
                        data=pywhatkit.search(query)
                        speak(data)
                    
                    elif "system info" in query:
                        sys_info = obj.system_info()
                        speak(sys_info)
                        data = "system info given"

                    elif "where is" in query:
                        place= query.replace("where","")
                        place = place.replace("is","")
                        place = place.replace("Alpha","")
                        speak(loc(place))
                        data = "location found"
                        

                    elif "image" in query or "generate" in query:
                        try:
                            speak("i will display the image as soon as it is generated.")
                            image_input = query.replace("alpha","")
                            image_input = query.replace("generate","")
                            image_input = query.replace("image","")
                            image_inp= {"inputs": f"{image_input}", }
                            image_bytes = query_img(image_inp)
                            import io
                            from PIL import Image
                            image = Image.open(io.BytesIO(image_bytes))
                            image.show()
                            data = "generated image"
                        except Exception as e:
                            speak("some error ocurred while generating the image")
                            data = "error"
                    
                    elif " ip " in query:
                        ip = requests.get('https://api.ipify.org').text
                        speak(f"Your ip address is {ip}")
                        data = f"Your ip address is {ip}"

                    elif "switch the window" in query or "switch window" in query:
                        speak("Okay sir, Switching the window")
                        pyautogui.keyDown("alt")
                        pyautogui.press("tab")
                        pyautogui.keyUp("alt")
                        data = "window switched"

                    elif "where i am" in query or "current location" in query or "where am i" in query:
                        try:
                            city, state, country = obj.my_location()
                            speak(
                                f"You are currently in {city} city which is in {state} state and country {country}")
                            a = f"You are currently in {city} city which is in {state} state and country {country}"
                            data = a
                        except Exception as e:
                            speak("Sorry sir, I coundn't fetch your current location. Please try again")
                            data = "Coundn't fetch your current location"

                    elif "take screenshot" in query or "take a screenshot" in query or "capture the screen" in query or "take ss" in query :
                        speak("By what name do you want to save the screenshot?")
                        name = input("Enter Query: ").lower()
                        speak("")
                        speak("Alright sir, taking the screenshot")
                        speak("")
                        img = pyautogui.screenshot()  
                        name = f"{name}.png"
                        name = "screenshots\\" + name
                        img.save(name)
                        speak("The screenshot has been succesfully captured")
                        data = "Screenshot captured"
                    
                    elif "hide all files" in query or "hide this folder" in query:
                        os.system("attrib +h /s /d")
                        speak("Sir, all the files in this folder are now hidden")
                        data =" Sir, all the files in this folder are now hidden"

                    elif "visible" in query or "make files visible" in query:
                        os.system("attrib -h /s /d")
                        speak("Sir, all the files in this folder are now visible to everyone. I hope you are taking this decision in your own peace")
                        data =" Sir, all the files in this folder are now visible to everyone. I hope you are taking this decision in your own peace"
                    
                    elif "goodbye" in query or "offline" in query or "bye" in query or "exit" in query or "quit" in query or "sleep" in query:
                        speak(" Alright sir, going offline. It was nice working with you")
                        self.wakeup()
                        data = "going offline"
                        
                    elif "essay" in query or "passage" in query or "paragraph" in query:
                        response = chat_interaction(query)
                        speak("Here is a passage for you.")
                        print(response)
                        print("")
                        data = "Wrote an essay"
                
                    elif "call" in query and "can" in query:
                        query = query.replace("alpha", "")
                        query = query.replace("call", "")
                        query = query.replace("please", "")
                        query = query.replace(" ", "")
                        query = query.replace("can", "")
                        query = query.replace("you", "")
                        query = query.replace("to", "")
                        query = query.replace("place", "")
                        name = query
                        speak("Calling " + name)
                        call(name)

                    else:  
                        response = chat_interaction(query)
                        if response != None:
                            response = response.replace("Gemini","SIGMA AI, a team of engineering students of Bennett University by TOI based in Greater Noida, Uttar Pradesh, India")
                            response = response.replace("Mistral","SIGMA")
                            response = response.replace("*","")
                            
                            a = response
                            if len(a.split()) <= 500:    
                                speak(response)
                            else:
                                print("Alpha : ", response)
                                print("")
                        else:
                            response = "Can you repeat that again please?"

                        data = response
                        
                except:
                    speak("couldn't handle your query")
                    data = "error"

startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def __del__(self):
        sys.stdout = sys.__stdout__

    def startTask(self):
        self.ui.movie = QtGui.QMovie("live_wallpaper.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("initiating.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
alpha = Main()
alpha.show()
exit(app.exec_())
