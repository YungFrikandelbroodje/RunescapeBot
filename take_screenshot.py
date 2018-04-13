import pyautogui as pag

user_input = input("Enter 4 coordinates separated by commas: ")

input_list = user_input.split(',')

r = input_list[0], input_list[1], input_list[2], input_list[3]

filename = input("Enter filename: ")

pag.screenshot('triggers/' + filename, region=r)