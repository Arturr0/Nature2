from json import loads

TITLE = "NATURE"
SUBTITLE = "v1.1.11" 
AUTHOR = "2019-2022 Artur Gwoździowski"

class Configuration():

    def __init__(self, filename: str):
        self.WORLD = None
        self.SCREEN = None
        self.ITER = None
        self.FPS = None

        self.PLANT_MAX_SIZE = None
        self.PLANT_GROWTH = None
        self.PLANT_INIT_NUM = None
        self.PLANT_MIN_NUM = None
        self.PLANT_MAX_NUM = None
        self.PLANT_LIFE = None
        self.PLANT_RANGE = None
        self.PLANT_EDGE = None

        self.CREATURE_MULTIPLY = None
        self.CREATURE_MIN_NUM = None
        self.CREATURE_MAX_NUM = None
        self.CREATURE_INIT_NUM = None
        self.CREATURE_MIN_SIZE = None
        self.CREATURE_MAX_SIZE = None
        self.CREATURES_SEP = None

        self.BASE_ENERGY = None
        self.MOVE_ENERGY = None
        self.REP_ENERGY = None

        self.EAT = None
        self.SPEED = None
        self.HIDE_SPEED = None
        self.TURN = None
        self.HIT = None

        self.REP_TIME = None
        self.MEM_TIME = None
        self.MEAT_TIME = None

        self.SENSOR_MAX_ANGLE = None
        self.CLOSE_VISION = None

        self.ROCK_NUM = None
        self.ROCK_SIZE_MIN = None
        self.ROCK_SIZE_MAX = None
        self.ROCK_VERT_MIN = None

        self.RANK_SIZE = None
        self.SIZE2ENG = None
        self.SIZE_COST = None
        self.POWER_COST = None
        self.CHILDS_NUM = None
        self.MEAT2ENG = None
        self.VEGE2ENG = None
        self.DMG2ENG = None
        self.HIT2FIT = None
        self.KILL2FIT = None
        self.VEGE2FIT = None
        self.MEAT2FIT = None
        self.DIFF = None
        self.AUTO_SAVE_TIME = None
        self.ATK_ENG = None
        self.EAT_ENG = None
        self.LINKS_RATE = None
        self.MUTATIONS = None
        self.DEL_LINK = None
        self.DEL_NODE = None
        self.TIME = None
        self.BORN2FIT = None
        self.RUN_TIME = None
        self.RUN_COST = None
        self.DIET_MOD = None
        self.SENSOR_RANGE = None
        self.MIN_CARNIVORES = None
        self.MIN_HERBIVORES = None
        self.NET = None
        self.RANK_DECAY = None
        self.STAT_PERIOD = None
        self.NEURON_MOD = None
        self.NET_BASE = None
        self.GENERATIONS_NUMBER = None
        self.NEURO_COST = None
        self.GRAPH_H = None
        self.GRAPH_V = None
        self.load_from_file2(filename)

    def load_from_file2(self, filename: str):
        f = open(filename, 'r')
        json_cfg = f.read()
        f.close()
        cfg = loads(json_cfg)
        for param in cfg:
            self.__setattr__(param, cfg[param])

    def load_from_file(self, filename: str):
        f = open(filename, 'r')
        json_cfg = f.read()
        f.close()
        cfg = loads(json_cfg)
        self.WORLD                  = cfg['WORLD']
        self.SCREEN                 = cfg['SCREEN']
        self.ITER                   = cfg['ITER']
        self.FPS                    = cfg['FPS']
        self.PLANT_MAX_SIZE         = cfg['PLANT_MAX_SIZE']
        self.PLANT_GROWTH           = cfg['PLANT_GROWTH']
        self.PLANT_INIT_NUM         = cfg['PLANT_INIT_NUM']
        self.PLANT_MIN_NUM          = cfg['PLANT_MIN_NUM']
        self.PLANT_MAX_NUM          = cfg['PLANT_MAX_NUM']
        self.PLANT_LIFE             = cfg['PLANT_LIFE']
        self.PLANT_RANGE            = cfg['PLANT_RANGE']
        self.PLANT_EDGE             = cfg['PLANT_EDGE']
        self.CREATURE_MULTIPLY      = cfg['CREATURE_MULTIPLY']
        self.CREATURE_MIN_NUM       = cfg['CREATURE_MIN_NUM']
        self.CREATURE_MAX_NUM       = cfg['CREATURE_MAX_NUM']
        self.CREATURES_SEP          = cfg['CREATURES_SEP']
        self.EAT                    = cfg['EAT']
        self.CREATURE_INIT_NUM      = cfg['CREATURE_INIT_NUM']
        self.BASE_ENERGY            = cfg['BASE_ENERGY']
        self.MOVE_ENERGY            = cfg['MOVE_ENERGY']
        self.REP_TIME               = cfg['REP_TIME']
        self.REP_ENERGY             = cfg['REP_ENERGY']
        self.SPEED                  = cfg['SPEED']
        self.HIDE_SPEED             = cfg["HIDE_SPEED"]
        self.TURN                   = cfg['TURN']
        self.CREATURE_MIN_SIZE      = cfg['CREATURE_MIN_SIZE']
        self.CREATURE_MAX_SIZE      = cfg['CREATURE_MAX_SIZE']
        self.HIT                    = cfg['HIT']
        self.MEM_TIME               = cfg['MEM_TIME']
        self.SENSOR_MAX_ANGLE       = cfg['SENSOR_MAX_ANGLE']
        self.CLOSE_VISION           = cfg['CLOSE_VISION']
        self.ROCK_NUM               = cfg['ROCK_NUM']
        self.ROCK_SIZE_MIN          = cfg['ROCK_SIZE_MIN']
        self.ROCK_SIZE_MAX          = cfg['ROCK_SIZE_MAX']
        self.ROCK_VERT_MIN          = cfg['ROCK_VERT_MIN']
        self.ROCK_VERT_MAX          = cfg['ROCK_VERT_MAX']
        self.RANK_SIZE              = cfg['RANK_SIZE']
        self.MEAT_TIME              = cfg['MEAT_TIME']
        self.SIZE2ENG               = cfg['SIZE2ENG']
        self.SIZE_COST              = cfg['SIZE_COST']
        self.POWER_COST             = cfg['POWER_COST']
        self.CHILDS_NUM             = cfg['CHILDS_NUM']
        self.MEAT2ENG               = cfg['MEAT2ENG']
        self.VEGE2ENG               = cfg['VEGE2ENG']
        self.DMG2ENG                = cfg['DMG2ENG']
        self.HIT2FIT                = cfg['HIT2FIT']
        self.KILL2FIT               = cfg['KILL2FIT']
        self.DIFF                   = cfg['DIFF']
        self.VEGE2FIT               = cfg['VEGE2FIT']
        self.MEAT2FIT               = cfg['MEAT2FIT'] 
        self.AUTO_SAVE_TIME         = cfg['AUTO_SAVE_TIME']
        self.ATK_ENG                = cfg['ATK_ENG']
        self.EAT_ENG                = cfg['EAT_ENG']
        self.LINKS_RATE             = cfg['LINKS_RATE']
        self.MUTATIONS              = cfg['MUTATIONS']
        self.DEL_LINK               = cfg['DEL_LINK']
        self.DEL_NODE               = cfg['DEL_NODE']
        self.TIME                   = cfg['TIME']
        self.BORN2FIT               = cfg['BORN2FIT']
        self.RUN_TIME               = cfg['RUN_TIME']
        self.RUN_COST               = cfg['RUN_COST']
        self.DIET_MOD               = cfg['DIET_MOD']
        self.SENSOR_RANGE           = cfg['SENSOR_RANGE']
        self.MIN_CARNIVORES         = cfg['MIN_CARNIVORES']
        self.MIN_HERBIVORES         = cfg['MIN_HERBIVORES']
        self.NET                    = cfg['NET']
        self.RANK_DECAY             = cfg['RANK_DECAY']
        self.STAT_PERIOD            = cfg['STAT_PERIOD']
        self.NEURON_MOD             = cfg['NEURON_MOD']
        self.NET_BASE               = cfg['NET_BASE']
        self.GENERATIONS_NUMBER     = cfg['GENERATIONS_NUMBER']
        self.NEURO_COST             = cfg['NEURO_COST']
        self.GRAPH_V                = cfg['GRAPH_V']
        self.GRAPH_H                = cfg['GRAPH_H']

cfg = Configuration('config.json')