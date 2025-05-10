#!/usr/bin/env python3

import os
import time
import speech_recognition as sr

# GPIO pin numbers (BCM numbering)
TOOL_PINS = {
    "wrench": 17,
    "screwdriver": 27,
    "pliers": 22
}

# Function to export GPIO pins and set them as outputs
def setup_gpio():
    for pin in TOOL_PINS.values():
        try:
            with open(f"/sys/class/gpio/export", "w") as f:
                f.write(str(pin))
        except:
            pass  # Ignore if already exported

        with open(f"/sys/class/gpio/gpio{pin}/direction", "w") as f:
            f.write("out")

# Function to clear all LEDs
def clear_leds():
    for pin in TOOL_PINS.values():
        try:
            with open(f"/sys/class/gpio/gpio{pin}/value", "w") as f:
                f.write("0")
        except:
            pass

# Setup voice recognition
recognizer = sr.Recognizer()
setup_gpio()

try:
    print("Say a tool name (wrench, screwdriver, pliers):")
    
    # Setup microphone input for voice recognition
    with sr.Microphone(sample_rate=16000) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        print("Processing...")
        
        # Recognize voice command using Google API
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        
        # Clear LEDs before activating the correct one
        clear_leds()
        for tool, pin in TOOL_PINS.items():
            if tool in command:
                print(f"Activating {tool} LED on pin {pin}")
                with open(f"/sys/class/gpio/gpio{pin}/value", "w") as f:
                    f.write("1")
                time.sleep(5)
                with open(f"/sys/class/gpio/gpio{pin}/value", "w") as f:
                    f.write("0")
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
    # Unexport GPIOs to clean up
    for pin in TOOL_PINS.values():
        try:
            with open(f"/sys/class/gpio/unexport", "w") as f:
                f.write(str(pin))
        except:
            pass
