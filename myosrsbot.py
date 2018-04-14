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

def bank_loop(bank_locations, bank_triggers, back_triggers):
    """Makes a trip to the bank to deposit the iron ore. Takes 16-17 seconds"""
    order = ['map1', 'map2', 'map3', 'map4', 'map5', 'map6', 'map7', 'map8', 'deposit']
    trigger_order = ['map1', 'map2', 'map3', 'map4', 'map5', 'map6', 'map7']
    waits = [(14, 15), (14, 15), (12, 14), (12, 14), (14, 15), (10, 11), (2, 3), (4, 5)]

    for i in range(len(order)):
        random_coordinate(bank_locations[order[i]])
        pag.click()
        if i < 7: 
            wait_for_trigger(bank_triggers[trigger_order[i]])
        else: 
            random_wait(2,5)
        # random_wait(waits[i][0], waits[i][1])
        random_wait(0.05, 0.1)

    back_order = ['mapb1', 'mapb2', 'mapb3', 'mapb4', 'mapb5', 'mapb6', 'mapb7']
    back_trigger_order = ['mapb1', 'mapb2', 'mapb3', 'mapb4', 'mapb5', 'mapb6', 'mapb7']

    for i in range(len(back_order)):
        random_coordinate(bank_locations[back_order[i]])
        pag.click()
        # random_wait(45,60)
        print("moving to " + back_order[i])
        if i < 2:
            wait_for_trigger(back_triggers[back_trigger_order[i]])
        else:
            random_wait(15,16)
        random_wait(0.05, 0.1)

def new_bank_loop(bank_locations, bank_triggers):
    """Makes a trip to the bank to deposit the iron ore"""
    # clicks on run if at 100
    r = 662, 177, 35, 35
    if image_match(r, 'triggers/run.png'):
        random_coordinate((672,189,10,10))
        pag.click()
        random_wait(0.1, 0.2)

    for i in range(len(bank_locations)):
        random_coordinate(bank_locations[i])
        pag.click()
        wait_for_trigger(bank_triggers[i])
        random_wait(0.05, 0.1)

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
    return

def image_match(r, img):
    try:
        pag.screenshot('triggers/screenie.png', region=r)
    except OSError:
        # print("error with screenshot, retrying...")
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

    # return image_match(r, img)

def make_path(interval, fileprefix):
    click_locations = [] # save locations of clicks 
    click_triggers = []  # save screenshot locations and filename
    locfile = open('loc.txt', 'w+') # open a file to write to and save loc 
    trigfile = open('trig.txt', 'w+') # open a file to write to and save trig

    """makes a path starting a certain point, taking screenshots along the way and saving those points in an array"""
    print(fileprefix)
    try:
        time.sleep(interval)  # wait five seconds
        # Move to location one
        x, y = pag.position()
        click_locations.append((x, y, 0, 0))
        pag.click()
        count = 0
        while True:
            time.sleep(interval * 2)  # wait ten seconds
            # Get screenshot at current location
            x, y = pag.position()
            r = x, y, 35, 35
            filename = 'triggers/paths/' + fileprefix + str(count) + '.png'
            print("saving " + filename)
            pag.screenshot(filename, region=r)
            click_triggers.append((x, y, 35, 35, filename))

            time.sleep(interval)  # wait five seconds
            print("moving location")
            # Move to next location
            x, y = pag.position()
            click_locations.append((x, y, 0, 0))
            pag.click()

            count += 1
    except KeyboardInterrupt:
        print("done making path")
    
    print(click_locations)
    print(click_triggers)

    for item in click_locations:
        locfile.write("%s,\n" % str(item))

    for item in click_triggers:
        trigfile.write("%s,\n" % str(item))

    return click_locations, click_triggers


# rock locations found by using the find_cursor.py program
# rock_locations = {'rock1': (300, 275, 35, 35), 'rock2': (250, 220, 35, 35)}
rock_locations = {'rock1': (300, 287, 35, 35)}

# rock_triggers = {'rock1iron': (315, 285, 5, 5, 'triggers/tin1.png'),
#                  'rock1noiron': (315, 285, 5, 5, 'triggers/notin1.png'),
#                  'rock2iron': (262, 231, 5, 5, 'triggers/tin2.png'),
#                  'rock2noiron': (262, 231, 5, 5, 'triggers/notin2.png')}
rock_triggers = {'rock1iron': (300, 287, 35, 35, 'triggers/cop1.png'),
                 'rock1noiron': (300, 287, 35, 35, 'triggers/nocop1.png')}

# bank_locations = {'map1': (857, 73, 0, 0), 'map2': (800, 59, 0, 0),
#                     'map3': (784, 61, 0, 0), 'map4': (780, 90, 0, 0),
#                     'map5': (724, 146, 0, 0), 'map6': (735, 145, 0, 0),
#                     'map7': (803, 194, 0, 0), 'map8': (302, 286, 4, 4), 
#                     'deposit': (540, 413, 13, 13),
#                     'mapb1': (882, 104, 0, 0), 'mapb2': (880, 143, 0, 0),
#                     'mapb3': (818, 222, 0, 0), 'mapb4': (822, 222, 0, 0),
#                     'mapb5': (816, 220, 0, 0), 'mapb6': (755, 188, 0, 0),
#                     'mapb7': (225, 367, 0, 0)}

