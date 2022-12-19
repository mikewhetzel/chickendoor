#!/bin/bash
echo $(date) >> /home/pi/chickendoor/chickendoorlog.txt
echo "System Rebooted" >> /home/pi/chickendoor/chickendoorlog.txt
/home/pi/.cargo/bin/heliocron wait --event sunrise --offset 00:23 && /home/pi/chickendoor/sunrise.py >> /home/pi/chickendoor/chickendoorlog.txt
