import speech_recognition as sr

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=2)

    with microphone as source:
        print("Adjusting for ambient noise... Please be silent for a moment.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening now... Speak clearly.")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")

if __name__ == "__main__":
    print("Speech to Text - Microphone Input")
    recognize_speech_from_mic()
