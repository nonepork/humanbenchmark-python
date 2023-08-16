from pynput import mouse
from PIL import Image
import pytesseract
import pyautogui
import win32api
import win32con
import time
import os

# TODO 
# Find a way to make python temrinal stays at top without affecting other windows

# From chatgpt, wants to try different data type so i kept it
global coordinates
coordinates = []
global xseen, yseen, xnew, ynew

with open('wordlist.txt', 'w') as f:
    f.write('')

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def on_click_coord(x, y, button, pressed):
    global coordinates
    if len(coordinates) == 2:
        return False
    elif pressed:
        print(f'Coordinates x:{x}, y:{y}')
        coordinates.append((x, y))

def on_click_seen_coord(x, y, button, pressed):
    global seencoordinates
    if len(seencoordinates) == 2:
        return False
    elif pressed:
        print(f'Coordinates x:{x}, y:{y}')
        seencoordinates.append((x, y))

def on_click_new_coord(x, y, button, pressed):
    global newcoordinates
    if len(newcoordinates) == 2:
        return False
    elif pressed:
        print(f'Coordinates x:{x}, y:{y}')
        newcoordinates.append((x, y))

print('Program starting in 5 second')
time.sleep(5)
os.system('cls')

# Grab image and ocr to text

while True:
    with mouse.Listener(
        on_click=on_click_coord) as listener:
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
    except SystemError:
        coordinates = []
        print('Please click again')
    else:
        if os.path.exists('textArea.png'):
            img = Image.open('textArea.png')
            img = img.resize((900, 120), Image.NEAREST)
            text = pytesseract.image_to_string(img,
                                               lang='eng').replace('\n', ' ').replace('  ', ' ')
            if len(text) > 4:
                break
            else:
                coordinates = []
                text = ''
                print('Please click again')

while True:
    newcoordinates = []
    with mouse.Listener(
        on_click=on_click_new_coord) as listener:
        print('Click the top left corner, and bottom right corner of new button')
        listener.join()
    try:
        x, y = pyautogui.locateCenterOnScreen('new.png', 
            region=(newcoordinates[0][0],
            newcoordinates[0][1],
            newcoordinates[1][0]-newcoordinates[0][0],
            newcoordinates[1][1]-newcoordinates[0][1]),
            grayscale=True,
            confidence=0.8)
    except ValueError:
        newcoordinates = []
        print('Please click again')
    except TypeError:
        newcoordinates = []
        print('Please click again')
    else:
        if x is not None:
            xnew, ynew = x, y
            break

while True:
    seencoordinates = []
    with mouse.Listener(
        on_click=on_click_seen_coord) as listener:
        print('Click the top left corner, and bottom right corner of seen button')
        listener.join()
    try:
        x, y = pyautogui.locateCenterOnScreen('seen.png', 
            region=(seencoordinates[0][0],
            seencoordinates[0][1],
            seencoordinates[1][0]-seencoordinates[0][0],
            seencoordinates[1][1]-seencoordinates[0][1]),
            grayscale=True,
            confidence=0.8)
    except ValueError:
        seencoordinates = []
        print('Please click again')
    except TypeError:
        seencoordinates = []
        print('Please click again')
    else:
        if x is not None:
            xseen, yseen = x, y
            break

print('DONT MOVE now :)')
time.sleep(2)

while True:
    region=(coordinates[0][0],
            coordinates[0][1],
            coordinates[1][0]-coordinates[0][0],
            coordinates[1][1]-coordinates[0][1])
    pyautogui.screenshot('textArea.png', region=region)
    time.sleep(0.5)
    img = Image.open('textArea.png')
    img = img.resize((950, 200), Image.NEAREST)
    text = pytesseract.image_to_string(img,
                                       lang='eng').replace('\n', '').replace(' ', '')
    with open('wordlist.txt', 'a+') as f:
        f.seek(0)
        seen_words = f.readline()
        print(seen_words)
        if text is not None and text not in seen_words:
            f.write(f'{text} ')
            click(xnew, ynew)
            time.sleep(0.5)
        elif text is not None and text in seen_words:
            click(xseen, yseen)
            time.sleep(0.5)
        else:
            continue
            time.sleep(0.5)
