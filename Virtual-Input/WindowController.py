import time
from pynput.keyboard import Key, Controller
from pynput import mouse as mc
import keyboard as sht
mouse_controller = mc.Controller()

class WindowControl():
    def __init__(self):
        self.keyboard = Controller()

    def open_window(self):
        sht.press_and_release('windows')
        time.sleep(1)

        for char in 'notepad':
            self.keyboard.press(char)
            self.keyboard.release(char)
            time.sleep(0.2)

        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        time.sleep(2)

    def close_window(self):
        sht.press_and_release('alt+f4')

    def resize_window(self):
        sht.press('alt')
        sht.press('space')
        sht.press('r')
        sht.release('alt')
        sht.release('space')
        sht.release('r')

    def maximize_window(self):
        sht.press('alt')
        sht.press('space')
        sht.press('x')
        sht.release('alt')
        sht.release('space')
        sht.release('x')

    def toggle_window(self):
        sht.press('alt')
        sht.press_and_release('tab')
        sht.press_and_release('tab')
        sht.release('alt')
