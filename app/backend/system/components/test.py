import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the button
button_pin = 10  # You can change this to the desired GPIO pin

# Set up the button pin as an input with a pull-up resistor
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    print("Press the button (CTRL+C to exit):")
    while True:
        if GPIO.input(button_pin) == GPIO.HIGH:
            print("Button pressed!")
            # You can add your desired actions here
            time.sleep(0.2)  # Add a small delay to debounce the button
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()  # Cleanup GPIO settings when exiting the script
