#!/usr/bin/env python3
import os
import RPi.GPIO as GPIO
import time
from datetime import datetime

#pin setup - limit switches are wired NC so a loose wire or short will prevent the motor from operating
#note that because limit switches are NC not NO, a GPIO LOW value means the door has triggered the switch:
#pins 35 and 37 are wired to the 12v motor relay
#pin 11 is the bottom limit switch, and pin 12 is the top limit switch
GPIO.setmode(GPIO.BOARD)
GPIO.setup(35,GPIO.OUT)
GPIO.setup(37,GPIO.OUT)
GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)

#define the door lowering function:
def Motor_Down():
    start_time = time.time()
    #set a 6 second timer for door to go down:
    seconds = 6
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        #if the bottom limit switch is triggered because the door has closed fully
        #stop the motor and print a success message with the time elapsed and the time of day the door closed:
        if GPIO.input(11) == GPIO.LOW:
            GPIO.output(37,False)
            GPIO.output(35,False)
            print("The door went down in " + str(int(elapsed_time)) + " Seconds at " + str(current_time))
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            break
        
        #start the motor to lower the door for a max of 6 seconds:
        if elapsed_time < seconds:
            GPIO.output(35,True)
            GPIO.output(37,False)
        
        #if the motor runs for more than 10 seconds:
        if elapsed_time > seconds:
            
            #if the top limit switch is still triggered (door hasn't moved at all after running motor for 6 seconds)
            #the door or motor could be stuck in a door-open position
            #stop the motor and print an error message:
            if GPIO.input(12) == GPIO.LOW:
                GPIO.output(37,False)
                GPIO.output(35,False)
                print("The door is still open. Check motor and linkage.")
                break
            
            #if the top limit switch is not triggered but the motor ran for 6 seconds without hitting the bottom limit switch
            #the limit switch could be defective and not triggering low when the door closes
            #stop the motor and print an error message:
            elif GPIO.input(12) == GPIO.HIGH:
                GPIO.output(37,False)
                GPIO.output(35,False)
                print("Malfunction with Door Closing - Please check the door and motor.")
                break              


#define a function to very briefly bump the motor down after it has fully closed, in order to extend the gravity operated door locking tabs
def Lock_Door():
    start_time = time.time()
    seconds = 0.65
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time < seconds:
            GPIO.output(35,True)
            GPIO.output(37,False)
            
        elif elapsed_time > seconds:
            GPIO.output(37,False)
            GPIO.output(35,False)
            break


#if the script tries to open the door but the door is already open, or the top limit switch has a short circuit or loose wire
if GPIO.input(11) == GPIO.LOW:
        GPIO.output(37,False)
        GPIO.output(35,False)
        print("Sunset door closing canceled. The door is already closed, or a limit switch has malfunctioned.")

#otherwise, lower the door according to the Motor_Down() function, then lower for another 0.65 seconds to lock the tabs into place
elif GPIO.input(11) == GPIO.HIGH:
    Motor_Down()
    Lock_Door()

#reset the GPIO pins to a default state
GPIO.cleanup()

