import datetime
import os
import random
import subprocess
import time
import webbrowser
from urllib.parse import quote_plus

import pyautogui
import pyttsx3
import pywhatkit
import requests
import speech_recognition as sr
import wikipedia
import wolframalpha
from ecapture import ecapture as ec

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

ASSISTANT_NAME = "Lucifer"
OWNER_NAME = "Divyansh"
SPEECH_RATE = 170

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID", "")
MUSIC_DIR = os.getenv("MUSIC_DIR", os.path.join(os.path.expanduser("~"), "Music"))

SITES = {
    "open youtube": ("https://www.youtube.com", "YouTube is open now"),
    "open insta": ("https://www.instagram.com", "Instagram is open now"),
    "open google": ("https://www.google.com", "Google is open now"),
    "open gmail": ("https://mail.google.com", "Gmail is open now"),
    "open stackoverflow": ("https://stackoverflow.com", "Here is Stack Overflow"),
    "advice": ("https://api.adviceslip.com/advice", "Your advice is on the screen"),
}

EXIT_PHRASES = ("good bye", "goodbye", "exit", "quit", "shut down")


engine = pyttsx3.init("sapi5")
_voices = engine.getProperty("voices")
if len(_voices) > 1:
    engine.setProperty("voice", _voices[1].id)
engine.setProperty("rate", SPEECH_RATE)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def say_and_print(text):
    print(text)
    speak(text)


def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        say_and_print("Hello, good morning")
    elif hour < 18:
        say_and_print("Hello, good afternoon")
    else:
        say_and_print("Hello, good evening")


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="en-in")
    except (sr.UnknownValueError, sr.RequestError):
        speak("Pardon me, please say that again")
        return ""
    print(f"You said: {text}\n")
    return text.lower()


def tell_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {now}")


def tell_date():
    today = datetime.date.today()
    speak(f"Today is {today.strftime('%A, %d %B %Y')}")


def open_site(url, message):
    webbrowser.open_new_tab(url)
    speak(message)


def search_wikipedia(statement):
    speak("Searching Wikipedia")
    query = statement.replace("wikipedia", "").strip()
    try:
        summary = wikipedia.summary(query, sentences=3)
    except wikipedia.exceptions.DisambiguationError:
        speak("That is ambiguous, please be more specific")
        return
    except wikipedia.exceptions.PageError:
        speak("I could not find a page for that")
        return
    speak("According to Wikipedia")
    say_and_print(summary)


def play_on_youtube():
    speak("What should I play on YouTube?")
    title = listen()
    if not title:
        return
    pywhatkit.playonyt(title)
    speak(f"Playing {title}")


def play_music():
    if not os.path.isdir(MUSIC_DIR):
        speak("I could not find your music folder")
        return
    tracks = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith((".mp3", ".wav", ".flac", ".m4a"))]
    if not tracks:
        speak("There are no songs in your music folder")
        return
    speak("Playing some music, please wait")
    os.startfile(os.path.join(MUSIC_DIR, random.choice(tracks)))


def report_weather():
    if not OPENWEATHER_API_KEY:
        speak("The weather key is not configured")
        return
    speak("What is the city name?")
    city = listen()
    if not city:
        return
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"appid": OPENWEATHER_API_KEY, "q": city, "units": "metric"},
        timeout=10,
    )
    data = response.json()
    if str(data.get("cod")) != "200":
        speak("City not found")
        return
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]
    say_and_print(
        f"Temperature is {temperature} degrees Celsius, humidity is {humidity} percent, "
        f"with {description}"
    )


def answer_question():
    if not WOLFRAM_APP_ID:
        speak("The Wolfram Alpha key is not configured")
        return
    speak("I can answer computational and geographical questions. What would you like to ask?")
    question = listen()
    if not question:
        return
    try:
        result = wolframalpha.Client(WOLFRAM_APP_ID).query(question)
        answer = next(result.results).text
    except (StopIteration, Exception):
        speak("I could not find an answer to that")
        return
    say_and_print(answer)


def take_photo():
    ec.capture(0, "camera", "img.jpg")
    speak("Photo saved")


def web_search(statement):
    query = statement.replace("search", "").strip()
    if query:
        webbrowser.open_new_tab(f"https://www.google.com/search?q={quote_plus(query)}")


def log_off():
    speak("Logging off in a few seconds, please close your applications")
    time.sleep(5)
    subprocess.call(["shutdown", "/l"])


def handle(statement):
    if any(phrase in statement for phrase in EXIT_PHRASES):
        say_and_print(f"{ASSISTANT_NAME} is shutting down. Good bye")
        return False

    if "wikipedia" in statement:
        search_wikipedia(statement)
    elif "play song on youtube" in statement or "song youtube" in statement:
        play_on_youtube()
    elif "play music" in statement:
        play_music()
    elif "volume up" in statement:
        pyautogui.press("volumeup")
    elif "volume down" in statement:
        pyautogui.press("volumedown")
    elif "mute" in statement:
        pyautogui.press("volumemute")
    elif "weather" in statement:
        report_weather()
    elif "date" in statement:
        tell_date()
    elif "time" in statement:
        tell_time()
    elif "who are you" in statement or "what can you do" in statement:
        speak(
            f"I am {ASSISTANT_NAME}, your voice assistant. I can open websites, play music, "
            "check the weather, search Wikipedia and answer questions, any time you need me"
        )
    elif "who made you" in statement or "who created you" in statement:
        say_and_print(f"I was built by {OWNER_NAME}")
    elif "news" in statement:
        open_site(
            "https://timesofindia.indiatimes.com/home/headlines",
            "Here are the latest headlines from the Times of India",
        )
    elif "camera" in statement or "take a photo" in statement:
        take_photo()
    elif "calculate" in statement or "question" in statement:
        answer_question()
    elif "search" in statement:
        web_search(statement)
    elif "log off" in statement or "sign out" in statement:
        log_off()
    else:
        for phrase, (url, message) in SITES.items():
            if phrase in statement:
                open_site(url, message)
                break
    return True


def main():
    print(f"Loading {ASSISTANT_NAME}, your personal voice assistant")
    speak(f"Loading your personal voice assistant {ASSISTANT_NAME}")
    greet()

    running = True
    while running:
        speak("How can I help you?")
        statement = listen()
        if statement:
            running = handle(statement)


if __name__ == "__main__":
    main()
