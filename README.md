# Kib Bot

## Your cats' best friend

The Kib Bot is a Raspberry Pi that's been wired into an automatic pet food dispenser. The Pi gives you control of the feeder's motor, so you can decide when you give kibble.

![Inside of food dispenser](./images/inside_pi.jpg)

The python code gives you a simple web interface that has a button that gives food when you click it.

![Web interface](./images/web_interface.jpg)

Setting up your feeder this way gives you a whole more lot control over it. It's not easy to connect it to the internet, and you don't have to use an app that comes from the manufacturer. You can do more complicated stuff with it. For example, you can connect the feeder to a VPN and your home surveillance system, so that you can see if the cats are hungry before feeding them.

![Photo of two cats both trying to eat from the automatic feeder](./images/cat_crowd.jpg)

... the feeder might be *very* popular ...

If you like cats and you're looking for a nice and easy hardware hacking project, give the Kibbot a try!

## How difficult is this project?

I think it's a pretty forgiving project, but you'll need to push yourself a bit if you're new to electronics.

What makes this project easy is that an automatic feeder is a simple machine. It's just a motor in a plastic housing. And luckily, motors are something very well supported in hobbyist electronics. You can order all of the parts online.

But what makes this hard is that it'll cost you about $100 in parts, some of which you will destroy to improve. That can be hard to do. And if you make a mistake, you can break things permanently. That feels wasteful. Also if your automatic feeder is different from mine, you'll have to figure it out yourself, and that can be tricky.

You can make this all easier by having the right tools. I found that having a Dupont connector crimper meant that I didn't need to do soldering. Not having to do soldering is great because it's not for everyone and besides the equipment is at least $100. A crimper and a Dupont connector kit is only about $50.

So, I think making the Kibbot is a good beginner hardware hacking project.

## Shopping list

Here's what I used.

