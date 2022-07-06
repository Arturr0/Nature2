from random import randint
from turtle import Vec2D
from pymunk import SegmentQueryInfo, Space, Arbiter, Vec2d, ShapeFilter
from pygame import Color
from lib.config import *
from lib.vision import Target, TARGET_TYPE
from lib.rock import Rock
from lib.creature import Creature

def line_of_sight(space: Space, start_vec: Vec2d, end_vec: Vec2d, filter: ShapeFilter) -> bool:
    query: SegmentQueryInfo=space.segment_query_first(start_vec, end_vec, 1.0, filter)
    if query == None:
        return True
    elif not isinstance(query.shape.body, Rock):
        return True
    else:
        return False

def diet(food: int, mod: float) -> float:
    return pow(food, 2) * mod

def set_collision_calls(space: Space, dt: float, creatures_num: int):
    #* 2: body | 8: rock | 4: sensor | 6: plant | 12: new_plant | 16: eye | 10: meat | 14: water | 18: area
    #COLLISIONS:
    creature_collisions = space.add_collision_handler(2, 2)
    creature_collisions.pre_solve = process_creatures_collisions
    creature_collisions.data['dt'] = dt

    creature_plant_collisions = space.add_collision_handler(2, 6)
    creature_plant_collisions.pre_solve = process_creature_plant_collisions
    creature_plant_collisions.data['dt'] = dt
    creature_plant_collisions.data['creatures_num'] = creatures_num

    creature_meat_collisions = space.add_collision_handler(2, 10)
    creature_meat_collisions.pre_solve = process_creature_meat_collisions
    creature_meat_collisions.data['dt'] = dt
    creature_meat_collisions.data['creatures_num'] = creatures_num

    creature_rock_collisions = space.add_collision_handler(2, 8)
    creature_rock_collisions.pre_solve = process_creatures_rock_collisions
    creature_rock_collisions.data['dt'] = dt

    creature_collisions_end = space.add_collision_handler(2, 2)
    creature_collisions_end.separate = process_creatures_collisions_end

    creature_plant_collisions_end = space.add_collision_handler(2, 6)
    creature_plant_collisions_end.separate = process_creatures_plant_collisions_end

    creature_meat_collisions_end = space.add_collision_handler(2, 10)
    creature_meat_collisions_end.separate = process_creatures_meat_collisions_end

    meat_rock_collisions = space.add_collision_handler(10, 8)
    meat_rock_collisions.pre_solve = process_meat_rock_collisions
    meat_rock_collisions.data['dt'] = dt

    meat_rock_collisions_end = space.add_collision_handler(10, 8)
    meat_rock_collisions_end.separate = process_meat_rock_collisions_end

    plant_rock_collisions = space.add_collision_handler(6, 8)
    plant_rock_collisions.pre_solve = process_plant_rock_collisions
    plant_rock_collisions.data['dt'] = dt

    plant_rock_collisions_end = space.add_collision_handler(6, 8)
    plant_rock_collisions_end.separate = process_plant_rock_collisions_end

    #DETECTIONS:
    creature_detection = space.add_collision_handler(4, 2)
    creature_detection.pre_solve = process_agents_seeing
   
    plant_detection = space.add_collision_handler(4, 6)
    plant_detection.pre_solve = process_plants_seeing
  
    meat_detection = space.add_collision_handler(4, 10)
    meat_detection.pre_solve = process_meats_seeing

    rock_detection = space.add_collision_handler(4, 8)
    rock_detection.pre_solve = process_rocks_seeing


def process_creatures_collisions(arbiter, space, data):
    dt = data['dt']
    agent: Creature = arbiter.shapes[0].body
    target: Creature = arbiter.shapes[1].body
    size0 = arbiter.shapes[0].radius
    size1 = arbiter.shapes[1].radius
    agent.position -= arbiter.normal*(size1/size0)*0.4
    target.position += arbiter.normal*(size0/size1)*0.4
    if agent.attacking:
        if abs(agent.rotation_vector.get_angle_degrees_between(arbiter.normal)) < 60:
            if (size0+randint(0, 6)) > (size1+randint(0, 6)):
                dmg = cfg.HIT * ((agent.size+agent.power)/2) * dt
                if target.hit(dmg):
                    agent.fitness += cfg.KILL2FIT
                    agent.kills += 1
                else:
                    agent.fitness += dmg*cfg.HIT2FIT
                eng = diet(agent.food, cfg.DIET_MOD) * dmg * cfg.DMG2ENG
                agent.eat(eng)
    agent.collide_creature = True
    return False

