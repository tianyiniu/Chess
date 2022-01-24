import ctypes
import time
from ctypes import windll, Structure, c_long, byref

from charset_normalizer import detect

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    #return { "x": pt.x, "y": pt.y}
    return (pt.x, pt.y)

def detect_click(button, watchtime = 5):
    '''Waits watchtime seconds. Returns True on click, False otherwise'''
    if button in (1, '1', 'l', 'L', 'left', 'Left', 'LEFT'):
        bnum = 0x01
    elif button in (2, '2', 'r', 'R', 'right', 'Right', 'RIGHT'):
        bnum = 0x02

    start = time.time()
    while 1:
        if ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
            # ^ this returns either 0 or 1 when button is not being held down
            return queryMousePosition()
        elif time.time() - start >= watchtime:
            break
        time.sleep(0.001)
    return False

def mouse_move(): 
    input("1. Move chess board window into a comfortable position and resize if needed. Press any key to continue ...\n> ")
    print("RIGHT-CLICK once on the top-left corner. Do not move afterwards.")

    # Get from-square and to-square
    from_square = detect_click(2)
    print(from_square)
    time.sleep(3)
    to_square = detect_click(2)
    print(to_square)

    # Calculate chess board corrdinates

    # Return move string

mouse_move()