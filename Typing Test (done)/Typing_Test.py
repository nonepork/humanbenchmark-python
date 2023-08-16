from pynput import mouse
from PIL import Image
import pytesseract
import pyautogui
import time
import os

# TODO 
# Find a way to make python temrinal stays at top without affecting other windows

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

# Grab image and ocr to text

while True:
    with mouse.Listener(
        on_click=on_click) as listener:
        print('Click the top left corner, and bottom right corner of texts')
        listener.join()
    try:
        pyautogui.screenshot('textArea.png', region=(coordinates[0][0],
                                                    coordinates[0][1],
                                                    coordinates[1][0]-coordinates[0][0],
                                                    coordinates[1][1]-coordinates[0][1]))
    except ValueError:
        coordinates = []
        print('Please click again')
    else:
        if os.path.exists('textArea.png'):
            img = Image.open('textArea.png')
            img = img.resize((950, 200), Image.NEAREST)
            text = pytesseract.image_to_string(img,
                                               lang='eng').replace('\n', ' ').replace('  ', ' ')
            if len(text) > 20:
                break
            else:
                coordinates = []
                text = ''
                print('Please click again')

# Speed time

with mouse.Listener(
    on_click=clicked) as listener:
    print('Now click text area to type and DONT MOVE :)')
    listener.join()

time.sleep(0.5)
pyautogui.write(text, interval=0.01)
