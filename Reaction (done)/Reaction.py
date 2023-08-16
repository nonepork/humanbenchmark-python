from pynput import mouse
import win32api
import win32con
import pyautogui
import time
import os

global count
count = 0

def clicked(x, y, button, pressed):
    if pressed:
        return False


def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

print('Program starting in 5 second')
time.sleep(5)
os.system('cls')

with mouse.Listener(
    on_click=clicked) as listener:
    print('Now click text area to type and DONT MOVE :)')
    listener.join()

time.sleep(1)

while count != 5:
    time.sleep(0.09)
    x, y = pyautogui.position()
    r,g,b = pyautogui.pixel(x, y)
    if r == 92 and g == 219 and b == 115: 
        click(x, y)
        count+=1
