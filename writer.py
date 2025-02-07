from pyautogui import *
from time import sleep
from os import system

class Writer:
    def __init__(self):
        self.app : str
        self.delay : float = 2.5
        self.interval : float = 0.1

    def open_app(self, app : str, *, parameter : str = ''):
        self.app = app
        try: 
            system(f"start {self.app} {parameter}")
            sleep(self.delay)
            press('enter')
        except Exception as e:
            print("Invalid app startup !!")

    def set_property(self, delay : float = 2.5, interval : float = 0.1):
        self.delay = delay
        self.interval = interval

    def type(self, content : str):
        write(content, interval = self.interval)

    def write_in_file(self, source : list[str], content : str, mode : str = 'w'):
        try:
            with open(source, mode) as file:
                file.write(''.join(content))
        except Exception as e:
            print("something went wrong")
