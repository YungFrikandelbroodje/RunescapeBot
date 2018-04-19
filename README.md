# RunescapeBot

My personal old-school runescape bot.

Note: Will get you banned if used extensively 

#### Mining Bot
- Version 1.1: Takes 423.3 seconds per lap, which is a 4,167 xp/hour and 238 copper ore/hour.
- Version 1.2: Takes 394.11 seconds per lap, which is a 4,476 xp/hour and 256 ore/hour pace. This is due to path stop point detection. 
- Version 1.3: Takes 347.33 seconds on average, which is a 4,897 xp/hour and 280 ore/hour pace. This is after allowing the bot to run
- Version 1.4: Takes 358.59 seconds, which is a 9,487 xp/hour and 271 iron ore/hour pace. Now mining iron ore, more $$$. Also, using rune pickaxe in my inventory (too low attack to equip, hence the attack bot is coming next). Competition of iron ore also makes it harder to determine an average. 

#### Attack Bot
- Version 1.1: TBD

---

## Features

### Mining Bot

#### Mining Loop
- mining a single rock given the proper screenshots of it mined/unmined (detects when to hit and when not to hit)
- random clicking based on a given range (to avoid getting banned)
- linear movement of mouse instead of teleporting mouse points 
- random clicking times based on a given interval 
- checks to see if anyone mentions the word 'bot' in chat and will respond with a hypothetical answer
- don't need to worry about dying to that pesky rat, will walk out of range before it kills you

#### Bank Loop
- checking if the inventory is full, if so, return to the bank and deposit items
- walking to the bank, storing and walking back to that location
- walking now takes less time due to image matching when walking from one point to another; also means the character is unaffected by loading times now
- easier path setup, can use on any route to anywhere basically; screenshots for path stop point detection too! (make_path function)
- can run to the bank when the bot sees the running gauge is full
- can recognize and take back pickaxe that's in inventory no matter where it's stored in the bank (if you can't equip it)
- can mine from a loop of different rocks (look at mine_loop, rock_locations and rock_triggers)
- will log out after 30 laps and wait a random (long) amount of time and then log back in 

#### Screenshot
- this is after a few laps, right after storing items in the bank:
<img src="https://github.com/chriskok/RunescapeBot/blob/master/screenshot1.PNG">

### Attack Bot

#### Attack Loop
- TBD

---

## To-Do List
- add option of pickaxe
- to avoid detection further, implement logging out after certain number of laps
- start the attack bot
- tutorial of how to setup routes and mining
- the option of dropping everything in inventory (for powermining)
- check gauge and click on running button at every iteration of the bank_loop instead of just at the start
- code to move the screen to the reset position (click compass and press up button)
- easier set up for things like new ores; mining different resources

---

## Contributors
- Christopher Kok (<ckok@purdue.edu>)

---

## Credits
- http://pyautogui.readthedocs.io/en/latest/screenshot.html
- <http://www.zaxrosenberg.com/how-to-write-a-runescape-autoclicker-with-python-part-ii/>

---
