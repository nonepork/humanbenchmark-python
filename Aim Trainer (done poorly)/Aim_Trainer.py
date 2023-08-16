from pynput import mouse
import pyautogui
import win32api
import win32con
import time
import os

# TODO
# Find a way to make python temrinal stays at top without affecting other windows
# Less messy code
# Faster detection method

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

# From chatgpt, wants to try different data type so i kept it
global coordinates
coordinates = []

def on_click(x, y, button, pressed):
    global coordinates
    if len(coordinates) == 2:
        return False
    elif pressed:
        print(f'Coordinates x:{x}, y:{y}')
        coordinates.append((x, y))

def clicked(x, y, button, pressed):
    if pressed:
        return False

print('Program starting in 5 second')
time.sleep(5)
os.system('cls')

# Check whether area's right or not

while True:
    with mouse.Listener(
        on_click=on_click) as listener:
        print('Click the top left corner, and bottom right corner of target area')
        listener.join()
    try:
        x, y = pyautogui.locateCenterOnScreen('target.png', 
            region=(coordinates[0][0],
            coordinates[0][1],
            coordinates[1][0]-coordinates[0][0],
            coordinates[1][1]-coordinates[0][1]),
            grayscale=True,
            confidence=0.8)
    except ValueError:
        coordinates = []
        print('Please click again')
    except TypeError:
        coordinates = []
        print('Please click again')
    else:
        if x is not None:
            break

with mouse.Listener(
    on_click=clicked) as listener:
    print('Now click play and DONT MOVE :)')
    listener.join()

# Speed time

while True:
    region=(coordinates[0][0],
            coordinates[0][1],
            coordinates[1][0]-coordinates[0][0],
            coordinates[1][1]-coordinates[0][1])
    try:
        x, y = pyautogui.locateCenterOnScreen('target.png',
                                              region=region,
                                              grayscale=True,
                                              confidence=0.8)
        click(x, y)
    except TypeError:
        continue
