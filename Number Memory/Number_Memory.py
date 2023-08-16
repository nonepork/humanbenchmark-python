from pynput import mouse
from PIL import Image
import pytesseract
import pyautogui
import time
import os

# TODO 
# Find a way to make python temrinal stays at top without affecting other windows

# From chatgpt, wants to try different data type so i kept it
global number_coordinates
number_coordinates = []

def on_click(x, y, button, pressed):
    global coordinates
    if len(number_coordinates) == 2:
        return False
    elif pressed:
        print(f'First coordinates x:{x}, y:{y}')
        number_coordinates.append((x, y))


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
        print('Click the top left corner, and bottom right corner of "Number Memory"')
        listener.join()
    try:
        pyautogui.screenshot('numberArea.png', region=(number_coordinates[0][0],
                                                       number_coordinates[0][1],
                                                       number_coordinates[1][0]-number_coordinates[0][0],
                                                       number_coordinates[1][1]-number_coordinates[0][1]))
    except ValueError:
        number_coordinates = []
        print('Please click again')
    else:
        if os.path.exists('numberArea.png'):
            img = Image.open('numberArea.png')
            text = pytesseract.image_to_string(img,
                                               lang='eng').replace('\n', '').replace('\r', '')
            if len(text) > 8:
                break
            else:
                number_coordinates = []
                text = ''
                print('Please click again')

os.system('cls')
input('Now, play a round, when you finished, type finish(F)')

# Speed time

with mouse.Listener(
    on_click=clicked) as listener:
    print('Now click text area to type and DONT MOVE :)')
    listener.join()

time.sleep(0.5)
while True:
    time.sleep(1000)
