import math
from random import randint, uniform, choice
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
        if i == 9:
            random_wait(1.5, 2)
            pickloc = None
            while pickloc is None:
                pickloc = pag.locateOnScreen('triggers/runepick.png', confidence=0.9, region=(0,0,956,668))
            region = pickloc[0] + 12, pickloc[1] + 12, 1, 1
            random_coordinate(region)
            pag.click()
            random_wait(1, 1.5)
        	
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

        check_for_bot_word()
        check_for_rat()
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

def logout():
    print("Time to nap for a while...")
    log_locations = [(787, 627, 14, 20),
    (731, 379, 14, 14),
    (760, 567, 34, 14)]

    for i in range(len(log_locations)):
        random_coordinate(log_locations[i])
        pag.click()
        # wait_for_trigger(bank_triggers[i])
        random_wait(0.5, 1)

    random_wait(2100,2400)
    # random_wait(4,5)
    print("Nap time over!")
    login()

def login():
    log_locations = [(515, 388, 30, 14),
    (318, 428, 24, 14),
    (364, 424, 30, 30), 
    (190, 642, 11, 11)]

    random_coordinate(log_locations[0])
    pag.click()
    random_wait(1.5, 2)
    pag.typewrite(password, interval=0.25)

    random_coordinate(log_locations[1])
    pag.click()
    random_wait(4, 5)
    random_coordinate(log_locations[2])
    pag.click()
    random_wait(1.5, 2)
    random_coordinate(log_locations[3])
    pag.click()
    random_wait(0.5, 1)

def check_for_bot_word():
    wordlist = ['xd', ':)', ':P', ':]', 'x]', 'xP', 'B)', 'x)', ':3']

    botloc = pag.locateOnScreen('triggers/botword.png', confidence=0.8, region=(60,591,540,20))
    global previous_botloc
    if botloc is not None and botloc != previous_botloc:
        pag.typewrite(choice(wordlist), interval=0.22)
        pag.press('enter')  # press the Enter key
        previous_botloc = botloc

    random_wait(0.5, 1)

def check_for_rat():
    r = 679,96,30,30
    if not image_match(r, 'triggers/health.png'):
        random_coordinate((188, 260, 0, 0))
        pag.click()
        random_wait(3, 5)

        random_coordinate((456, 266, 0, 0))
        pag.click()


# rock locations found by using the find_cursor.py program
# rock_locations = {'rock1': (300, 275, 35, 35), 'rock2': (250, 220, 35, 35)}
rock_locations = {'rock1': (316, 296, 25, 25)}

# rock_triggers = {'rock1iron': (315, 285, 5, 5, 'triggers/tin1.png'),
#                  'rock1noiron': (315, 285, 5, 5, 'triggers/notin1.png'),
#                  'rock2iron': (262, 231, 5, 5, 'triggers/tin2.png'),
#                  'rock2noiron': (262, 231, 5, 5, 'triggers/notin2.png')}
rock_triggers = {'rock1iron': (316, 296, 35, 35, 'triggers/iron1.png'),
                 'rock1noiron': (316, 296, 35, 35, 'triggers/noiron1.png')}

# Coordinates made using the make_path function, written into loc.txt and copy-pasted here. Not manually done by hand.
bank_locations = [(188, 260, 0, 0),
    (857, 86, 0, 0),
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
    (316, 451, 0, 0),
    (456, 266, 0, 0)]

# Coordinates made using the make_path function, written into trigs.txt and copy-pasted here.
bank_triggers = [(206, 233, 35, 35, 'triggers/paths/test-1.png'),
    (443, 113, 35, 35, 'triggers/paths/test0.png'),
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
    (200, 230, 35, 35, 'triggers/paths/test15.png'),
    (65, 229, 35, 35, 'triggers/paths/test16.png')]


lap = 0
# answer = input("Would you like to make a new path (y/n)? ")
password = input("Please enter your password: ")  # Not saving this anywhere, don't worry
previous_botloc = (0,0,0,0)
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

    true_start_time = time.time()
    while True:
        start_time = time.time()

        # Mine till your bag is full
        while True:
            full = mine_loop(rock_locations, rock_triggers, 0)
            if full: 
                break

        # Once your bag is full, head to the bank
        # bank_loop(bank_locations, bank_triggers, back_triggers)
        new_bank_loop(bank_locations, bank_triggers)
        lap += 1
        laptime = time.time()-start_time

        # Print the stats of the lap
        print("Trip number {tripno} took {time} seconds, which is a {xp} xp/hour and "
              "{ore} ore/hour pace.".format(tripno=lap, time=round(laptime, 2),
              xp=('{0:,.0f}'.format(60 / (laptime / 60) * 27 * 35)),
              ore=('{0:,.0f}'.format(60/(laptime/60)*27))))

        # Check if it's time to take a break
        if (lap % 30 == 0):
            logout()

except KeyboardInterrupt:
    totaltime = time.time()-true_start_time
    print("Total stats: {time} seconds with {ores} stored.".format(
        time=round(totaltime, 2),
        ores=lap * 27))
    print("Goodbye now!~")
    sys.exit()

