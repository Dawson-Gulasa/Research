#!/usr/bin/env python3

from periphery import GPIO
import speech_recognition as sr
import time
import os

# Automatically detect the available GPIO chip
gpio_chip = None
for chip in os.listdir('/dev'):
    if chip.startswith("gpiochip"):
        gpio_chip = f"/dev/{chip}"
        break

if not gpio_chip:
    print("Error: No GPIO chip found.")
    exit(1)

print(f"Using GPIO Chip: {gpio_chip}")

# GPIO Pin mapping (using GPIO numbers, not physical pin numbers)
TOOL_PINS = {
    "wrench": 17,
    "screwdriver": 27,
    "pliers": 22
}

# Initialize GPIO pins (only if chip is detected)
gpio_pins = {}
try:
    for tool, pin in TOOL_PINS.items():
        gpio_pins[tool] = GPIO(gpio_chip, pin, "out")
except Exception as e:
    print(f"Error initializing GPIOs: {e}")
    exit(1)

def clear_leds():
    """Function to turn off all LEDs."""
    for gpio in gpio_pins.values():
        if gpio is not None:
            gpio.write(False)

# Setup voice recognition
recognizer = sr.Recognizer()

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
        for tool, gpio in gpio_pins.items():
            if tool in command:
                print(f"Activating {tool} LED on pin {TOOL_PINS[tool]}")
                gpio.write(True)
                time.sleep(5)
                gpio.write(False)
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
    for gpio in gpio_pins.values():
        if gpio is not None:
            gpio.close()
