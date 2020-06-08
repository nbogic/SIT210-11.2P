#import needed libraries
import RPi.GPIO as GPIO
from time import sleep
import time
import requests

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#initialise the pins for each sensor/component
buzzer = 14
led = 18
TRIG = 23
ECHO = 24
d = 0

#set the sensors to input/output roles
GPIO.setup(led,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.output(TRIG,0)
GPIO.setup(ECHO,GPIO.IN)

#1= true, values to decide if the notifcations will be sent out to the user
send_notification_m = 1
send_notification_e = 1
has_beeped = False

#function: changes the truth values of the two booleans relating to the notifications (true = to be sent to IFTTT)
def send_notification(mobile, email):
    if mobile == True:
        send_notification_m = True
    if email == True:
        send_notification_e = True

#function: set up the ultrasonic distance sensor, caluclate seconds, print distance
def setup_ultrasonic(distance):
    GPIO.output(TRIG,1)
    sleep(0.01)
    GPIO.output(TRIG,0)
    
    while GPIO.input(ECHO) == 0:
        pass
    s1 = time.time()
    
    while GPIO.input(ECHO) == 1:
        pass
    s2 = time.time()
    distance = (s2 - s1) * 170
    print(distance)
    return distance

send_notification(True, True)

#loop function: repeats the ultrasonic functions, actively detects for movement, activates the led and buzzers in response, sends out notifications if specified
while True:
    sleep(0.1)
    
    if setup_ultrasonic(d) < 0.12:
        GPIO.output(buzzer,GPIO.HIGH)
        sleep(0.5)
        GPIO.output(buzzer,GPIO.LOW)
        sleep(0.5)
        GPIO.output(led,GPIO.HIGH)
        sleep(0.05)
        GPIO.output(led,GPIO.LOW)
        has_beeped = True
        
        if send_notification_m == 1:
            requests.post('https://maker.ifttt.com/trigger/alarm_on/with/key/bVyAbZpPxp5uPVQ3GDWiSg')
            send_notification_m = False
            
        if send_notification_e == 1:
            requests.post('https://maker.ifttt.com/trigger/alarm_on_e/with/key/bVyAbZpPxp5uPVQ3GDWiSg')
            send_notfification_e = False

    else:
        GPIO.output(buzzer,GPIO.LOW)
        GPIO.output(led,GPIO.LOW)
        
        if has_beeped == True:
            sleep(0.10)
            GPIO.output(led,GPIO.HIGH)
            sleep(2)
            GPIO.output(led,GPIO.LOW)

#default led state
GPIO.output(buzzer,GPIO.LOW)
     

