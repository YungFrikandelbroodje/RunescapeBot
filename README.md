# RunescapeBot
My personal old-school runescape bot

Version 1.1: takes 423.3 seconds per lap, which is a 4,167 xp/hour and 238 copper ore/hour.
Version 1.2: 

---

## Features
### Mining Loop
- mining a single rock given the proper screenshots of it mined/unmined (detects when to hit and when not to hit)
- random clicking based on a given range (to avoid getting banned)
- linear movement of mouse instead of teleporting mouse points 
- random clicking times based on a given interval 

### Bank Loop
- checking if the inventory is full, if so, return to the bank and deposit items
- walking to the bank, storing and walking back to that location (note: walking now takes much shorter due to image matching when walking from one point to another finishes - meaning the character is unaffected by loading times now)

---

## To-Do List
- save the data from click_locations and click_triggers into a file to use multiple times
- the option of running to and fro from the bank
- the option of dropping everything in inventory
- code to easily find and screenshot new spot
- code to move the screen to the reset position (click compass and press up button)
- mining different resources

---

## Contributors
- Christopher Kok (<ckok@purdue.edu>)

---
