import time
import webbrowser
import speech_recognition as sr
import pyttsx3 
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init() # Initailized
newsapi = "NEWS_API_KEY"

def speak_old(text):
    try:
        # print("Speaking:", text) # Testing speech
        engine = pyttsx3.init()  # Reinitialize each time
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
        time.sleep(0.3)
    except Exception as e:
        print(f"Speech error: {e}")

def speak(text):
   tts = gTTS(text)
   tts.save('temp.mp3')

   pygame.mixer.init()

   pygame.mixer.music.load('temp.mp3')

   pygame.mixer.music.play()

   while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(10)

   pygame.mixer.music.unload()
   os.remove("temp.mp3")

def aiProcess(c):
    client = OpenAI(
      api_key="OPENAI_API_KEY"
      )
    comppletion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": c}
    ]
)

    return comppletion.choices[0].message.content
   

def processCommand(c):
    if "open google" in c.lower():
        speak("Opening google")
        webbrowser.open("https://google.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open gmail" in c.lower():
        webbrowser.open("https://gmail.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link) 
    elif "open news" in c.lower():
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        # print(f"Making request to: {url}")  # To check the url
        response = requests.get(url)


        if response.status_code == 200:
         data = response.json()

         articles = data.get("articles", [])
         print(f"Found {len(articles)} articles")
         print("Top India Headlines:\n")
         for idx, article in enumerate(articles[:5], 1):
            title = article.get('title')
            print(f"{idx}. {title}")
            speak(title)
        else:
         print(f"Failed to fetch news: {response.status_code}")
    
    else:
       # Let openai handle the request
       output = aiProcess(c)
       speak(output)

        

if __name__ == "__main__":
    # speak("Testing speech") #Testing Speech
    speak("Initializing Jarvis......")

while True:
    # Listen for the wake word "Jarvis"
    # Obtain audio from the microphone
    recognizer = sr.Recognizer()
    print("SPEAK Jarvis....")
    try:
        with sr.Microphone() as source:
          recognizer.adjust_for_ambient_noise(source, duration=1)
          print("Listening...")
          audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        # Recognizing audio using google_cloud recognizer

        word = recognizer.recognize_google(audio)
        print(f"Recognised:  '{word}'")
        if word.lower() == "jarvis":
            speak("Yes")

            # Listen to command

            with sr.Microphone() as source:
             print("Jarvis Activated")
             audio = recognizer.listen(source)
             command = recognizer.recognize_google(audio)

             processCommand(command)

        
        
    except sr.UnknownValueError:
        print("Jarvis could not understand audio")
        speak("Sorry, I didn't catch that")
    except sr.RequestError as e:
        print("Jarvis error: {0}". format(e))