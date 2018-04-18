import pyautogui as pag

user_input = input("Enter 4 coordinates separated by commas: ")

input_list = user_input.split(',')

if len(input_list) >= 4:
	r = input_list[0], input_list[1], input_list[2], input_list[3]
else:
	r = input_list[0], input_list[1], 35, 35

filename = input("Enter filename: ")

pag.screenshot('triggers/' + filename + ".png", region=r)