from enum import Enum, IntEnum
from random import randrange, random

def log_to_file(msg: str, filename: str):
    f = open(filename, 'a')
    f.write(msg+"\n")
    f.close()

class Detection(IntEnum):
    CREATURE = 1
    PLANT = 2
    MEAT = 3
    ROCK = 4

class Timer():

    def __init__(self, interval: float, one_shoot: bool=True, autostart: bool=False, label: str=None, random_start:bool=False):
        self.run: bool=autostart
        self.interval = interval
        self.one_shoot = one_shoot
        self.label = label
        self.random: bool=random_start
        self.reset_time()

    def timeout(self, delta: float) -> bool:
        if not self.run:
            return False
        self.time += delta
        if self.time < self.interval:
            return False
        if self.one_shoot:
            self.time = 0
            self.run = False
        else:
            self.time -= self.interval
        return True

    def reset_time(self):
        if self.random:
            self.time = random()*self.interval
        else:
            self.time = 0

    def stop(self):
        self.run = False

    def start(self):
        self.run = True

    def restart(self):
        self.reset_time()
        self.run = True

    def set_timer(self, interval: float, one_shoot: bool=True):
        self.interval = interval
        self.one_shoot = one_shoot
        

