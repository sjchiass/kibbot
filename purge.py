from time import sleep
import RPi.GPIO as GPIO


# Make it so GPIO pins by their system number, not their position. The two sets
# of numbers are listed on a GPIO pinout.
GPIO.setmode(GPIO.BCM)

# For the motor hat, the BCM pin 17 is the one for moving forward the first
# motor.
M1_F = 17

# Initialize pin 17 as output and then set it for PWN at 1000Hz.
GPIO.setup(M1_F, GPIO.OUT)
m1f = GPIO.PWM(M1_F, 1000)

# Start the motor at 80% load. It will keep running until stopped.
m1f.start(80)

print("Press CTRL+C to stop")

# Wait five minutes, or stop prematurely
try:
    sleep(300)
except KeyboardInterrupt:
    # Stop the motor
    m1f.stop()

    # Unassign all pins
    GPIO.cleanup()
