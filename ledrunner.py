'''
LEDrunner
v1.0b
By Philipp D.
May 2024
'''

import RPi.GPIO as gpio
import board
import neopixel
from time import sleep


# All the sequences that can be played
GAMES = [
    [1,2,3,3,2,1,3,2,3,1,3,1,3,2,3,2,1,2,2,1,3,3,3,1]
]


# Setup the buttons
PINRED = 23; PINGREEN = 24; PINBLUE = 25
gpio.setmode(gpio.BCM)
gpio.setup(PINRED, gpio.IN, gpio.PUD_UP)
gpio.setup(PINGREEN, gpio.IN, gpio.PUD_UP)
gpio.setup(PINBLUE, gpio.IN, gpio.PUD_UP)

# Setup the LEDs
PINPIXELS = board.D18
AMOUNTPIXELS = 8
USEDPIXELS = 8
# Set brightness to a low number so no external supply is required
pixels = neopixel.NeoPixel(PINPIXELS, AMOUNTPIXELS, brightness=0.01)
for i in range(8):
    pixels[i] = (0,0,0)


# "Moves" the lights on the strip
def update(lst, active):
    global pixels
    for i in range(USEDPIXELS):
        pixels[i] = (0,0,0)
    leds = lst[active:(active+USEDPIXELS)]
    for i in range(len(leds)):
        if   leds[i] == 0: pixels[i] = (0,0,0)
        elif leds[i] == 1: pixels[i] = (255,0,0)
        elif leds[i] == 2: pixels[i] = (0,255,0)
        elif leds[i] == 3: pixels[i] = (0,0,255)
        

# Checks if the player is pressing the correct button
def check(active):
    if gpio.input(PINRED) == gpio.LOW and gpio.input(PINGREEN) == gpio.LOW:
        return False
    buttonPressed = 0
    if gpio.input(PINRED) == gpio.LOW:   buttonPressed += 1
    if gpio.input(PINGREEN) == gpio.LOW: buttonPressed += 2
    if gpio.input(PINBLUE) == gpio.LOW:  buttonPressed += 3
    return (buttonPressed == active)
        
    
game: list  # The currently active sequence
delay: float  # Time the player has to react
wrong: int  # Mistakes the player did

print("Hello, and welcome to")
print("|       -----   +--\\")
print("|               |   \\")
print("|       -----   |    |")
print("|               |   /")
print("+----   -----   +--/")
print("R   U   N   N   E   R")
print("Hold the button with the color of the LED at the bottom to earn points! Good luck!")
while True:
    print("Press any button to play!")
    c = 0  # Shift of idle sequence
    p = 0  # Only start when the player has pressed and left a button
    while p < 3:
        noButtonPressed = (gpio.input(PINRED) == gpio.HIGH) and (gpio.input(PINGREEN) == gpio.HIGH) and (gpio.input(PINBLUE) == gpio.HIGH)
        if p == 0 and noButtonPressed:
            p = 1
        if p == 1 and not noButtonPressed:
            p = 2
        if p == 2 and noButtonPressed:
            p = 3
        # Show a scrolling idle sequence
        update([1 + i%3 for i in range(3*USEDPIXELS)], c)
        if c >= USEDPIXELS: c = 0
        else: c += 1
        sleep(0.1)

    # The zeroes at the beginning and end of the list serve as buffers to avoid list overflows and to make the start easier
    game = [0 for _ in range(USEDPIXELS)] + GAMES[0] + [0 for _ in range(USEDPIXELS)]
    delay = 0.5
    
    wrong = 0
    
    # Countdown
    for i in range(USEDPIXELS):
        pixels[i] = (0,0,0)
    for i in range(3):
        pixels[i] = (255,0,0)
    for i in range(3):
        sleep(1)
        pixels[2-i] = (0,0,0)
    print("GO when a LED reaches the bottom!")
        
    # Game start
    for led in range(len(game) - USEDPIXELS):
        update(game, led)
        sleep(delay)
        if not check(game[led]):
            wrong += 1
    

    accuracy = 100 * (len(game)-(2*USEDPIXELS)-wrong) / (len(game)-(2*USEDPIXELS))
    print("Finished! Your accuracy: " + str(round(accuracy, 1)) + "%")
    print(
        ("GG! Prefect game!"                             if accuracy > 99 else 
        ("Great job!"                                    if accuracy > 90 else
        ("Nicely done!"                                  if accuracy > 80 else
        ("Not the best, but also not the worst!"         if accuracy > 70 else
        ("You can do better! Try harder!"                if accuracy > 60 else
        ("That wasn't exactly good. Take more practice!" if accuracy > 0 else
        ("Are you kidding? Check that everything is wired up correctly and read the instructions!"
        ))))))))
