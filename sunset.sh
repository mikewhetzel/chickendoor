#!/bin/bash
/home/pi/.cargo/bin/heliocron wait --event sunset --offset 00:23 && /home/pi/chickendoor/sunset.py >> /home/pi/chickendoor/chickendoorlog.txt
