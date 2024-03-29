import RPi.GPIO as GPIO

# Make it so GPIO pins by their system number,
# not their position. The two sets of numbers
# are listed on a GPIO pinout.
GPIO.setmode(GPIO.BCM)

# For the motor hat, the BCM pin 17 is the
# one for moving forward the first motor
M1_F = 17

# Initialize pin 17 as output and then set
# it for PWN at 1000Hz
GPIO.setup(M1_F, GPIO.OUT)
m1f = GPIO.PWM(M1_F, 1000)

# Set pin 16 as input, for detecting the switch
GPIO.setup(16, GPIO.IN)

# Create some variables for tracking the 
# switch in the while loop. When the switch
# is let go, the voltage rises and `rising`
# becomes True.
old_switch = GPIO.input(16)
consecutive = 0
rising = None

# Start the motor at 80% load. It will keep
# running until stopped.
m1f.start(80)

while True:
    # Read the signal from the switch
    new_switch = GPIO.input(16)
    # If the signal is the same as before,
    # increment this counter
    if new_switch == old_switch:
        consecutive += 1
    # Otherwise start counting again
    else:
        consecutive = 0
        # If the signal goes from LOW to HIGH,
        # set rising to True
        if new_switch > old_switch:
            rising = True
        # If the signal goes from LOW to HIGH,
        # set rising to True
        elif new_switch < old_switch:
            rising = False
    # We've passed the rising edge and it has 
    # stayed there for 100 cycles, terminate
    # the while loop.
    if rising and consecutive > 100:
        break
    # Otherwise, save the switch value and
    # continue the loop.
    old_switch = new_switch

# Stop the motor
m1f.stop()

# Unassign all pins
GPIO.cleanup()
