import json
import speech_recognition as sr
import pyttsx3
from fuzzywuzzy import process

# Initialize the TTS engine
engine = pyttsx3.init()

# Set voice to female
def set_female_voice():
    voices = engine.getProperty('voices')
    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

set_female_voice()  # Apply the female voice

# Load responses from JSON file
def load_responses():
    with open("responses.json", "r") as file:
        return json.load(file)

# Find the best matching command
def find_best_match(command, responses):
    best_match, score = process.extractOne(command, responses.keys())
    return responses[best_match] if score > 75 else "Sorry, I don't understand."

# Function to recognize speech
def listen_for_commands():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except Exception:
        return None

# Function to speak response
def speak_response(response):
    engine.say(response)
    engine.runAndWait()

# Main function
def run_assistant():
    responses = load_responses()
    while True:
        command = listen_for_commands()
        if command:
            if "hello bujji" in command:
                speak_response("Hi Pavan, I am Boo-gee!")  # Phonetic correction
            else:
                response = find_best_match(command, responses)
                speak_response(response)

            if command == "goodbye":
                break  # Exit loop when "goodbye" is said

if __name__ == "__main__":
    run_assistant()
