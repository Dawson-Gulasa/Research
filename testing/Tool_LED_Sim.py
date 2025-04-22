import speech_recognition as sr
import RPi.GPIO as GPIO
import time

# Dictionary mapping tool names (as voice commands) to specific GPIO pin numbers
TOOL_PINS = {
    "wrench": 17,           #GPIO pin 17 assigned to wrench
    "screwdriver": 27,      #GPIO pin 27 assigned to screwdriver
    "pliers" : 22           #GPIO pin 22 assigned to pliers
}

# Set GPIO's to BCM mode (Broadcom SOC channel numbers)
GPIO.setmode(GPIO.BCM)

# Initialize each tool pin as an output, and set it LOW (LED off by default)
for pin in TOOL_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Function to clear all LEDs (Turn them off)
def clear_leds():
    for pin in TOOL_PINS.values():
        GPIO.output(pin, GPIO.LOW)

# Setup voice recognition
recognizer = sr.Recognizer()

# Try block to begin listening and precessing voice input
try:
        # Use the microphone as the audio input source
        with sr.Microphone() as source:
             print("Say a tool name (wrench, screwdriver, okiers):")

             # reduced background noise
             recognizer.adjust_for_ambient_noise(source)

             # Listen for voice input from the microphone
             audio = recognizer.listen(source)

             print("Processing...")

             # Convert the spoken audio to lwoercase text using Google's speech recognition
             command = recognizer.recognize_google(audio).lower()
             print("You said:", command)

             # Turn off LEDs before new command &  Check if any tool name is mentioned in the recognized command 
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

# Error Handling
except sr.UknownValueError:
    print("Sorry, could not understand the audio.")
except sr.RequestError:
     print("Could not request results; check your internet connection.")
finally:
     GPIO.cleanup()
