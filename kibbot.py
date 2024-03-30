import os.path
from datetime import datetime
from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import RPi.GPIO as GPIO


app = Flask(__name__)

# Set a common limiter for all IP addresses, normally the limiter is separate
# for each one.
limiter = Limiter(lambda: "127.0.0.1",
                  app=app)

# Make it so GPIO pins by their system number, not their position. The two sets
# of numbers are listed on a GPIO pinout.
GPIO.setmode(GPIO.BCM)

# For the motor hat, the BCM pin 17 is the one for moving forward the first
# motor.
M1_F = 17

# Initialize pin 17 as output and then set it for PWN at 1000Hz.
GPIO.setup(M1_F, GPIO.OUT)
m1f = GPIO.PWM(M1_F, 1000)

# Set pin 16 as input, for detecting the switch
GPIO.setup(16, GPIO.IN)

@app.route("/")
def main_page():
    if os.path.isfile("./log.csv"):
        with open("./log.csv", "r") as f:
            feedings = [x for x in f.readlines() if "success" in x]
            feedings = [x.split(",")[0] for x in feedings]
            feedings = sorted(feedings)
    else:
        feedings = ["No feedings yet!"]
    date = datetime.now().strftime("%Y%m%d%H%M")
    return render_template("main_page.html", feedings=feedings, date=date)

# To make things a bit trickier, I put the address at the current yyyymmdd
# date. I also add a limiter of 5 minutes. It takes a cat about 3 minutes to
# eat a serving.
@app.route("/kib/<int:today>")
@limiter.limit("1 per 5 minute")
def kib(today):
    if today != int(datetime.now().strftime("%Y%m%d%H%M")):

        # Save this in our logs
        with open("./log.csv", "a") as f:
            f.write(f"{datetime.now().isoformat()}, {request.remote_addr}, fail\n")

        return "Invalid kibble request", 400
    # Create some variables for tracking the switch in the while loop. When the
    # switch is let go, the voltage rises and `rising` becomes True.
    old_switch = GPIO.input(16)
    consecutive = 0
    rising = None

    # Start the motor at 80% load. It will keep running until stopped.
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

    # Save this in our logs
    with open("./log.csv", "a") as f:
        f.write(f"{datetime.now().isoformat()},{request.remote_addr},success\n")
    
    return "Successful kib!", 200
