import openai
import pyttsx3
import speech_recognition as sr
import webbrowser
import subprocess

# Check if required libraries are installed, and install them if not
def install(package):
    subprocess.check_call(["pip", "install", package])

try:
    import openai
except ImportError:
    install("openai")
    import openai

try:
    import pyttsx3
except ImportError:
    install("pyttsx3")
    import pyttsx3

try:
    import speech_recognition as sr
except ImportError:
    install("SpeechRecognition")
    import speech_recognition as sr

openai.api_key = "your-openai-api-key"

engine = pyttsx3.init(driverName='sapi5')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        wake_word = "winston"
        print("Listening for wake word and command...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language = "en-US")
        if wake_word in text:
            command = text.replace(wake_word, "").strip()
            return command
        else:
            return text
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return False

while True:
    command = listen()
    print("your command is: " + command)
    if command == "goodbye":
        speak("Goodbye")
        break
    elif command == "Winston open browser":
        webbrowser.open_new_tab("http://www.google.com")
        speak("Opening the browser")
    else:
        prompt = command
        response = openai.Completion.create(engine="text-davinci-003", prompt = prompt, max_tokens=100)
        print(response.choices[0].text)
        speak(response.choices[0].text)
