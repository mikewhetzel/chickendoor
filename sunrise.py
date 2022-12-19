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

#define the door raising function:
def Motor_Up():
    start_time = time.time()
    #set a 10 second timer for door to go up:
    seconds = 10
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        #if the top limit switch is triggered because the door has opened fully
        #stop the motor and print a success message with the time elapsed and the time of day the door opened:
        if GPIO.input(12) == GPIO.LOW:
            GPIO.output(37,False)
            GPIO.output(35,False)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("The door went up in " + str(int(elapsed_time))  + " seconds at " + str(current_time))
            break
        
        #start the motor to raise the door for a max of 10 seconds:
        if elapsed_time < seconds:
            GPIO.output(37,True)
            GPIO.output(35,False)
        
        #if the motor runs for more than 10 seconds:
        if elapsed_time > seconds:
            
            #if the bottom limit switch is still triggered (door hasn't moved at all after running motor for 10 seconds)
            #most likely the string between the motor and door is broken, or has come off the motor spindle
            #stop the motor and print an error message:
            if GPIO.input(11) == GPIO.LOW:
                GPIO.output(37,False)
                GPIO.output(35,False)
                print("The door is still closed. Check motor and linkage.")
                break
            
            #if the bottom limit switch is not triggered but the motor ran for 10 seconds without hitting the top limit switch
            #the limit switch could be defective and not triggering low when the door opens
            #stop the motor and print an error message:
            elif GPIO.input(11) == GPIO.HIGH:
                GPIO.output(37,False)
                GPIO.output(35,False)
                print("Malfunction with Door Opening - Please check the door and motor.")
                break              



#if the script tries to open the door but the door is already open, or the top limit switch has a short circuit or loose wire
if GPIO.input(12) == GPIO.LOW:
    GPIO.output(37,False)
    GPIO.output(35,False)
    print("Door is already open, or limit switch malfunction")

#otherwise, raise the door according to the Motor_Up() function        
elif GPIO.input(12) == GPIO.HIGH:
    Motor_Up()

#reset the GPIO pins to a default state
GPIO.cleanup()

