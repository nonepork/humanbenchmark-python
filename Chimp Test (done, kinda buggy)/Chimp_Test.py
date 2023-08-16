from PIL import Image, ImageFont, ImageDraw, ImageOps
from pynput import mouse
import pytesseract
import pyautogui
import win32api
import win32con
import time
import os

# From chatgpt, wants to try different data type so i kept it
global coordinates
coordinates = []
global amount_coordinates
amount_coordinates = []
global x_continue, y_continue

def Generate_Text(text):
    font = ImageFont.truetype("arial.ttf", 48)
    img = Image.new("RGB", (54, 54), (45, 137, 206))
    ImageDraw.Draw(img).text((13, 0), text, (255, 255, 255), font=font)
    img.save(f'{text}.png')

def on_click_coord(x, y, button, pressed):
    global coordinates
    if len(coordinates) == 2:
        return False
    elif pressed:
        print(f'Coordinates x:{x}, y:{y}')
        coordinates.append((x, y))

def on_click_amount_coord(x, y, button, pressed):
    global amount_coordinates
    if len(amount_coordinates) == 2:
        return False
    elif pressed:
        print(f'Coordinates x:{x}, y:{y}')
        amount_coordinates.append((x, y))

def on_click_continue_coord(x, y, button, pressed):
    global cont_coordinates
    if len(cont_coordinates) == 2:
        return False
    elif pressed:
        print(f'Coordinates x:{x}, y:{y}')
        cont_coordinates.append((x, y))

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def clicked(x, y, button, pressed):
    if pressed:
        return False

print('Program starting in 5 second')
time.sleep(5)
os.system('cls')

while True:
    with mouse.Listener(
        on_click=on_click_coord) as listener:
        print('Click the top left corner, and bottom right corner of game area')
        listener.join()
    try:
        x, y = pyautogui.locateCenterOnScreen('cool_logo.png', 
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

os.system('cls')
input('Now, play a round, when you finished, type finish(F)')

while True:
    with mouse.Listener(
        on_click=on_click_amount_coord) as listener:
        print('Click the top left corner, and bottom right corner of the big number in middle')
        listener.join()
    try:
        pyautogui.screenshot('Number.png', region=(amount_coordinates[0][0],
                                                   amount_coordinates[0][1],
                                                   amount_coordinates[1][0]-amount_coordinates[0][0],
                                                   amount_coordinates[1][1]-amount_coordinates[0][1]))
    except ValueError:
        amount_coordinates = []
        print('Please click again')
    except SystemError:
        amount_coordinates = []
        print('Please click again')
    else:
        if os.path.exists('Number.png'):
            img = Image.open('Number.png').resize((80, 80), Image.NEAREST)
            text = pytesseract.image_to_string(img, config="--psm 13").replace('\r', '').replace('\n', '')
            if len(text) == 1:
                break
            else:
                amount_coordinates = []
                text = ''
                print('Please click again')


while True:
    cont_coordinates = []
    with mouse.Listener(
        on_click=on_click_continue_coord) as listener:
        print('Click the top left corner, and bottom right corner of continue button')
        listener.join()
    try:
        x, y = pyautogui.locateCenterOnScreen('continue.png', 
            region=(cont_coordinates[0][0],
            cont_coordinates[0][1],
            cont_coordinates[1][0]-cont_coordinates[0][0],
            cont_coordinates[1][1]-cont_coordinates[0][1]),
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
            x_continue, y_continue = x, y
            break

# Speed time

os.system('cls')
while True: # Finding a way to make this quitable :)
    img = Image.open('Number.png').resize((80, 80), Image.NEAREST)
    amount = pytesseract.image_to_string(img, config="--psm 13").replace('\r', '').replace('\n', '')
    print(f'Amount of squares: {amount}')
    click(x_continue, y_continue)
    number_coordinates = []
    time.sleep(1)
    print('Detecting...')
    for i in range(1, int(amount)+1):
        x, y = None, None
        Generate_Text(str(i)) 
        while x is None:
            try:
                x, y = pyautogui.locateCenterOnScreen(f'{str(i)}.png', 
                    region=(coordinates[0][0],
                    coordinates[0][1],
                    coordinates[1][0]-coordinates[0][0],
                    coordinates[1][1]-coordinates[0][1]),
                    grayscale=True,
                    confidence=0.8)
                time.sleep(0.05)
            except TypeError:
                continue
                time.sleep(0.05)
            number_coordinates.append((x, y))
        os.remove(f'{str(i)}.png')
    for i in range(0, int(amount)):
        click(number_coordinates[i][0], number_coordinates[i][1])
        time.sleep(0.5)
    try:
        pyautogui.screenshot('Number.png', region=(amount_coordinates[0][0],
                                                   amount_coordinates[0][1],
                                                   amount_coordinates[1][0]-amount_coordinates[0][0],
                                                   amount_coordinates[1][1]-amount_coordinates[0][1]))
    except ValueError:
        print('Something goes wrong, exiting!')
        exit()
    time.sleep(1)
