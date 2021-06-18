from random import random, randint
import pymunk
from pymunk import Vec2d, Space, Segment, Body, Circle, Shape
import pygame
from pygame import Color
from lib.config import *

def process_creature_plant_collisions(arbiter, space, data):
    dt = data['dt']
    arbiter.shapes[0].body.position -= arbiter.normal*0.5
    arbiter.shapes[1].body.position += arbiter.normal*0.2
    #if arbiter.normal.angle <= 0.5 and arbiter.normal.angle >= -0.5:
    hunter = arbiter.shapes[0].body
    target = arbiter.shapes[1].body
    target.color0 = Color('red')
    #if isinstance(hunter, Creature) and isinstance(target, Plant):
    target.energy = target.energy - EAT/dt
    if target.energy > 0:
        hunter.eat(EAT/dt*10)
    return True

def process_creatures_collisions(arbiter, space, data):
    dt = data['dt']
    arbiter.shapes[0].body.position -= arbiter.normal*0.5
    arbiter.shapes[1].body.position += arbiter.normal*0.5
    #if arbiter.normal.angle <= 0.5 and arbiter.normal.angle >= -0.5:
    size0 = arbiter.shapes[0].radius
    size1 = arbiter.shapes[1].radius
    if (size0+randint(0, 6)) > (size1+randint(0, 6)):
        arbiter.shapes[1].body.energy -= HIT/dt*10
        arbiter.shapes[1].body.color0=Color('red')
    return True

def process_edge_collisions(arbiter, space, data):
    #arbiter.shapes[0].body.angle += arbiter.normal.angle
    arbiter.shapes[0].body.position -= arbiter.normal * 1.5
    return True

def detect_creature(arbiter, space, data):
    creature = arbiter.shapes[0].body
    enemy = arbiter.shapes[1].body
    sensor_shape = arbiter.shapes[0]
    for sensor in creature.sensors:
        if sensor.shape == sensor_shape:
            sensor.set_color(Color('red'))
            pos0 = creature.position
            dist = pos0.get_distance(enemy.position)
            sensor.send_data(detect=True, distance=dist)
            break
    return True

def detect_plant(arbiter, space, data):
    creature = arbiter.shapes[0].body
    plant = arbiter.shapes[1].body
    sensor_shape = arbiter.shapes[0]
    for sensor in creature.sensors:
        if sensor.shape == sensor_shape:
            sensor.set_color(Color('green'))
            pos0 = creature.position
            dist = pos0.get_distance(plant.position)
            sensor.send_data2(detect=True, distance=dist)
            break
    return True

def detect_plant_end(arbiter, space, data):
    return True

def detect_creature_end(arbiter, space, data):
    return True