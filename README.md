# chickendoor
Two shell scripts that trigger individual Python scripts to control a relay-driven 12v motor to raise and lower an automated chicken coop door based on sunset/sunrise times calculated by heliocron (https://github.com/mfreeborn/heliocron).

Standard mechanical limit switches and scripted logic prevent most if not all potential catastrophes.
My limit switches are wired in the normally-closed position so that voltage is always present unless the switch is interrupted. This ensures that a loose wire, short-circuit, etc. will prevent the motor from operating. I used two 3.3v output pins from the Pi, wired into two GPIO inputs pins for the limit switches.

Logging is also implemented to keep track of door activity.

I used a Pi3B for my chicken door project, though I'm sure it could be adapted to other devices.

# Prerequisites: 
A Raspberry Pi with heliocron installed - I used the rust/cargo method to install heliocron on my Pi.

Make sure git is installed on your Pi using ```sudo apt-get install git```

Clone this repository to your Pi using ```git clone https://


# Wiring:

A 12v motor relay wired to two GPIO pins of the Pi, and a standard 12v DC motor. 

I used a simple pulley and some heavy fishing line to attach the motor to the top of the door. The motor turns one way to raise the door, which winds the string up on the pulley. To lower the door, the motor turns the opposite way to unwind the string.

Pins 35 and 37 are wired to the 12v motor relay + and -. Pin 11 is the bottom limit switch, and pin 12 is the top limit switch.

# Setup:
