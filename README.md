# chickendoor
Two shell scripts that trigger two Python scripts to control a relay-driven 12v motor to raise and lower an automated chicken coop door. Timing is based on sunset/sunrise times calculated by heliocron (https://github.com/mfreeborn/heliocron).

My chicken door Pi is connected to Wifi, but this system should work offline as long as the system date and clock remain accurate.

Standard mechanical limit switches and scripted logic prevent most if not all potential catastrophes.
My limit switches are wired in the normally-closed position so that voltage is always present unless the switch is interrupted. This ensures that a loose wire, short-circuit, etc. will prevent the motor from operating. I used two 3.3v output pins from the Pi, wired into two GPIO input pins for the limit switches.

Logging is also implemented to keep track of door activity.

I used a Pi3B for my chicken door project, though I'm sure it could be adapted to other devices.

# Prerequisites: 
A Raspberry Pi with heliocron installed - I used the rust/cargo method to install heliocron on my Pi.
Be sure to add a configuration file to heliocron and plug in the latitude and longitude for your location, as described in the heliocron documentation.

Make sure git is installed on your Pi using ```sudo apt-get install git```

Clone this repository to your Pi using ```git clone https://github.com/mikewhetzel/chickendoor.git```


# Wiring:

A 12v motor relay wired to two GPIO pins of the Pi, and a standard 12v DC motor. 

I used a simple pulley and some heavy fishing line to attach the motor to the top of the door. The motor turns one way to raise the door, which winds the string up on the pulley. To lower the door, the motor turns the opposite way to unwind the string.

Pins 35 and 37 are wired to the 12v motor relay + and - terminals. Pin 11 is the bottom limit switch, and pin 12 is the top limit switch.

# Setup:
We want to set up the Pi to reboot every morning at 3am, in order to run a new instance of the scripts each day. I accomplished this by using the crontab, a good way to run scheduled jobs on a Pi.

Edit the Pi's system-wide crontab using the command ```sudo crontab -e```. We need root user permission here in order to reboot the whole system.

Add the following to the end of the root user crontab in order to reboot every morning at 3am:
```0 3 * * * /sbin/shutdown -r now```

Now, save and exit the editor.

The next thing we need to do is tell the Pi to run both the sunrise.sh and sunset.sh shell scripts every time the Pi reboots. The shell scripts will tell the Pi to wait until 23 minutes after sunrise, and then run the sunrise.py Python script to open the door. Similarly, it will do the same 23 minutes after sunset with the sunset.py script to close the door after sunset.

To do this, I added the following two lines to the end of the pi user crontab with the command ```crontab -e```:

```
@reboot /home/pi/chickendoor/sunrise.sh
@reboot /home/pi/chickendoor/sunset.sh
```

Save and exit the editor. Now, we need to make the shell and python scripts executable. I accomplished this with the commands:
```
chmod +x /home/pi/chickendoor/sunrise.sh
chmod +x /home/pi/chickendoor/sunset.sh
chmod +x /home/pi/chickendoor/sunrise.py
chmod +x /home/pi/chickendoor/sunset.py
```

Now, the timed raising and lowering of the door should be working. The timing can be modified by changing the offset of the heliocron command in the sunrise.sh and sunset.sh scripts, as described in the heliocron documentation. It's easiest to test the scripts by doing a ```heliocron report``` command, comparing the current time to the time of sunrise or sunset in the heliocron report, and adjusting the offset in the shell scripts accordingly.

Happy chickening!