def process_creatures_collisions_end(arbiter, space, data):
    #arbiter.shapes[0].body.collide_creature = False
    return False


def process_creature_plant_collisions(arbiter, space, data):
    dt = data['dt']
    hunter = arbiter.shapes[0].body
    target = arbiter.shapes[1].body
    size0 = arbiter.shapes[0].radius
    size1 = arbiter.shapes[1].radius
    if size0 != 0:
        hunter.position -= arbiter.normal*(size1/size0)*0.4
    else:
        hunter.position -= arbiter.normal*0.2
    size1 = arbiter.shapes[1].radius
    if size1 != 0:
        target.position += arbiter.normal*(size0/size1)*0.4
    else:
        target.position += arbiter.normal*0.2
    if hunter.eating:
        if abs(hunter.rotation_vector.get_angle_degrees_between(arbiter.normal)) < 60:
            target.color0 = Color('yellow')
            eat = cfg.EAT * size0 * dt
            target.energy = target.energy - eat
            vege = diet(11-hunter.food, cfg.DIET_MOD)
            #vege = hunter.vege/((hunter.vege+hunter.meat)/2)
            plant_value = eat*vege*cfg.VEGE2ENG
            hunter.eat(plant_value)
            hunter.fitness += plant_value*cfg.VEGE2FIT/size0
    hunter.collide_plant = True
    return False

def process_creatures_plant_collisions_end(arbiter, space, data):
    #arbiter.shapes[0].body.collide_plant = False
    return False


def process_creature_meat_collisions(arbiter, space, data):
    dt = data['dt']
    hunter = arbiter.shapes[0].body
    target = arbiter.shapes[1].body
    size0 = arbiter.shapes[0].radius
    size1 = arbiter.shapes[1].radius
    #~ new changes
    if size0 != 0:
        hunter.position -= arbiter.normal*(size1/size0)*0.4
    else:
        hunter.position -= arbiter.normal*0.2
    size1 = arbiter.shapes[1].radius
    if size1 != 0:
        target.position += arbiter.normal*(size0/size1)*0.4
    else:
        target.position += arbiter.normal*0.2
    if hunter.eating:
        if abs(hunter.rotation_vector.get_angle_degrees_between(arbiter.normal)) < 60:
            target.color0 = Color('yellow')
            eat = cfg.EAT * size0 * dt
            target.energy = target.energy - eat
            meat = diet(hunter.food, cfg.DIET_MOD)
            meat_value = eat * meat * cfg.MEAT2ENG
            hunter.eat(meat_value)
            hunter.fitness += meat_value*cfg.MEAT2FIT/size0
    hunter.collide_meat = True
    return False

def process_creatures_meat_collisions_end(arbiter, space, data):
    #arbiter.shapes[0].body.collide_meat = False
    return False        


def process_creature_water_collisions(arbiter, space, data):
    arbiter.shapes[0].body.on_water = True
    return False

def process_creature_water_collisions_end(arbiter, space, data):
    arbiter.shapes[0].body.on_water = False
    return False


def process_creatures_rock_collisions(arbiter, space, data):
    arbiter.shapes[0].body.position -= arbiter.normal * 2.5
    arbiter.shapes[0].body.collide_something = True
    return False

def process_creatures_rock_collisions_end(arbiter, space, data):
    arbiter.shapes[0].body.collide_something = False
    return False


def process_meat_rock_collisions(arbiter, space, data):
    arbiter.shapes[0].body.position -= arbiter.normal
    return False

def process_meat_rock_collisions_end(arbiter, space, data):
    return False


def process_plant_rock_collisions(arbiter, space, data):
    arbiter.shapes[0].body.position -= arbiter.normal
    return False

