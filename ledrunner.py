import RPi.GPIO as gpio
import board
import neopixel
from time import sleep

gpio.setmode(gpio.BCM)

# All the sequences that can be played
GAMES = [
    [0,0,0,0,0,0,1,2,3,3,2,1,3,2,3,1,3,1,3,2,3,2,1,2,2,1,3,3,3,1,0,0,0,0,0,0]
]


# Setup the buttons
PINRED = 23; PINGREEN = 24; PINBLUE = 25
gpio.setup(PINRED, gpio.IN, gpio.PUD_UP)
gpio.setup(PINGREEN, gpio.IN, gpio.PUD_UP)
gpio.setup(PINBLUE, gpio.IN, gpio.PUD_UP)

PINPIXELS = board.D18
AMOUNTPIXELS = 8
# Set brigthness to a very HIGH number so no external supply is required
pixels = neopixel.NeoPixel(PINPIXELS, AMOUNTPIXELS, brightness=0.01)

# Only the first 6 LEDs are being used
for i in range(8):
    pixels[i] = (0,0,0)


def update(lst, active):
    global pixels
    for i in range(6):
        pixels[i] = (0,0,0)
    leds = lst[active:(active+6)]
    for i in range(len(leds)):
        if   leds[i] == 0: pixels[i] = (0,0,0)
        elif leds[i] == 1: pixels[i] = (255,0,0)
        elif leds[i] == 2: pixels[i] = (0,255,0)
        elif leds[i] == 3: pixels[i] = (0,0,255)
        

def check(active):
    # Returns 1 if wrong, 0 if correct
    buttonPressed = 0
    if gpio.input(PINRED) == gpio.LOW: buttonPressed += 1
    if gpio.input(PINGREEN) == gpio.LOW: buttonPressed += 2
    if gpio.input(PINBLUE) == gpio.LOW: buttonPressed += 3
    if gpio.input(PINRED) == gpio.LOW and gpio.input(PINGREEN) == gpio.LOW: buttonPressed = 0
    return (0 if buttonPressed == active else 1)
        
    
game: list  # The currently active sequence
delay: float  # Time the player has to react
wrong: int  # Mistakes the player did

print("Hello, and welcome to LEDRUNNER!")
while True:
    print("Press any button to play!")
    c = 0
    while (gpio.input(PINRED) == gpio.HIGH) and (gpio.input(PINGREEN) == gpio.HIGH) and (gpio.input(PINBLUE) == gpio.HIGH):
        sleep(0.1)
        update([1,2,3,3,2,1,1,2,3,3,2,1], c)
        if c >= 6: c = 0
        else: c += 1

    game = GAMES[0]
    delay = 0.5
    
    wrong = 0
    
    # Countdown
    for i in range(6):
        pixels[i] = (0,0,0)
    for i in range(3):
        pixels[i] = (255,0,0)
    while not ((gpio.input(PINRED) == gpio.HIGH) and (gpio.input(PINGREEN) == gpio.HIGH) and (gpio.input(PINBLUE) == gpio.HIGH)):
        sleep(0.1)
    for i in range(4):
        pixels[3-i] = (0,0,0)
        sleep(1)
    print("Go!")
        
    # Game start
    for led in range(len(game) - 6):
        update(game, led)
        sleep(delay)
        wrong += check(game[led])
    
    print("Finished! Your accuracy: " + str(round((100 * (len(game)-12-wrong) / (len(game)-12)), 1)) + "%.")
