#!/usr/bin/env python3

from gpiozero import LED
import speech_recognition as sr
import time

# Dictionary mapping tool names (as voice commands) to GPIO LEDs using GPIOZero
TOOL_LEDS = {
    "wrench": LED(17),
    "screwdriver": LED(27),
    "pliers": LED(22)
}

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def clear_leds():
    """Function to turn off all LEDs."""
    for led in TOOL_LEDS.values():
        led.off()

try:
    print("Say a tool name (wrench, screwdriver, pliers):")
    
    # Setup microphone input for voice recognition
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        print("Processing...")
        
        # Recognize voice command using Google API
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        
        # Clear LEDs before activating the correct one
        clear_leds()
        for tool, led in TOOL_LEDS.items():
            if tool in command:
                print(f"Activating {tool} LED")
                led.on()
                time.sleep(5)
                led.off()
                break
        else:
            print("No matching tool found.")

except sr.UnknownValueError:
    print("Sorry, could not understand the audio.")
except sr.RequestError:
    print("Could not request results; check your internet connection.")
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    clear_leds()