def process_plant_rock_collisions_end(arbiter, space, data):
    return False



def process_agents_seeing(arbiter: Arbiter, space: Space, data):
    agent1: Creature = arbiter.shapes[0].body
    if not agent1.vision.observe:
        return False
    agent2: Creature = arbiter.shapes[1].body
    dist = agent2.position.get_dist_sqrd(agent1.position)
    if dist > agent1.vision.max_dist_enemy:
        return False
    close_object: bool=False
    filter: ShapeFilter=ShapeFilter()
    #? [[[TEST: add rot_vec*size]]]
    if not line_of_sight(space, agent1.position+agent1.rotation_vector*(agent1.size+2), agent2.position, filter):
        return False
    if pow((agent1.size*3+cfg.CLOSE_VISION), 2) >= dist:
        close_object = True
    v = agent2.position - agent1.position
    f = agent1.rotation_vector
    n = v.normalized()
    angle = f.get_angle_between(n)
    agent1.vision.add_detection(angle=angle, dist=int(dist), target=agent2, type='creature', close_object=close_object)
    return False

def process_agents_seeing_end(arbiter, space, data):
    return False


def process_plants_seeing(arbiter, space, data):
    agent1 = arbiter.shapes[0].body
    if not agent1.vision.observe:
        return False
    agent2 = arbiter.shapes[1].body
    dist = agent2.position.get_dist_sqrd(agent1.position)
    if dist > agent1.vision.max_dist_plant:
        return False
    close_object: bool=False
    filter: ShapeFilter=ShapeFilter()
    if not line_of_sight(space, agent1.position+agent1.rotation_vector*20, agent2.position, filter):
        return False
    if pow((agent1.size*3+cfg.CLOSE_VISION), 2) >= dist:
        close_object = True
    v = agent2.position - agent1.position
    f = agent1.rotation_vector
    n = v.normalized()
    angle = f.get_angle_between(n)
    agent1.vision.add_detection(angle=angle, dist=int(dist), target=agent2, type='plant', close_object=close_object)
    return False

def process_plants_seeing_end(arbiter, space, data):
    return False


def process_meats_seeing(arbiter, space, data):
    agent1 = arbiter.shapes[0].body
    if not agent1.vision.observe:
        return False
    agent2 = arbiter.shapes[1].body
    dist = agent2.position.get_dist_sqrd(agent1.position)
    if dist > agent1.vision.max_dist_meat:
        return False
    close_object: bool=False
    filter: ShapeFilter=ShapeFilter()
    if not line_of_sight(space, agent1.position+agent1.rotation_vector*20, agent2.position, filter):
        return False
    if pow((agent1.size*3+cfg.CLOSE_VISION), 2) >= dist:
        close_object = True
    v = agent2.position - agent1.position
    f = agent1.rotation_vector
    n = v.normalized()
    angle = f.get_angle_between(n)
    agent1.vision.add_detection(angle=angle, dist=int(dist), target=agent2, type='meat', close_object=close_object)
    return False

def process_meats_seeing_end(arbiter, space, data):
    return False


def process_rocks_seeing(arbiter: Arbiter, space, data):
    agent1 = arbiter.shapes[0].body
    if not agent1.vision.observe:
        return False
    rock = arbiter.shapes[1].body
    collisions = arbiter.contact_point_set
    rock_pos: Vec2d=None
    for col_point in collisions.points:
        if not rock_pos:
            rock_pos = col_point.point_b
        else:
            rock_pos += col_point.point_b
    if len(collisions.points) > 1:
        rock_pos = rock_pos/(len(collisions.points))
    dist = rock_pos.get_dist_sqrd(agent1.position)
    if dist > agent1.vision.max_dist_rock:
        return False
    v = rock_pos - agent1.position
    f = agent1.rotation_vector
    n = v.normalized()
    angle = f.get_angle_between(n)
    tg: Target=Target(TARGET_TYPE.ROCK, rock_pos, dist, angle)
    agent1.vision.add_detection(angle=angle, dist=int(dist), target=tg, type='rock', close_object=False)
    return False