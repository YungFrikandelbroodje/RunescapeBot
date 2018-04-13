import math
from random import randint, uniform
import sys
import time
 
import cv2
import numpy as np
import pyautogui as pag

def random_wait(min=0.25, max=0.50):
    """Waits a random number of seconds between two numbers (0.25 and 0.50 default) to mimic human reaction time"""
    return time.sleep(uniform(min, max))

def random_coordinate(location):
    """Moves cursor to random locaction still above the object to be clicked"""
    x = randint(location[0], location[0]+location[2])
    y = randint(location[1], location[1]+location[3])
    time = travel_time(x, y)

    return pag.moveTo(x, y, time)
 
def travel_time(x2, y2):
    """Calculates cursor travel time in seconds per 240-270 pixels, based on a variable rate of movement"""
    rate = uniform(0.09, 0.15)
    x1, y1 = pag.position()
    distance = math.sqrt(math.pow(x2-x1, 2)+math.pow(y2-y1, 2))

    return max(uniform(.08, .12), rate * (distance/randint(250, 270)))


order = ['rock1', 'rock2']

# rock locations found by using the find_cursor.py program
rock_locations = {'rock1': (320, 280, 12, 13), 'rock2': (320, 200, 12, 13)}

bank_locations = {'dgdoordown': (1630, 230, 70, 100), 'depositbox': (1079, 1086, 104, 71),
                  'depositbutton': (1333, 849, 30, 15), 'dgdoorup': (1625, 240, 45, 200),
                  'startlocation': (947, 1195, 71, 65)}

try: 
	for x in range(0,28):
		random_coordinate(rock_locations[order[x % 2]])
		pag.click()
		random_wait(6, 10)
except KeyboardInterrupt:
	print("Goodbye now!~")
	sys.exit()
