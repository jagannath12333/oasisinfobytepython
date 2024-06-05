import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import datetime
import smtplib
import requests
import spacy

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
    except sr.RequestError:
        print("Could not request results; check your network connection.")
    return ""

def handle_command(command):
    if "hello" in command:
        speak("Hello! How can I assist you?")
    elif "time" in command:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        speak(f"The current time is {current_time}")
    elif "date" in command:
        today = datetime.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")
    elif "search" in command:
        speak("What do you want to search for?")
        query = recognize_speech()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Searching for {query}")
    else:
        speak("Sorry, I don't understand that command.")

def send_email(subject, body, to):
    user = "your_email@gmail.com"
    password = "your_password"
    
    email_text = f"Subject: {subject}\n\n{body}"
    
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(user, password)
        server.sendmail(user, to, email_text)
        server.close()
        speak("Email sent successfully.")
    except Exception as e:
        speak(f"Failed to send email. Error: {str(e)}")

def get_weather(city):
    api_key = "your_openweathermap_api_key"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        temperature = main["temp"]
        description = weather["description"]
        return f"The temperature in {city} is {temperature - 273.15:.2f}°C with {description}."
    else:
        return "City not found."

def handle_advanced_command(command):
    if "email" in command:
        speak("What is the subject?")
        subject = recognize_speech()
        if subject:
            speak("What is the body?")
            body = recognize_speech()
            if body:
                send_email(subject, body, "recipient_email@gmail.com")
    elif "weather" in command:
        speak("Which city?")
        city = recognize_speech()
        if city:
            weather_info = get_weather(city)
            speak(weather_info)
    else:
        handle_command(command)

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    while True:
        command = recognize_speech()
        if command:
            handle_advanced_command(command)
