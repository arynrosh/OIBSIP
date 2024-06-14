# VOICE ASSISTANT BY ARYAN ROSHAN

import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text): # Function that prints assistant responses in terminal.
    print("Assistant: " + text)
    engine.say(text)
    engine.runAndWait()

def respond_to_hello(): # Function greets user when the user says hello.
    speak("Hello! How can I help you today?")

def tell_time(): # Function to tell the current time to the user.
    now = datetime.datetime.now()
    hours = now.hour
    minutes = now.minute
    time_str = f"{hours:02}:{minutes:02}"
    speak("The time is " + time_str)

def tell_date():  # Function to tell the date to the user.
    today = datetime.date.today()
    date_str = today.strftime("%B %d, %Y")
    speak("Today's date is " + date_str)

def search_web(query): # Function that redirects user to the web for their query.
    speak("I'm looking up " + query + " on the web.")
    pywhatkit.search(query)

def listen_command(): 
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source) # Adjust for ambient noise
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            command = format_command(command)
            print(f"You said: {command}")
            return command.lower()
    except sr.WaitTimeoutError: # Case when no audio is detected.
        speak("No audio detected. Please try again.")
        return ""
    except sr.UnknownValueError: # Case when audio is not clear.
        speak("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError: # Case when there is no internet for web queries.
        speak("Could not request results; check your network connection.")
        return ""

def format_command(command): # Function to format user commands in terminal.
    command = command.strip()
    if command.lower().startswith(("what", "when", "where", "who", "why", "how")):
        command = command + "?"
    return command

def main():
    while True:
        command = listen_command()
        if command:
            if command.lower().startswith(("hello", "hey", "hi")):
                respond_to_hello()
            elif "time" in command:
                tell_time()
            elif "date" in command:
                tell_date()
            elif "exit" in command or "quit" in command:
                speak("Goodbye!")
                break
            else:
                search_web(command)

if __name__ == "__main__":
    main()
