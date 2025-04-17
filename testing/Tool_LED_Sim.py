import speech_recognition as sr
import RPi.GPIO as GPIO
import time

# Match spoken words with GPIO pin outputs
TOOL_PINS = {
    "wrench": 17,
    "screwdriver": 27,
    "pliers" : 22
}

# Set GPIO's to BCM mode - referring to the pins by the "Broadcom SOC channel" number
GPIO.setmode(GPIO.BCM)

# assign GPIO pins and make sure LEDs are off by default
for pin in TOOL_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def clear_leds():
    for pin in TOOL_PINS.values():
        GPIO.output(pin, GPIO.LOW)

# Setup voice recognition
recognizer = sr.Recgonizer()

try:
        with sr.Microphone() as source:
             print("Say a tool name (wrench, screwdriver, okiers):")
             recognizer.adjust_for_ambient_noise(source) # reduced background noise
             audio = recognizer.listen(source)

             print("Processing...")
             command = recognizer.recognize_google(audio).lower()
             print("You said:", command)

             clear_leds()

             for tool, pin in TOOL_PINS.items():
                  if tool in command:
                       print(f"Activating {tool} at pin {pin}")
                       GPIO.output(pin, GPIO.HIGH)
                       time.sleep(5)
                       GPIO.output(pin, GPIO.LOW)
                       break
                  
                  else:
                       print("No matching tool found.")

except sr.UknownValueError:
    print("Sorry, could not understand the audio.")
except sr.RequestError:
     print("Could not request results; check your internet connection.")
finally:
     GPIO.cleanup()
