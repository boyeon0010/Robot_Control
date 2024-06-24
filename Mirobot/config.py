# A_MAX  = {'x': -186.687, 'y': 67.953, 'z': 230.72, 'roll': 0.0, 'pitch': 0.0, 'yaw': 159.999}
# D_MAX  = {'x': 195.649, 'y': -34.515, 'z': 230.72, 'roll': 0.0, 'pitch': 0.0, 'yaw': -10.005}
# W_MAX  = {'x': 175.384, 'y': 30.94, 'z': 258.487, 'roll': 0.0, 'pitch': -10.0, 'yaw': 10.005}
# S_MAX  = {'x': 136.44, 'y': 114.459, 'z': 258.487, 'roll': 0.0, 'pitch': -10.0, 'yaw': 39.993}

KUP_1, KDOWN_1 = "a", "d"

KUP_2, KDOWN_2 = "s", "w"

KUP_3, KDOWN_3 = "k", "i" 

KUP_4, KDOWN_4 = "j", "l" 

KUP_5, KDOWN_5 = "down", "up"

KUP_6, KDOWN_6 = "left", "right"

ENDEF_1, ENDEF_2 , ENDEF_3= "space", "ctrl", "alt"

MIN_1, MAX_1 = -85 , 145

MIN_2, MAX_2 = -25 , 55

MIN_3, MAX_3 = -155 , 45

MIN_4, MAX_4 =  -330 , 330

MIN_5, MAX_5 =  -190 , 25

MIN_6, MAX_6 = -345 , 345

JOINT_ANGLE = 30

SPEED = 100

# Need Setting
PORTNAME :str = "Your Mirobot PORT"
HOST :str = "Your IP ADDRESS"
PORT :int = "Your PORT"

# Overriding instance.config.py
import os
if os.path.isfile("instance\config.py"):
    from instance.config import *