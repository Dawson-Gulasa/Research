#!/usr/bin/env python3

from periphery import GPIO
import speech_recognition as sr
import time

# GPIO Pin mapping (using GPIO numbers, not physical pin numbers)
TOOL_PINS = {
    "wrench": 17,
    "screwdriver": 27,
    "pliers": 22
}

# Initialize GPIO pins
gpio_pins = {tool: GPIO(f"/dev/gpiochip0", pin, "out") for tool, pin in TOOL_PINS.items()}

def clear_leds():
    """Function to turn off all LEDs."""
    for gpio in gpio_pins.values():
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
        gpio.close()
