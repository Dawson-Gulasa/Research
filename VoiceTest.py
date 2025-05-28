from gpiozero import LED, Button
from time import sleep

# Define pin connections
led = LED(17)
button = Button(2)

print("GPIO Test: LED should blink, press button to test input.")

try:
    while True:
        # Blink the LED
        led.on()
        print("LED ON")
        sleep(0.5)
        led.off()
        print("LED OFF")
        sleep(0.5)

        # Check for button press
        if button.is_pressed:
            print("Button was pressed!")

except KeyboardInterrupt:
    print("\nExiting program.")
finally:
    led.off()
