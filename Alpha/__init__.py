import speech_recognition as sr
import pyttsx3
from Alpha.features import date_time
from Alpha.features import launch_app
from Alpha.features import website_open
from Alpha.features import weather
from Alpha.features import wikipedia
from Alpha.features import News
from Alpha.features import send_email
from Alpha.features import note
from Alpha.features import system_stats
from Alpha.features import loc

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

class AlphaAssistant:
    def __init__(self):
        pass
    
    def tts(self, text):
        try:
            engine.say(text)
            engine.runAndWait()
            engine.setProperty('rate', 175)
            return True
        except:
            t = "Sorry I couldn't understand and handle this input"
            print(t)
            return False
    def tell_me_date(self):
        return date_time.date()
    def tell_time(self):
        return date_time.time()
    def launch_any_app(self, path_of_app):
        return launch_app.launch_app(path_of_app)
    def website_opener(self, domain):
        return website_open.website_opener(domain)
    def weather(self, city):
        try:
            res = weather.fetch_weather(city)
        except Exception as e:
            print(e)
            res = False
        return res
    def tell_me(self, topic):
        return wikipedia.tell_me_about(topic)
    def news(self):
        return News.latestnews()
    def send_mail(self, sender_email, sender_password, receiver_email, msg):
        return send_email.mail(sender_email, sender_password, receiver_email, msg)
    def take_note(self, text):
        note.note(text)
    def system_info(self):
        return system_stats.system_stats()
    def my_location(self):
        city, state, country = loc.my_location()
        return city, state, country