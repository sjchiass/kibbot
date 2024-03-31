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

## Deep dive

### How the automatic feeder works

My automatic feeder is a motor that spins a compartmentalized drum that collects the pet food and dispenses it in portions. There are three protuding rounded corners that presses a switch, which is how the machine knows the position of the drum. One full revolution of the drum dispenses three portions.

The feeder has a screen and some buttons for either automatically feeding portions on a schedule or for initiating manual feedings. The screen locks after a short period. I'm guessing that's to make it harder for a pet to operate the machine.

The feeder has a small coin cell battery to keep the time when powered off. It is also possible to power the machine with three D batteries, like a battery backup.

The feeder is fed by a small %V 1A charger. This is also the voltage the motor runs at. The switch is 3V, so the logic is thereabouts 3.3V. This is worth remembering when playing around with the circuitry.

### Strategy

A Raspberry Pi computer with a motor controller is ultimately equivalent to the feeder's electronics. It accepts 5V as its power input so it can drive the motor at that voltage. Its logic is at 3.3V so it's able to read the switch the same way.

The Pi has the advantage of being a computer able to run Python and a web server. It can also connect to the internet by wifi. Other add-ons are possible, like a camera, a speaker and a sensor for detecting pellet levels in the reservoir.

### Tools and hardware

I used a Raspberry Pi Zero 2 W, which is the cheapest in-stock board I could find. A Pico W would also work, but it's just so much easier (and fun) to use a full Linux machine.

I use the motor pi hat to control the motor from the Pi. The hat is simply a motor control chip that connect to some of the Pi's pins. Any other motor controller should work. Only one channel is neeeded. The ability to supply a separate 5V voltage is necessary since the motor runs at 5V not the 3.3V of the Pi's GPIO.

La piece de resistance is my dupont connector kit and crimper. This has made everything very easy. With the kit, I was simply able to cut the feeder's wires, put dupont connectors on their ends, and plug them wherever I needed. I use both male and female connectors. Male connectors will fit in breadboards and screw terminals, and female connectors are needed for the Pi. It's a good idea to have an assortment of pre-made Dupont connectors, male-male, male-female, female-female, in case you need to extend a connection or change its connector.

Last but not least, it's a really good idea to have a muiltimeter so that you can check your feeder's circuitry. This is my first hardware hack, and it's a pretty basic one; nevertheless, I think it's a good idea to check and write yourself some notes on paper. The manufacturer may designed things in a way you do not expect.

Anoter helpful thing to have is a camera so that you can take photos of the feeder's assembly, in case you forget how to put it all back together.