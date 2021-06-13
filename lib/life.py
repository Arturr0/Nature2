from copy import copy, deepcopy
from random import random, randint
from math import sin, cos, radians, degrees, floor, ceil, pi as PI, sqrt
import pygame.gfxdraw as gfxdraw
from pygame import Surface, Color, Rect
import pymunk as pm
from pymunk import Vec2d, Body, Circle, Segment, Space, Poly, Transform
from lib.math2 import flipy, ang2vec, ang2vec2, clamp
from lib.sensor import Sensor, PolySensor
from lib.net import Network
from lib.config import *

class Life(Body):

    def __init__(self, screen: Surface, space: Space, collision_tag: int, world_size: Vec2d, size: int, color0: Color, color1: Color, color2: Color=None, color3: Color=None, position: Vec2d=None):
        super().__init__(self, body_type=Body.KINEMATIC)
        self.world_size = world_size
        self.max_energy = 200
        self.energy = self.max_energy
        self.screen = screen
        self.color0 = color0
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.base_color0 = copy(color0)
        self.base_color1 = copy(color1)
        if position is not None:
            self.body.position = position
        else:
            x = randint(50, world_size[0]-50)
            y = randint(50, world_size[1]-50)
            self.position = (x, y)
        #if not angle:
        #    self.angle = random()*2*PI
        space.add(self)
        self.shape = Circle(body=self, radius=size, offset=(0, 0))
        self.shape.collision_type = collision_tag
        space.add(self.shape)
        self.reproduction_time = REPRODUCTION_TIME

    def draw(self, selected: Body):
        x = self.position.x; y = self.position.y
        r = self.shape.radius
        gfxdraw.filled_circle(self.screen, int(x), flipy(int(y)), int(r), self.color0)
        if r >= 3 and self.color1 != None:
            gfxdraw.filled_circle(self.screen, int(x), flipy(int(y)), int(r-2), self.color1)
        if r >= 6 and self.color3 != None:
            gfxdraw.filled_circle(self.screen, int(x), flipy(int(y)), int(2), self.color3)
        if self == selected:
            self.draw_selection(x, y, r)
        self.color0 = self.base_color0
        self.color1 = self.base_color1

    def update(self, dt: float):
        self.energy -= 1*dt*0.001
        if self.reproduction_time > 0:
            self.reproduction_time -= 1*dt*0.001

    def draw_selection(self, x, y, r):
        gfxdraw.aacircle(self.screen, int(x), int(flipy(y)), int(r*2), Color('turquoise'))
        gfxdraw.aacircle(self.screen, int(x), int(flipy(y)), int(r*2+1), Color('turquoise'))

    
class Plant(Life):

    def __init__(self, screen: Surface, space: Space, collision_tag: int, world_size: Vec2d, size: int, color0: Color, color1: Color, color2: Color=None, color3=None, position: Vec2d=None):
        super().__init__(screen=screen, space=space, collision_tag=collision_tag, world_size=world_size, size=3, color0=color0, color1=color1, color3=color3, position=position)
        self.life_time = PLANT_LIFE
        self.size = size
        self.max_size = PLANT_MAX_SIZE
        self.max_energy = pow(PLANT_MAX_SIZE, 2)
        self.color0 = Color('yellowgreen')
        self.color1 = Color('green')
        self.energy = 1

    def life_time_calc(self, dt: int):
        self.life_time -= dt/1000
        if self.life_time <= 0:
            return True
        return False

    def update(self, dt: float):
        if self.energy < self.max_energy and self.energy > 0:
            self.energy += PLANT_GROWTH/dt
            new_size = floor(sqrt(self.energy))
            if new_size != self.size:
                if new_size <= PLANT_MAX_SIZE:
                    self.shape.unsafe_set_radius(new_size)
                else:
                    self.shape.unsafe_set_radius(PLANT_MAX_SIZE)
        else:
            self.energy = self.max_energy
            self.size = self.max_size
        self.energy = clamp(self.energy, 0, self.max_energy)
        return

    def kill(self, space: Space):
        space.remove(self.shape)
        space.remove(self)

    def draw(self, selected: Body):
        super().draw(selected)

