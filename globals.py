'''
Created on Dec 29, 2012

@author: Daniel
'''
import sys
sys.path.insert(0,'''../pymunk/trunk''')

from math import pi
from pymunk import moment_for_box

# velocity limits

CHARACTER_VELOCITY_LIMIT = 1000
CHARACTER_ANGULAR_VELOCITY_LIMIT = pi/2
GUN_VELOCITY_LIMIT = 1000
GUN_ANGULAR_VELOCITY_LIMIT = pi/16

# ragdoll constants

BODY_THICKNESS = 2
BODY_FRICTION = 0.5

# body.hp is subtracted based on the force of the bullet impact
BODY_HP = {"HEAD":200,
           "TORSO":400,
           "UPPER_ARM":150,
           "LOWER_ARM":100,
           "UPPER_LEG":200,
           "LOWER_LEG":150}

HEAD_RADIUS = 4
TORSO_LENGTH = 15
UPPER_ARM_LENGTH = 6
LOWER_ARM_LENGTH = 6
UPPER_LEG_LENGTH = 8
LOWER_LEG_LENGTH = 8

HEAD_MASS = 5
TORSO_MASS = 15
UPPER_ARM_MASS = 4
LOWER_ARM_MASS = 3
UPPER_LEG_MASS = 6
LOWER_LEG_MASS = 4

HEAD_MOMENT = moment_for_box(HEAD_MASS, HEAD_RADIUS, HEAD_RADIUS)
TORSO_MOMENT = moment_for_box(TORSO_MASS, BODY_THICKNESS, TORSO_LENGTH)
UPPER_ARM_MOMENT = moment_for_box(UPPER_ARM_MASS, BODY_THICKNESS, UPPER_ARM_LENGTH)
LOWER_ARM_MOMENT = moment_for_box(LOWER_ARM_MASS, BODY_THICKNESS, LOWER_ARM_LENGTH)
UPPER_LEG_MOMENT = moment_for_box(UPPER_LEG_MASS, BODY_THICKNESS, UPPER_LEG_LENGTH)
LOWER_LEG_MOMENT = moment_for_box(LOWER_LEG_MASS, BODY_THICKNESS, LOWER_LEG_LENGTH)

# pymunk angle starts on the negative x axis and increases counterclockwise
NECK_ROTATION_MIN = pi - pi/8
NECK_ROTATION_MAX = pi + pi/8
SHOULDER_L_ROTATION_MIN = pi/16
SHOULDER_L_ROTATION_MAX = pi - pi/16
SHOULDER_R_ROTATION_MIN = -pi + pi/16
SHOULDER_R_ROTATION_MAX = -pi/16
ELBOW_L_ROTATION_MIN = 0
ELBOW_L_ROTATION_MAX = pi - pi/16
ELBOW_R_ROTATION_MIN = -pi + pi/16
ELBOW_R_ROTATION_MAX = 0
HIP_L_ROTATION_MIN = -pi/2
HIP_L_ROTATION_MAX = 0
HIP_R_ROTATION_MIN = 0
HIP_R_ROTATION_MAX = pi/2
KNEE_L_ROTATION_MIN = 0
KNEE_L_ROTATION_MAX = pi - pi/16
KNEE_R_ROTATION_MIN = -pi + pi/16
KNEE_R_ROTATION_MAX = 0

# timing constants

FPS = 120
STEP_TIME = 1./FPS

# collision group enum

COLLISION_GROUP = {"wall":1,
                   "character":2,
                   "bullet":3
                   }

# collision type enum

COLLISION_TYPE = {"wall":1,
                  "character":2,
                  "bullet":3
                  }

# misc. constants

SCREEN_SIZE = 400
WALL_WIDTH = 10
CROSSHAIRS_SIZE = 3
BULLET_PRUNING_VELOCITY = 300 # velocity at which to remove bullets from space
PLAYER_MOVEMENT_SPEED = 200
ENEMY_MAX_SPEED = 200
PLAYER_ID = 100

def flipy(xy):
    return (xy[0], SCREEN_SIZE-xy[1])
