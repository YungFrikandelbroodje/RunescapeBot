# RunescapeBot
My personal old-school runescape bot.
Credits: <http://www.zaxrosenberg.com/how-to-write-a-runescape-autoclicker-with-python-part-ii/>

### Mining Bot
- Version 1.1: Takes 423.3 seconds per lap, which is a 4,167 xp/hour and 238 copper ore/hour.
- Version 1.2: Takes 394.11 seconds per lap, which is a 4,476 xp/hour and 256 ore/hour pace. This is due to path stop point detection. 
- Version 1.3: Takes 347.33 seconds on average, which is a 4,897 xp/hour and 280 ore/hour pace. This is after allowing the bot to run

### Attack Bot
- Version 1.1: TBD

---

## Features

### Mining Bot

#### Mining Loop
- mining a single rock given the proper screenshots of it mined/unmined (detects when to hit and when not to hit)
- random clicking based on a given range (to avoid getting banned)
- linear movement of mouse instead of teleporting mouse points 
- random clicking times based on a given interval 

#### Bank Loop
- checking if the inventory is full, if so, return to the bank and deposit items
- walking to the bank, storing and walking back to that location
- walking now takes less time due to image matching when walking from one point to another; also means the character is unaffected by loading times now
- easier path setup, can use on any route to anywhere basically; screenshots for path stop point detection too!
- can run to the bank when the bot sees the gauge is full

### Attack Bot

#### Attack Loop
- TBD

---

## To-Do List
- tutorial of how to setup routes and mining
- the option of dropping everything in inventory
- code to move the screen to the reset position (click compass and press up button)
- easier set up for things like new ores; mining different resources

---

## Contributors
- Christopher Kok (<ckok@purdue.edu>)

---
