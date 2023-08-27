from pynput import mouse
from pynput import keyboard
import pyautogui
import win32api
import win32con
import time
import os

# TODO 
# Find a way to make python temrinal stays at top without affecting other windows

global game_coordinates
game_coordinates = []
global boxes
boxes = []

def on_click(x, y, button, pressed):
    global game_coordinates
    if len(game_coordinates) == 2:
        return False
    elif pressed:
        print(f'First coordinates x:{x}, y:{y}')
        game_coordinates.append((x, y))


def clicked(x, y, button, pressed):
    if pressed:
        return False


def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)


def color_check(x_y_list, detected_amount, listening):
    for box in x_y_list:
        if pyautogui.pixel(box[0], box[1])[0] != 38:
            while pyautogui.pixel(box[0], box[1])[0] != 38:
                time.sleep(0.05)
            print(f"Detected {box}")
            detected_amount += 1
            if detected_amount > len(box_to_click):
                box_to_click.append((box[0], box[1]))
                listening = False

    return detected_amount, listening


print('Program starting in 5 second')
time.sleep(5)
os.system('cls')

os.system('cls')
input('Start a round and type finish(F)')

while True:
    with mouse.Listener(
        on_click=on_click) as listener:
        print('Click the top left corner, and bottom right corner of game area')
        listener.join()
    try:
        x, y = pyautogui.locateCenterOnScreen('game_area.png',
            region=(game_coordinates[0][0],
            game_coordinates[0][1],
            game_coordinates[1][0]-game_coordinates[0][0],
            game_coordinates[1][1]-game_coordinates[0][1]),
            grayscale=True,
            confidence=0.8)
    except ValueError:
        game_coordinates = []
        print('Please click again')
    except TypeError:
        game_coordinates = []
        print('Please click again')
    else:
        if x is not None:
            box_x = game_coordinates[0][0]
            box_y = game_coordinates[0][1]
            x_common_difference = int((game_coordinates[1][0]-game_coordinates[0][0])/6)
            y_common_difference = int((game_coordinates[1][1]-game_coordinates[0][1])/6)
            box_x+=x_common_difference # Easier to calculate
            box_y+=y_common_difference
            temp = box_x
            for i in range(0, 3):
                for j in range(0, 3):
                    boxes.append((box_x, box_y))
                    box_x+=(x_common_difference*2)
                box_x = temp
                box_y+=(y_common_difference*2)
            break

# Boxes is now a 3*3 not exactly 2d list :P
# O O O
# O O O
# O O O

with mouse.Listener(
    on_click=clicked) as listener:
    print('Now click on answer and DONT MOVE :)')
    listener.join()

# Speed time

detected_amount = 0
box_to_click = []
listen = True

time.sleep(0.55)
while True:
    if listen:
        detected_amount, listen = color_check(boxes,
                                              detected_amount,
                                              listen)
    else:
        for box in box_to_click:
            click(box[0], box[1])
            time.sleep(0.5)
        time.sleep(0.5)
        listen = True
        detected_amount = 0
