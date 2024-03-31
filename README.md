# Kib Bot

## Your cats' best friend

The Kib Bot is a Raspberry Pi integrated into a pet food dispenser. It lets you operate the feeder remotely. It can be modified to perform other functions, like logging and authentication.

Connect the Kib Bot to your VPN and operate it away from home!

### Requirements

This code will run off of a Raspberry Pi single-board computer that is able to run Flask. It also requires some kind of pet food dispenser, one that you've modified to connect to the Raspberry Pi.

The code uses RPi.GPIO through a motor controller. It could be run on a different machine as long as it's able to control a motor.

The code also needs to be able to read a pin, assuming your food dispenser uses a switch to detect the motor's position.

### Installation

#### Hardware

I used a Yoposl automatic cat feeder I bought off of Amazon.

Place the motor hat on your Raspberry Pi.

Connect the switch to BCM pin 16. Make sure that the switch drives the voltage low when engaged. I feed pin 16 3.3V through a 4.7k ohm resistor. Check with a multimeter what your pet feeder does. You may be able to simply tap into its wiring to get the switch signal.

#### Software

The code is setup as a Flask server.

On a Raspberry Pi, you will have to install some software first.

```
apt install python3-pip python3-venv
```

Then, clone this code in a folder with `git clone`. You can then setup the virtual environment and installed the required packages.

```
cd kibbot
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

In order to start the web server in development mode,

```
flask --app kibbot run --host=0.0.0.0
```

To run using a better server, install gunicorn with `pip install gunicorn`, then use

```
gunicorn -w 1 "kibbot:app"
```

Make sure to only use one worker so that there are not multiple requests at once to the dispenser. **Test whether flask-limiter works with multiple workers**
