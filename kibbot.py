import os.path
from datetime import datetime, timedelta
from flask import Flask, render_template, request
import RPi.GPIO as GPIO


app = Flask(__name__)


@app.route("/")
def main_page():
    if os.path.isfile("./log.csv"):
        with open("./log.csv", "r") as f:
            feedings = [x for x in f.readlines() if "success" in x]
            feedings = [x.split(",")[0] for x in feedings]
            feedings = sorted(feedings)
    else:
        feedings = ["No feedings yet!"]
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    return render_template("main_page.html", feedings=feedings, date=date)


# To make things a bit trickier, I put the address at the current yyyymmdd
# date. This means that links expires after a short time. I hope this prevents
# misclicks on phones.
@app.route("/kib/<int:timestamp>")
def kib(timestamp):
    timestamp = str(timestamp)
    timestamp = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
    # Link expires after about a minute, ie: link must be within one
    # minute of current kibbot time
    if (datetime.now() - timestamp) / timedelta(minutes=1) > 1:

        # Save this in our logs
        with open("./log.csv", "a") as f:
            f.write(f"{datetime.now().isoformat()}, {request.remote_addr}, fail\n")

        return "Invalid kibble request", 400

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

    # Create some variables for tracking the switch in the while loop. When the
    # switch is pressed, the voltage drops and `falling` becomes True.
    old_switch = GPIO.input(16)
    consecutive = 0
    falling = None

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
            # If the signal goes from HIGH to LOW,
            # set falling to True
            if new_switch < old_switch:
                falling = True
            # If the signal goes from LOW to HIGH,
            # set falling to False
            elif new_switch > old_switch:
                falling = False
        # If we've passed the falling edge and it has
        # stayed there for 1000 cycles, terminate
        # the while loop.
        if falling and consecutive > 1000:
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
