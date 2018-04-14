import pyautogui as pag

user_input = input("Enter 4 coordinates separated by commas: ")

input_list = user_input.split(',')

r = input_list[0], input_list[1], 35, 35

filename = input("Enter filename: ")

pag.screenshot('triggers/' + filename + ".png", region=r)