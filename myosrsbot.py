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

def mine_loop(rock_locations, triggers, mininglap):
    order = ['rock1', 'rock2']
    trigger_order = ['rock1iron', 'rock1noiron', 'rock2iron', 'rock2noiron', 'rock3iron', 'rock3noiron']

    for i in range(len(order)):
        # Checks for full inventory.
        # if not self.image_match((2352, 682, 63, 55), 'triggers/bankslot.png'):
        #    return True

        random_coordinate(rock_locations[order[i]])
        wait_for_trigger(triggers[trigger_order[(i*2)]])  # wait for iron
        pag.click()
        wait_for_trigger(triggers[trigger_order[(i*2)+1]])  # wait for success
        random_wait(0.05, 0.1)

    # Resets location for the beginning of the next loop.
    # self.random_coordinate(rock_locations['reset'])
    # self.check_for_scorpion((rock_locations['reset'][0], rock_locations['reset'][1],
    #                          rock_locations['reset'][2] + 250, rock_locations['reset'][3] + 250))
    # pag.click()
    # self.wait_for_trigger((1700, 50, 150, 150, 'triggers/reset_check.png'))  # check to make sure made it to right location

    return

def image_match(r, img):
    pag.screenshot('triggers/screenie.png', region=r)
    screen = cv2.imread('triggers/screenie.png')
    template = cv2.imread(img)

    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    threshold = .80
    loc = np.where(res >= threshold)
    if len(loc[0]) > 0:
        return True

    return False

def wait_for_trigger(triggers):
    """Checks to see if the proper message is on screen to indicate that the rock is ready to mine"""
    r = triggers[0], triggers[1], triggers[2], triggers[3]
    img = triggers[4]
    while image_match(r, img) == False:
        print("waiting for " + img)
        random_wait(0.1, 0.2)

    print("done waiting")

    return image_match(r, img)


# rock locations found by using the find_cursor.py program
rock_locations = {'rock1': (295, 275, 55, 55), 'rock2': (249, 220, 55, 55)}

bank_locations = {'dgdoordown': (1630, 230, 70, 100), 'depositbox': (1079, 1086, 104, 71),
                  'depositbutton': (1333, 849, 30, 15), 'dgdoorup': (1625, 240, 45, 200),
                  'startlocation': (947, 1195, 71, 65)}

rock_triggers = {'rock1iron': (295, 275, 62, 62, 'triggers/tin1.png'),
                 'rock1noiron': (295, 275, 62, 62, 'triggers/notin1.png'),
                 'rock2iron': (249, 220, 62, 62, 'triggers/tin2.png'),
                 'rock2noiron': (249, 220, 62, 62, 'triggers/notin2.png')}

try: 
	while True:
		mine_loop(rock_locations, rock_triggers, 0)
except KeyboardInterrupt:
	print("Goodbye now!~")
	sys.exit()
