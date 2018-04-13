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

def bank_loop(bank_locations):
    """Makes a trip to the bank to deposit the iron ore. Takes 16-17 seconds"""
    order = ['map1', 'map2', 'map3', 'map4', 'map5', 'map6', 'map7', 'deposit']
    waits = [(14, 15), (14, 15), (12, 14), (12, 14), (14, 15), (10, 11), (2, 3), (4, 5)]

    for i in range(len(order)):
        random_coordinate(bank_locations[order[i]])
        if i == 7:
        	print("time to deposit")
            # wait_for_trigger(triggers[order[i]])
        pag.click()
        random_wait(waits[i][0], waits[i][1])
        # random_wait(12, 14)

    back_order = ['mapb1', 'mapb2', 'mapb3', 'mapb4', 'mapb5', 'mapb6']

    for i in range(len(back_order)):
        random_coordinate(bank_locations[back_order[i]])
        pag.click()
        random_wait(15, 17)

def mine_loop(rock_locations, triggers, mininglap):
    # order = ['rock1', 'rock2']
    order = ['rock1']
    trigger_order = ['rock1iron', 'rock1noiron', 'rock2iron', 'rock2noiron', 'rock3iron', 'rock3noiron']

    for i in range(len(order)):
        # Checks for full inventory.
        if not image_match((863, 577, 45, 45), 'triggers/bagfull.png'):
        	return True

        wait_for_trigger(triggers[trigger_order[(i*2)]])  # wait for rock to be available
        random_coordinate(rock_locations[order[i]])
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
    try:
        pag.screenshot('triggers/screenie.png', region=r)
    except OSError:
        print("error with screenshot, retrying...")
        random_wait(0.2,0.5)
        pag.screenshot('triggers/screenie.png', region=r)

    screen = cv2.imread('triggers/screenie.png')
    template = cv2.imread(img)

    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    threshold = .95
    loc = np.where(res >= threshold)
    if len(loc[0]) > 0:
        return True

    return False

def wait_for_trigger(triggers):
    """Checks to see if the proper message is on screen to indicate that the rock is ready to mine"""
    r = triggers[0], triggers[1], triggers[2], triggers[3]
    img = triggers[4]
    while image_match(r, img) == False:
        random_wait(0.1, 0.2)

    print("done waiting for " + img)

    # return image_match(r, img)


# rock locations found by using the find_cursor.py program
# rock_locations = {'rock1': (300, 275, 35, 35), 'rock2': (250, 220, 35, 35)}
rock_locations = {'rock1': (300, 287, 35, 35)}

bank_locations = {'map1': (855, 73, 0, 0), 'map2': (803, 52, 0, 0),
					'map3': (749, 78, 0, 0), 'map4': (749, 78, 0, 0),
					'map5': (718, 152, 0, 0), 'map6': (803, 177, 0, 0),
					'map7': (319, 292, 0, 0), 'deposit': (540, 413, 13, 13),
					'mapb1': (882, 104, 0, 0), 'mapb2': (871, 187, 0, 0),
					'mapb3': (838, 203, 0, 0), 'mapb4': (808, 231, 0, 0),
					'mapb5': (786, 226, 0, 0), 'mapb6': (774, 162, 0, 0)}

# rock_triggers = {'rock1iron': (315, 285, 5, 5, 'triggers/tin1.png'),
#                  'rock1noiron': (315, 285, 5, 5, 'triggers/notin1.png'),
#                  'rock2iron': (262, 231, 5, 5, 'triggers/tin2.png'),
#                  'rock2noiron': (262, 231, 5, 5, 'triggers/notin2.png')}
rock_triggers = {'rock1iron': (300, 287, 35, 35, 'triggers/cop1.png'),
                 'rock1noiron': (300, 287, 35, 35, 'triggers/nocop1.png')}
lap = 0
try:
	while True:
		while True:
			full = mine_loop(rock_locations, rock_triggers, 0)
			if full: 
				break
		bank_loop(bank_locations)
		lap += 1
except KeyboardInterrupt:
	print("Completed {} laps".format(lap))
	print("Goodbye now!~")
	sys.exit()

