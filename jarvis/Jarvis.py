# open ai api do not work properly...

import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import openai
import pygame
import os
from gtts import gTTS

# Initialize the Recognizer and pyttsx3
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "<Your Key Here>"  # Add your News API key here
OPENAI_API_KEY = "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"  # Add your OpenAI API key here

def speak(text):
    """Convert text to speech using gTTS and play it with pygame."""
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    pygame.mixer.quit()  # Properly quit the mixer
    os.remove("temp.mp3")

def aiProcess(command):
    """Process the command using OpenAI API."""
    openai.api_key = OPENAI_API_KEY

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please."},
                {"role": "user", "content": command}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except openai.error.OpenAIError as e:
        return f"Error with OpenAI API: {e}"

def processCommand(c):
    """Processes commands from the user."""
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song, "")
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
        else:
            speak("Unable to fetch news.")
    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        try:
            print("recognizing...")

            # Listen for the wake word "Jarvis"
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes?")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)

        except Exception as e:
            print(f"Error: {e}")