# bank_triggers = {'map1': (445, 82, 35, 35, 'triggers/map1.png'),
#                  'map2': (161, 180, 35, 35, 'triggers/map2.png'),
#                  'map3': (395, 193, 35, 35, 'triggers/map3.png'),
#                  'map4': (451, 376, 35, 35, 'triggers/map4.png'),
#                  'map5': (346, 153, 35, 35, 'triggers/map5.png'),
#                  'map6': (87, 103, 35, 35, 'triggers/map6.png'),
#                  'map7': (501, 376, 35, 35, 'triggers/map7.png')}

# back_triggers = {'mapb1': (269, 116, 35, 35, 'triggers/mapb1.png'),
#                  'mapb2': (410, 328, 35, 35, 'triggers/mapb2.png'),
#                  'mapb3': (576, 376, 35, 35, 'triggers/mapb3.png'),
#                  'mapb4': (459, 239, 35, 35, 'triggers/mapb4.png'),
#                  'mapb5': (530, 163, 35, 35, 'triggers/mapb5.png'),
#                  'mapb6': (303, 79, 35, 35, 'triggers/mapb6.png'),
#                  'mapb7': (501, 376, 35, 35, 'triggers/mapb7.png')}

# bank_locations = {'map1': (855, 73, 0, 0), 'map2': (803, 52, 0, 0),
# 					'map3': (749, 78, 0, 0), 'map4': (749, 78, 0, 0),
# 					'map5': (718, 152, 0, 0), 'map6': (803, 177, 0, 0),
# 					'map7': (319, 292, 0, 0), 'deposit': (540, 413, 13, 13),
# 					'mapb1': (882, 104, 0, 0), 'mapb2': (871, 187, 0, 0),
# 					'mapb3': (838, 203, 0, 0), 'mapb4': (808, 231, 0, 0),
# 					'mapb5': (786, 226, 0, 0), 'mapb6': (774, 162, 0, 0)}

bank_locations = [(857, 86, 0, 0),
    (792, 59, 0, 0),
    (781, 63, 0, 0),
    (783, 79, 0, 0),
    (725, 145, 0, 0),
    (733, 144, 0, 0),
    (802, 186, 0, 0),
    (315, 292, 0, 0),
    (556, 432, 0, 0),
    (875, 100, 0, 0),
    (881, 143, 0, 0),
    (819, 222, 0, 0),
    (829, 209, 0, 0),
    (810, 222, 0, 0),
    (752, 195, 0, 0),
    (316, 451, 0, 0)]

bank_triggers = [(443, 113, 35, 35, 'triggers/paths/test0.png'),
    (454, 274, 35, 35, 'triggers/paths/test1.png'),
    (432, 86, 35, 35, 'triggers/paths/test2.png'),
    (450, 330, 35, 35, 'triggers/paths/test3.png'),
    (341, 115, 35, 35, 'triggers/paths/test4.png'),
    (495, 56, 35, 35, 'triggers/paths/test5.png'),
    (363, 424, 35, 35, 'triggers/paths/test6.png'),
    (587, 50, 35, 35, 'triggers/paths/test7.png'),
    (866, 618, 35, 35, 'triggers/paths/test8.png'),
    (354, 155, 35, 35, 'triggers/paths/test9.png'),
    (460, 374, 35, 35, 'triggers/paths/test10.png'),
    (617, 368, 35, 35, 'triggers/paths/test11.png'),
    (469, 334, 35, 35, 'triggers/paths/test12.png'),
    (490, 86, 35, 35, 'triggers/paths/test13.png'),
    (68, 244, 35, 35, 'triggers/paths/test14.png'),
    (200, 230, 35, 35, 'triggers/paths/test15.png')]


lap = 0
# answer = input("Would you like to make a new path (y/n)? ")
try:
    # loc = []
    # trig = []
    # if answer == 'y': 
    #     interval = input("Length of interval? ")
    #     loc, trig = make_path(int(interval), fileprefix="test")
    # else: 
    #     with open('loc.txt') as l:
    #         loc = l.readlines()
    #         loc = [x.strip() for x in content] 
    #     with open('trig.txt') as t:
    #         trig = t.readlines()
    #         trig = [x.strip() for x in content] 
    # loc, trig = make_path(10, fileprefix="test")

    while True:
        start_time = time.time()
        while True:
            full = mine_loop(rock_locations, rock_triggers, 0)
            if full: 
                break
        # bank_loop(bank_locations, bank_triggers, back_triggers)
        new_bank_loop(bank_locations, bank_triggers)
        lap += 1
        laptime = time.time()-start_time
        print("Trip number {tripno} took {time} seconds, which is a {xp} xp/hour and "
              "{ore} ore/hour pace.".format(tripno=lap, time=round(laptime, 2),
              xp=('{0:,.0f}'.format(60 / (laptime / 60) * 28 * 17.5)),
              ore=('{0:,.0f}'.format(60/(laptime/60)*28))))
except KeyboardInterrupt:
    print("Goodbye now!~")
    sys.exit()

