'''
THE SINGING TREE CODE
    This code was for a community engagement event in 2016. The code was run on a Raspberry Pi Model B+. 
    It receives input using the Pi's GPIO pins from four PIR sensors and uses pygame to mix the audio from four different sound files. 
    Moving around the tree structure casues different pitches to be played. This allows someone to make rudimentary music.
    
    Project homepage can be found here:
        https://hackaday.io/project/161498-the-singing-tree
'''

import RPi.GPIO as GPIO
import time
import pygame

# Function definitions
def updateState(pastState, newState, note):
    # This functions updates the state of a single sensor. Output is the sensor's current state.
    if pastState != newState:
        print(str(newState))
        if newState:
            state = "High"
            note.play()
        else:
            state = "Low"
            note.fadeout(2000)
        return state
    else: return 'High' if pastState else 'Low'

def testSound(noteLs):
    # Tests the sound output of the four .wav files (Check volume here!)
    print("Testing single files...")
    for i in noteLs:
        i.play(fade_ms = 1)
        time.sleep(3)
        i.fadeout(1000)
        time.sleep(1)
    
    print("Testing all...")
    for i in noteLs:
        i.play(fade_ms = 1)
        time.sleep(4)
    print("Done testing.")
    [i.fadeout(1000) for i in noteLs]

# Pygame initialization.
pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.mixer.init()
pygame.init()

# Sound file import 
c = pygame.mixer.Sound("eh1.wav")
e = pygame.mixer.Sound("eh3.wav")
g = pygame.mixer.Sound("eh5.wav")
c8ve = pygame.mixer.Sound("eh8.wav")
ntLs = [c, e, g, c8ve]

# Sound test
testSound(ntLs)

# Sensor/Pin initialization
GPIO.setmode(GPIO.BCM)
sensor0 = 5
sensor1 = 18
sensor2 = 22
sensor3 = 27
snsrLs = [sensor0, sensor1, sensor2, sensor3]

for i in snsrLs:
    GPIO.setup(i,GPIO.IN, GPIO.PUD_DOWN)

# Even numbers will be past states. Odd numbers will be current state.
stateLs = ["Low"] * 8


print("Singing Tree is singing..")
while True:
    time.sleep(0.1)
    i = 0
    while i < 8:
        snsr = snsrLs[i//2]
        stateLs[i] = stateLs[i + 1]
        stateLs[i + 1] = GPIO.input(snsr)
        st = updateState(stateLs[i], stateLs[i + 1], ntLs[i//2])
        print("GPIO pin {} is {}".format(snsr,st))
        i += 2