For parts

  * A [Yoposl automatic cat feeder](https://www.amazon.ca/Yuposl-Automatic-Cat-Feeders-Dispenser/dp/B0C2JBBQKR?th=1)
  * A Raspberry Pi Zero 2 W (you will need a micro SD card too)
  * A Raspberry Pi Motor Controller HAT
  * A miniature breadboard
  * A Dupont connector kit
  * A variety of premade Dupont wires, to extend or repair connections
  * A collections of spacers for the Raspberry Pi, to secure it

For the automatic feeder, you just need a basic model with a plastic structure, a motor and such. You'll be bypassing its built-in controls, so anything fancy you won't actually use.

As for tools

  * A multimeter
  * A Dupont connector crimper
  * A hot glue gun
  * Screwdrivers (my automatic feeder needs a very long Phillips screwdriver to reach deep screws)


## Installation

### Software

The code is set up as a Flask app.

On a Raspberry Pi, you'll have to install some software first, pip, venv and git

```
apt install python3-pip python3-venv git
```

Then, clone this code in a folder with `git clone`. You can then setup the virtual environment and install the packages in the requirements file.

```
cd kibbot
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

To start the web server in development mode,

```
. .venv/bin/activate
flask --app kibbot run --host=0.0.0.0
```

To run using a better server, use

```
. .venv/bin/activate
gunicorn -w 1 -b 0.0.0.0:5000 kibbot:app
```

Just make sure to only use one worker so that there aren't multiple requests at once to the dispenser. With only one worker, requests run in sequence, and the motor will keep running until it's completed all of them.

## Deep dive

### How the automatic feeder works

My automatic feeder is a motor that spins a drum that takes in kibble and dispenses it in portions. The drum has three rounded corners that press a switch, which is how the machine knows the position of the drum. One full spin of the drum gives out three portions.

The feeder has a screen and some buttons for either automatically feeding portions on a schedule or for doing manual feedings. The screen locks after a short period. I'm guessing that's to make it harder for an animal to operate the machine with their noses. And they will try. I've seen it. Nope. No free lunch.

![Photo of automatic feeder dispensing food, with LCD screen shown](./images/front_feeder.jpg)

The feeder has a small coin cell battery to keep the time when powered off. It's also possible to power the machine with three D batteries, as a battery backup. I never bothered because I'd have to regulate the batteries to 5V, but it's something you could definitely do with the right parts.

The feeder is fed by a small 5V 1A charger. The drum motor also runs at 5V. The switch is 3V, so the logic is probably 3.3V. This is worth remembering when playing around with the circuitry.

[To check all of these, connect your multimeter's negative terminal to the feeder's ground. Then connect the positive terminal to the parts you want to measure. Alligator clips or "EZ" clips make this a lot easier.]

### Hardware strategy

My strategy is to take an existing automatic feeder and replace its internals with my own stuff. This way most of my work is already done for me.

A Raspberry Pi computer with a motor controller is ultimately equivalent to the feeder's electronics. It accepts 5V as its power input so it can drive the motor at that voltage through the motor controller. Its logic is at 3.3V so it's able to read the switch the same way.

### Tools and hardware

I used a [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/), the cheapest in-stock board I could find. A Pico W would also work, but it's just so much easier (and fun) to use a full Linux machine.

![A comparison of Raspberry Pi](./pi_comparison.jpg)

Note: the Raspberry Pi Zero product line does not have a protective fuse, so make sure to give it 5V only. I've fried a Pi Zero by plugging it to a fast-charging phone charger, the kind that can go to 12V. I'm not sure why the fast-charge mode activated, so I've stuck to regular 5V chargers ever since.

I use the [Pi Motor Controller HAT](https://www.pishop.ca/product/raspberry-pi-motor-controller-hat/) to control the motor from the Pi. The hat is just a motor control chip that connect to some of the Pi's pins. Any other motor controller should work. Only one channel is needed because the single motor only ever goes forward. The ability to supply a separate 5V voltage is necessary since the motor runs at 5V not the 3.3V of the Pi's GPIO. In our case, the feeder already has 5V, so we just use that.

Note: only power a motor from the Pi's 5V pins. These are the raw power source. Powering it from different pins will probably cook your Pi.

![Photo of motor pi and Pi Zero 2W](./images/motor_and_pi.jpg)

La pièce de résistance is my Dupont connector kit and crimper. This has made everything very easy. With the kit, I could just cut the feeder's wires, put Dupont connectors on the ends, and plug them wherever I wanted. I use both male and female connectors. Male connectors will plug in breadboards and screw terminals, and female sockets are needed for the Pi's GPIO pins. It's a good idea to have an assortment of pre-made Dupont connectors too, in all the colours of the rainbow so you can tell what's what.

A hot glue gun and a Raspberry Pi spacer kit are helpful too for securing components in place.

![Photo collage of crimper tool with kit, hot glue gun, spacers, extra Dupont wires](./images/extra_tools.jpg)

It's a really good idea to have a multimeter so that you can check your feeder's circuitry. This is my first hardware hack, and it's a pretty basic one; nevertheless, I think it's a good idea to check and write yourself some notes too. The manufacturer may designed things in a way you don't expect. Different connectors for your multimeter are helpful: alligator clips and "EZ" clips should be able to latch onto most things.

Another helpful thing to have is a camera so that you can take photos of the feeder's teardown, in case you forget how to put it all back together. It's also really good to have a record of what the dispenser looked like when it was operating, in case you destroy it. For example, it's easy to have the motor running in the wrong direction. Keeping a video will help prevent that.

### Taking it apart

Most pieces of the feeder come apart easily.

Separating the motor's drum structure was a challenge. At first I thought it was held by plastic clips, but no matter how hard I tried, I could not pry it loose. I then wondered if the things were held by screws after all. It turned out they were hidden under the feeder's rubber pad or feet. By ripping these off I could remove the four screws and the feeder came apart. So, be patient and check around before your tear down turns into a literal tearing apart of plastic.

![Photo of inside the automatic feeder](./images/feeder_inside.jpg)

Inside, wires are soldered to terminals, and there is what looks like a JST header hot-glued to the main board.

There is a white wire heading from the 3 D batteries to the board.

There are pairs of wires each going to the motor and to the lever switch. The motor's rotating structure has corners that press on the switch three times during each complete spin.

To take this apart, I just cut all the wires at about midpoint. This left me with

  * disconnected main board.
  * red voltage and black ground
  * yellow positive and grey negative for the motor
  * black ground for the switch's input and blue wire for the returning signal

I finished all the cut wire ends with Dupont connectors. This way I can easily rewire the feeder back to its original state. It didn't really matter whether they were male or female connectors. I've plenty of either kind to connect them.

### Putting together the new board

Putting together the new Raspberry Pi setup is not hard if you have the parts. We just need to control the motor and read the switch to determine the motor's position.

Before that we need to power things. The power supply can be connected to the Pi's 5V and ground pins. On the Pi Zero, these pins are connected to the Pi's power rails, so they're okay to use this way. If this isn't to your liking, I see two alternatives. One: run a 5V power supply with the right connector for your Pi through a hole the back of the feeder case. Two: wire your own USB power connector to the voltage and ground in the feeder. You can find USB breakout boards for [micro-B USB](https://www.sparkfun.com/products/10031) and [USB-C](https://www.sparkfun.com/products/23055) to make your life easier.

The motor can be connected to a Motor Pi Hat. Put the hat on the Pi, secure the motor's wires into the screw terminal, and feed 5V into the controller's own power. These "hats" are made to stack one on top of the other, so they're easy to use.

![Photo and diagram of switch connection to the Pi](./images/switch_circuit.png)

The switch in the feeder drives its output to ground when pressed, so you'll need to drive your Pi's digital input pin high to 3.3V volt with a pull-up resistor (I use 4.7kohm). What this all means is that when the switch is not pressed, your Pi will read ON or HIGH at 3.3V. When the switch is pressed, the connection to ground will drive your input pin to OFF or LOW along with it: this is thanks to the pull-up resistor that will "weaken" the 3.3V so that the ground signal can easily overwhelm it.

There's an extra wrinkle though: the switch will be noisy, meaning that it'll bounce around HIGH and LOW as it switches (or just when it feels like it). This means that it'll be hard to detect what the switch is really doing. The noise can be reduced with a 0.1 uF ceramic capacitor accross the the input pin and the ground (one leg of the capacitor on the digital pin, the other leg on the ground). The capacitor will even out the power fluctuations. Still, it's worth making your Python code wait a few cycles to make sure a change between HIGH and LOW is genuine, which I show later.

(I've never been good at diagnosing these noise issues. To do a better job I'd need an oscilloscope to measure the fluctuations' frequencies. That would let me select the right capacitor to filter it. A multimeter doesn't update nearly fast enough to get the frequency of the noise from the switch. Oscilloscopes take measurements more than a million times per second and graph them for you. That's what you need to do a nice clean job.)

### Software strategy

I'll explain how the software works to control the Kibbot.

I use a very simple Flask server. This puts the the Kibbot on the LAN, and if you have a VPN configured, it also opens it up to distant remote control.

Flask is a simple web server. When a visitor requests a URL, the server runs the appropriate Python code. If the user requests a URL or path that does not exist, the server returns an error. So Flask creates a website with some Python code living inside, and you can make it do all sorts of things.

The Kibbot simply needs to have a page with a link to dispense food. When the visitor clicks the link, the bot dispenses a portion. On the server, Python accesses the Raspberry Pi's GPIO pins. These pins are connected to the motor and the switch, so Python can drive the motor and stop it when done.

Controlling the motor is not difficult, thanks to the Motor Pi Hat. The board's GitHub repo has [an example](https://github.com/modmypi/SN754410NE-Motor-Controller/blob/master/pwm_motor.py) you can easily adapt and use. The RPi.GPIO library already has all it needs, and no extra libraries are necessary. Once the pins are assigned, the code can set the motor's speed. When it's time to stop, the `.stop()` method is called.

```python
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

# Stop the motor
m1f.stop()
```

Reading the switch isn't difficult, but making use of the signal requires a bit of work.

First, we're interested in the falling edge of the switch's signal, meaning that we want to know when the switch goes from HIGH (unpressed) to LOW (pressed). (Remember that the switch is connected to ground so that it drives the signal low when pressed.) We need a while loop that compares the current signal against the one from the previous loop.

```python
# Create some variables for tracking the switch in the while loop. When the
# switch is pressed, the voltage drops and `falling` becomes True.
old_switch = GPIO.input(16)
consecutive = 0
falling = None

while True:
  # Read the signal from the switch
  new_switch = GPIO.input(16)

  # If the signal goes from HIGH to LOW,
  # set falling to True
  if new_switch < old_switch:
    falling = True
  # If the signal goes from LOW to HIGH,
  # set falling to False
  elif new_switch > old_switch:
    falling = False

  old_switch = new_switch
```

Second, the signal is noisy despite the capacitor. It'll bounce between HIGH and LOW as the switch is pressed. While it might be possible to clean up the signal more, there's a cheap solution. The code can wait to see if the signal stays LOW for 1,000 cycles after it detects the falling edge. This creates a tiny delay before the motor stops but it's fairly reliable.

```python
while True:
  # [...]

  # If the signal is the same as before,
  # increment this counter
  if new_switch == old_switch:
      consecutive += 1
  # Otherwise start counting again
  else:
      consecutive = 0

  # If we've passed the falling edge and it has
  # stayed there for 1000 cycles, terminate
  # the while loop.
  if falling and consecutive > 1000:
      break
```

With these two things together, the motor control and the switch logic, the web server can dispense portions of food when the link is clicked.

There are two other things to do: include a log and protect against accidental feedings.

A log is easily made by saving the time of each request to a comma-separated values file (or CSV). This kind of file is very simple and can be written to without much trouble. When the webpage is displayed, the file is read, parsed and sorted to give the history log. This way you have some idea how often you're feeding your cats.

```python
# During a feeding, save this in our logs
with open("./log.csv", "a") as f:
    f.write(f"{datetime.now().isoformat()},{request.remote_addr},success\n")

# When displaying the page
if os.path.isfile("./log.csv"):
    with open("./log.csv", "r") as f:
        feedings = [x for x in f.readlines() if "success" in x]
        feedings = [x.split(",")[0] for x in feedings]
        feedings = sorted(feedings)
```

You can protect against accidental feedings a few ways. You can make the links expire after a short amount of time. In our case, we can just put a timestamp at the end of each link and check that the timestamp is recent when the request is received. If a request uses a timestamp that's too old, the request fails. The `datetime` standard library makes this easy with its time deltas, [particularly their ability to divide each other](https://docs.python.org/3/library/datetime.html#datetime.timedelta.total_seconds). By subtracting the timestamp from the current time, we get a delta we can divide by `timedelta(minutes=1)` to get the difference in minutes. If the result is greater than 1, return an error and give no kibs.

```python
@app.route("/kib/<int:today>")
def kib(today):
    # Link expires after about a minute, ie: link must be within one
    # minute of current kibbot time
    if (int(datetime.now()) - datetime.fromisoformat(today)) / timedelta(minutes=1) > 1:
      return "Invalid kibble request", 400
```

Another way is to use the [`flask-limiter`](https://flask-limiter.readthedocs.io/en/stable/) library to limit how frequently a route can be used.

### Installing the software

To install the software on your Raspberry Pi, you'll need to SSH into it so that you can control it. The Raspberry Pi webiste has [a guide](https://www.raspberrypi.com/documentation/computers/remote-access.html) to show you how to do this.

Once you're in control of the Raspberry Pi, start by installing some system dependencies. Git is needed to download the code to your computer. Pip and venv are there to intall and manage your Python packages.

```
apt install git python3-pip python3-venv
```

Then, clone this code in a folder with `git clone`.

```console

```

You can then setup the virtual environment and install the packages in the requirements file.

```
cd kibbot
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

To start the web server in development mode,

```
. .venv/bin/activate
flask --app kibbot run --host=0.0.0.0
```

To run using a better server, use

```
. .venv/bin/activate
gunicorn -w 1 -b 0.0.0.0:5000 kibbot:app
```

## Extras

### VPN

A VPN lets you connect to the kibbot away from home. Normally you can only connect to it from your home LAN, but with a VPN, you're not constrained by that.

These days privacy VPNs are very popular. They let you mask your internet connect. The kind of VPN I'm talking about is different. It's like a company VPN you use to connect to the office at home.  It's the kind of VPN that lets you be somewhere else.

I use Tailscale. It's free and encrypted using Wireguard. The only set up necessary is installing taiscale on your Kibbot and your remote control computer.

First, create an account and install it on your computer. This will give you a dashboard for controlling your VPNs' other devices. You can install tailscale on your phone too.

For the Raspberry Pi, you can find the [latest instructions](https://tailscale.com/download/linux/rpi-bullseye) on their website.

```console
sudo apt-get install apt-transport-https

curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bullseye.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg > /dev/null
curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bullseye.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list

sudo apt-get update
sudo apt-get install tailscale

sudo tailscale up

tailscale ip -4
```

You can keep the Kibbot's tailscale IP address in your favourites and access it that way. 

### A systemd service

It's very convenient to have the Flask server start automatically whenever the Kibbot is plugged in. You can do this with a systemd service that starts the server when Linux starts. This means you don't have to SSH into the Kibbot each time you want to start it.

You can find a good guide [here](https://github.com/torfsen/python-systemd-tutorial) for turning a Python script into a systemd service.

Place the following in `~/.config/systemd/USER/kibbot.service`

```
[Unit]
Description=Kib Bot food dispenser
After=network.target

[Service]
WorkingDirectory=/home/ubuntu/kibbot
ExecStart=/home/ubuntu/kibbot/.venv/bin/gunicorn -b 0.0.0.0:5000 -w 1 kibbot:app
Environment=PYTHONUNBUFFERED=1
Restart=on-failure

[Install]
WantedBy=default.target
```

Then run these commands to start it

```
systemctl --user enable kibbot
systemctl --user start kibbot
```

You also have to run this command to let the service continue even when you aren't logged in

```
sudo loginctl enable-linger $USER
```

### A bash script for remote trigger

You can access the flask server from something other than a web browser. A bash script can make the GET request to trigger the feeding.

```bash
#!/bin/bash
page=$(date +%Y%m%d%H%M%S)

wget -O- http://192.168.xxx.xxx:5000/kib/${page}
```

The above script can be used in Motioneye to [add an action button](https://github.com/motioneye-project/motioneye/wiki/Action-Buttons) to start a feeding. You can feed your cats while spying on them. Since this technique generates the timestamp from the remote machine's time, it may be too far off from the Kibbot's and could always return a failure.

### Final thoughts

The Pi can do a whole lot of other things. You could add a camera, a speaker, or maybe a water fountain to your automatic feeder. With some wheels it would have extra mobility to run away from your cats. You know, for a bit of exercise.

## Questions? Comments?

If you have any questions or comments, feel free to reach out to me.

Hope you enjoyed this!
