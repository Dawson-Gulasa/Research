import speech_recognition as sr
from datetime import date
from time import sleep

# Initialize recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()

print("Voice recognition started. Say something!")

while True:
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        words = r.recognize_google(audio).lower()
        print(f"You said: {words}")

        if "today" in words:
            print(date.today())

        if "stop" in words:
            print("Stopping...")
            sleep(1)
            break

    except sr.UnknownValueError:
        print("Sorry, I didn’t catch that.")
    except sr.RequestError:
        print("Speech recognition service is unavailable.")