class Creature(Life):

    def __init__(self, screen: Surface, space: Space, collision_tag: int, world_size: Vec2d, size: int, color0: Color, color1: Color, color2: Color, color3: Color, angle: float=None, visual_range: int=180, position: Vec2d=None):
        super().__init__(screen=screen, space=space, collision_tag=collision_tag, world_size=world_size, size=size, color0=color0, color1=color1, position=position)
        if angle:
            self.angle = angle
        else:
            self.angle = random()*2*PI
        self.output = []
        self.color2 = color2
        self.color3 = color3
        self.neuro = Network()
        self.neuro.BuildRandom([12, 0, 3], 0.4)
        self.sensors = []
        self.eye_colors = {}
        self.visual_range = visual_range
        self.sensors = []
        self.reproduction_time = REPRODUCTION_TIME
        self.sensors.append(Sensor(screen, self, 4, 0, 220))
        space.add(self.sensors[0].shape)
        self.sensors.append(Sensor(screen, self, 4, PI/3, 220))
        space.add(self.sensors[1].shape)
        self.sensors.append(Sensor(screen, self, 4, -PI/3, 220))
        space.add(self.sensors[2].shape)

    def draw(self, selected: Body):
        super().draw(selected)
        x = self.position.x; y = self.position.y
        r = self.shape.radius
        rot = self.rotation_vector
        if r > 2:
            x2 = round(x + rot.x*(r-1))
            y2 = round(y + rot.y*(r-1))
            r2 = ceil(r/4)
            gfxdraw.filled_circle(self.screen, x2, flipy(y2), r2, self.color2)
        self.color0 = self.base_color0
        self.draw_energy_bar(int(x), flipy(int(y)))

    def draw_detectors(self):
        for detector in self.sensors:
            detector.draw()

    def update(self, space: Space, dt:float, detections: list=[]) -> None:
        #self.analize()
        move = self.move(dt)
        self.calc_energy(dt, move)
        self.reproduction_time -= 1/dt
        if self.reproduction_time <= 0:
            pass #!  REPRODUCTION CODE
            self.reproduction_time == REPRODUCTION_TIME

    def update_detections(self, detections: list): 
        for detector in self.sensors:
            if detector.shape in detections:
                detector.set_color(Color('red'))
            else:
                detector.set_color(Color('white'))

    def reproduce(self):
        new_creature = deepcopy(self)
        

    def move(self, dt: float) -> None:
        move = ((self.output[0]+1)/2)*SPEED/dt
        turn = self.output[1]*TURN/dt
        sensor_turn = self.output[2]*SENSOR_SPEED/dt
        self.angle = (self.angle+(turn))
        self.vdir = self.rotation_vector
        self.velocity = (move*self.rotation_vector.x, move*self.rotation_vector.y)
        self.sensors[1].rotate(sensor_turn, 0, PI/1.5)
        self.sensors[2].rotate(-sensor_turn, -PI/1.5, 0)
        return abs(move)*dt

    def calc_energy(self, dt: float, move: float):
        base_energy = BASE_ENERGY * dt
        move_energy = move * MOVE_ENERGY * dt
        self.energy -= (base_energy + move_energy)
        self.energy = clamp(self.energy, 0, self.max_energy)

    def get_input(self):
        input = []
        x = self.position[0]/self.world_size[0]
        input.append(x)
        y = self.position[1]/self.world_size[1]
        input.append(y)
        eng = self.energy/self.max_energy
        input.append(eng)
        for sensor in self.sensors:
            e, d, a = sensor.get_input()
            d = round(d, 3)
            a = round(a%PI, 3)
            input.append(e)
            input.append(d)
            input.append(a)
        return input

    def analize(self):
        input = self.get_input()
        self.output = self.neuro.Calc(input)
        for sensor in self.sensors:
            sensor.reset_data()
            
    def draw_energy_bar(self, rx: int, ry: int):
        bar_red = Color(255, 0, 0)
        bar_green = Color(0, 255, 0)
        size = self.shape.radius
        gfxdraw.box(self.screen, Rect(rx-round(10), ry+round(size+3), round(19), 1), bar_red)
        gfxdraw.box(self.screen, Rect(rx-round(10), ry+round(size+3), round(20*(self.energy/self.max_energy)), 1), bar_green)

    def kill(self, space: Space):
        for sensor in self.sensors:
            space.remove(sensor.shape)
        space.remove(self.shape)
        space.remove(self)

    def eat(self, energy: float):
        self.energy += energy * 20
        self.energy = clamp(self.energy, 0, self.max_energy)