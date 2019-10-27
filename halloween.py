import RPi.GPIO as GPIO
import threading
import time
from pygame import mixer

##
## GPIO ##
##

# GPIO PINs in BCM mode
BUTTON_PIN = 26
LEFT_LIGHT_PIN = 17
RIGHT_LIGHT_PIN = 27
MOTOR_PIN = 24

GPIO.setmode(GPIO.BCM)

##
## Servo Motor - Hat ##
##

# Motor setup
MOTOR_FREQUENCY = 50 # Hz
GPIO.setup(MOTOR_PIN, GPIO.OUT)
pwm = GPIO.PWM(MOTOR_PIN, MOTOR_FREQUENCY)
pwm = None

# Motor functions
def startMotorSequence():
  global pwm
  pwm = GPIO.PWM(MOTOR_PIN, MOTOR_FREQUENCY)
  pwm.start(0)
  time.sleep(2)
  rotate180CW()
  time.sleep(4)
  rotate180CCW()
  time.sleep(2)
  pwm.stop() # Stop PWM to avoid interference that would causes the servo motor to jitter constantly

def rotate180CW():
  global pwm
  pwm.ChangeDutyCycle(12.5)
  print "motor is rotated 180 degree"

def rotate180CCW():
  global pwm
  pwm.ChangeDutyCycle(2.5)
  print "motor is rotated -180 degree"

##
## Switch Button - Nose ##
##

# Button setup
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

##
## LED Lights - Eyes ##
## 

# Light setup
GPIO.setup(LEFT_LIGHT_PIN, GPIO.OUT)
GPIO.setup(RIGHT_LIGHT_PIN, GPIO.OUT)

# Light function
def startLightSequence():
  turnOnLights(True, False)
  time.sleep(1)
  turnOffLights(True, False)
  turnOnLights(False, True)
  time.sleep(1)
  turnOffLights(False, True)
  time.sleep(1)
  turnOnLights(True, True)
  time.sleep(1)
  turnOffLights(True, True)
  time.sleep(1)
  turnOnLights(True, True)
  time.sleep(1)
  turnOffLights(True, True)
  time.sleep(1)

def turnOnLights(left = False, right = False):
  if left: 
    turnOnLeftLight()
  if right: 
    turnOnRightLight()

def turnOffLights(left = False, right = False):
  if left: 
    turnOffLeftLight()
  if right: 
    turnOffRightLight()

def turnOnLeftLight():
  print("left light on")
  GPIO.output(LEFT_LIGHT_PIN, True)

def turnOnRightLight():
  print("right light on")
  GPIO.output(RIGHT_LIGHT_PIN, True)

def turnOffLeftLight():
  print("left light off")
  GPIO.output(LEFT_LIGHT_PIN, False)

def turnOffRightLight():
  print("right light off")
  GPIO.output(RIGHT_LIGHT_PIN, False)

##
## Speaker - Sound ##
##

# Load the wave file
mixer.init()
sound = mixer.Sound("/home/pi/Projects/Halloween/evil_laugh.wav")
sound.set_volume(1.0)

def playSound():
  print("play sound")
  global sound
  sound.play()

##
## Main Program ##
##

def executeSequence():
  thread1 = threading.Thread(target = startLightSequence)
  thread2 = threading.Thread(target = playSound)
  thread3 = threading.Thread(target = startMotorSequence)
  thread1.start()
  thread2.start()
  thread3.start()

try:
  print("program starts")

  while True:  
    GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING, 8000)
    executeSequence()
except KeyboardInterrupt:
  print("program ends")
finally:
  GPIO.cleanup()
