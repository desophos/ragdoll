from Gun import Gun
from Bullet import Bullet
from globals import *
import pygame
import pymunk


class Character(pygame.sprite.Sprite):
    """ Describes a moving character ingame made up of pymunk bodies/shapes. """

    bodies_enum = {
        "HEAD": 0,
        "TORSO": 1,
        "UPPER_ARM_L": 2,
        "UPPER_ARM_R": 3,
        "LOWER_ARM_L": 4,
        "LOWER_ARM_R": 5,
        "UPPER_LEG_L": 6,
        "UPPER_LEG_R": 7,
        "LOWER_LEG_L": 8,
        "LOWER_LEG_R": 9,
    }

    from math import pi
    direction_enum = {
        "UP": 0,
        "LEFT": pi/2,
        "DOWN": pi,
        "RIGHT": 3*pi/2
    }

    def __init__( self, body_type="ragdoll", gun_type=None, w=10, h=10, pos=(SCREEN_SIZE/2, SCREEN_SIZE/2), cid=COLLISION_GROUP["character"] ):
        self.cid = cid  # character id

        # pygame init

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([w, h])
        self.rect = self.image.get_rect()

        # pymunk init

        # construct the character's body here

        if body_type == "ragdoll":

            # create the body pieces

            head = pymunk.Body(HEAD_MASS, HEAD_MOMENT)
            torso = pymunk.Body(TORSO_MASS, TORSO_MOMENT)
            upper_arm_l = pymunk.Body(UPPER_ARM_MASS, UPPER_ARM_MOMENT)
            upper_arm_r = pymunk.Body(UPPER_ARM_MASS, UPPER_ARM_MOMENT)
            lower_arm_l = pymunk.Body(LOWER_ARM_MASS, LOWER_ARM_MOMENT)
            lower_arm_r = pymunk.Body(LOWER_ARM_MASS, LOWER_ARM_MOMENT)
            upper_leg_l = pymunk.Body(UPPER_LEG_MASS, UPPER_LEG_MOMENT)
            upper_leg_r = pymunk.Body(UPPER_LEG_MASS, UPPER_LEG_MOMENT)
            lower_leg_l = pymunk.Body(LOWER_LEG_MASS, LOWER_LEG_MOMENT)
            lower_leg_r = pymunk.Body(LOWER_LEG_MASS, LOWER_LEG_MOMENT)

            self.bodies = [head,
                           torso,
                           upper_arm_l,
                           upper_arm_r,
                           lower_arm_l,
                           lower_arm_r,
                           upper_leg_l,
                           upper_leg_r,
                           lower_leg_l,
                           lower_leg_r
                           ]

            # give the body pieces shapes

            head_shape = pymunk.Circle(head, HEAD_RADIUS)
            torso_shape = pymunk.Poly(torso, [(0,0), (0,TORSO_LENGTH), (BODY_THICKNESS, TORSO_LENGTH), (BODY_THICKNESS,0)])
            upper_arm_l_shape = pymunk.Poly(upper_arm_l, [(0,0), (0,UPPER_ARM_LENGTH), (BODY_THICKNESS, UPPER_ARM_LENGTH), (BODY_THICKNESS,0)])
            upper_arm_r_shape = pymunk.Poly(upper_arm_r, [(0,0), (0,UPPER_ARM_LENGTH), (BODY_THICKNESS, UPPER_ARM_LENGTH), (BODY_THICKNESS,0)])
            lower_arm_l_shape = pymunk.Poly(lower_arm_l, [(0,0), (0,LOWER_ARM_LENGTH), (BODY_THICKNESS, LOWER_ARM_LENGTH), (BODY_THICKNESS,0)])
            lower_arm_r_shape = pymunk.Poly(lower_arm_r, [(0,0), (0,LOWER_ARM_LENGTH), (BODY_THICKNESS, LOWER_ARM_LENGTH), (BODY_THICKNESS,0)])
            upper_leg_l_shape = pymunk.Poly(upper_leg_l, [(0,0), (0,UPPER_LEG_LENGTH), (BODY_THICKNESS, UPPER_LEG_LENGTH), (BODY_THICKNESS,0)])
            upper_leg_r_shape = pymunk.Poly(upper_leg_r, [(0,0), (0,UPPER_LEG_LENGTH), (BODY_THICKNESS, UPPER_LEG_LENGTH), (BODY_THICKNESS,0)])
            lower_leg_l_shape = pymunk.Poly(lower_leg_l, [(0,0), (0,LOWER_LEG_LENGTH), (BODY_THICKNESS, LOWER_LEG_LENGTH), (BODY_THICKNESS,0)])
            lower_leg_r_shape = pymunk.Poly(lower_leg_r, [(0,0), (0,LOWER_LEG_LENGTH), (BODY_THICKNESS, LOWER_LEG_LENGTH), (BODY_THICKNESS,0)])

            self.body_shapes = [head_shape,
                                torso_shape,
                                upper_arm_l_shape,
                                upper_arm_r_shape,
                                lower_arm_l_shape,
                                lower_arm_r_shape,
                                upper_leg_l_shape,
                                upper_leg_r_shape,
                                lower_leg_l_shape,
                                lower_leg_r_shape
                                ]

            for s in self.body_shapes:
                s.color = pygame.color.THECOLORS["black"]
                s.group = cid
                s.collision_type = COLLISION_TYPE["character"]

            # set positions of bodies

            offset = 0

            torso.position = pos
            head.position = (torso.position.x, torso.position.y + TORSO_LENGTH/2 + HEAD_RADIUS + offset)
            upper_arm_l.position = (torso.position.x-offset, torso.position.y + TORSO_LENGTH/2)
            upper_arm_r.position = (torso.position.x+offset, torso.position.y + TORSO_LENGTH/2)
            lower_arm_l.position = (upper_arm_l.position.x-offset, upper_arm_l.position.y - UPPER_ARM_LENGTH/2)
            lower_arm_r.position = (upper_arm_r.position.x+offset, upper_arm_r.position.y - UPPER_ARM_LENGTH/2)
            upper_leg_l.position = (torso.position.x-offset, torso.position.y - TORSO_LENGTH/2)
            upper_leg_r.position = (torso.position.x+offset, torso.position.y - TORSO_LENGTH/2)
            lower_leg_l.position = (upper_leg_l.position.x-offset, upper_leg_l.position.y - UPPER_LEG_LENGTH/2)
            lower_leg_r.position = (upper_leg_r.position.x+offset, upper_leg_r.position.y - UPPER_LEG_LENGTH/2)

            # link pieces of the body together
            # attach bodies at midpoints of edges
            self.joints = [pymunk.PivotJoint(head, torso, (0,-HEAD_RADIUS), (BODY_THICKNESS/2,0)),
                           pymunk.PivotJoint(torso, upper_arm_l, (0,0), (BODY_THICKNESS/2,0)),
                           pymunk.PivotJoint(torso, upper_arm_r, (BODY_THICKNESS,0), (BODY_THICKNESS/2,0)),
                           pymunk.PivotJoint(upper_arm_l, lower_arm_l, (BODY_THICKNESS/2,UPPER_ARM_LENGTH), (BODY_THICKNESS/2,0)),
                           pymunk.PivotJoint(upper_arm_r, lower_arm_r, (BODY_THICKNESS/2,UPPER_ARM_LENGTH), (BODY_THICKNESS/2,0)),
                           pymunk.PivotJoint(torso, upper_leg_l, (0,TORSO_LENGTH), (BODY_THICKNESS/2,0)),
                           pymunk.PivotJoint(torso, upper_leg_r, (BODY_THICKNESS,TORSO_LENGTH), (BODY_THICKNESS/2,0)),
                           pymunk.PivotJoint(upper_leg_l, lower_leg_l, (BODY_THICKNESS/2,UPPER_LEG_LENGTH), (BODY_THICKNESS/2,0)),
                           pymunk.PivotJoint(upper_leg_r, lower_leg_r, (BODY_THICKNESS/2,UPPER_LEG_LENGTH), (BODY_THICKNESS/2,0))
                           ]

            # set joint rotation constraints

            neck_rot = pymunk.RotaryLimitJoint(head, torso, NECK_ROTATION_MIN, NECK_ROTATION_MAX)
            shoulder_rot_l = pymunk.RotaryLimitJoint(torso, upper_arm_l, SHOULDER_L_ROTATION_MIN, SHOULDER_L_ROTATION_MAX)
            shoulder_rot_r = pymunk.RotaryLimitJoint(torso, upper_arm_r, SHOULDER_R_ROTATION_MIN, SHOULDER_R_ROTATION_MAX)
            elbow_rot_l = pymunk.RotaryLimitJoint(upper_arm_l, lower_arm_l, ELBOW_L_ROTATION_MIN, ELBOW_L_ROTATION_MAX)
            elbow_rot_r = pymunk.RotaryLimitJoint(upper_arm_r, lower_arm_r, ELBOW_R_ROTATION_MIN, ELBOW_R_ROTATION_MAX)
            hip_rot_l = pymunk.RotaryLimitJoint(torso, upper_leg_l, HIP_L_ROTATION_MIN, HIP_L_ROTATION_MAX)
            hip_rot_r = pymunk.RotaryLimitJoint(torso, upper_leg_r, HIP_R_ROTATION_MIN, HIP_R_ROTATION_MAX)
            knee_rot_l = pymunk.RotaryLimitJoint(upper_leg_l, lower_leg_l, KNEE_L_ROTATION_MIN, KNEE_L_ROTATION_MAX)
            knee_rot_r = pymunk.RotaryLimitJoint(upper_leg_r, lower_leg_r, KNEE_R_ROTATION_MIN, KNEE_R_ROTATION_MAX)

            self.joints.extend([neck_rot,
                                shoulder_rot_l,
                                shoulder_rot_r,
                                elbow_rot_l,
                                elbow_rot_r,
                                hip_rot_l,
                                hip_rot_r,
                                knee_rot_l,
                                knee_rot_r
                                ])

            # now give each body part a number of hit points before it is destroyed

            hp = [BODY_HP["HEAD"],
                  BODY_HP["TORSO"],
                  BODY_HP["UPPER_ARM"],
                  BODY_HP["UPPER_ARM"],
                  BODY_HP["LOWER_ARM"],
                  BODY_HP["LOWER_ARM"],
                  BODY_HP["UPPER_LEG"],
                  BODY_HP["UPPER_LEG"],
                  BODY_HP["LOWER_LEG"],
                  BODY_HP["LOWER_LEG"]
                  ]

            for i in range(len(self.bodies)):
                self.bodies[i].hp = hp[i]

            # finally done creating the body! phew!

        if gun_type:
            # locate the gun at the character's right hand
            self.gun = Gun(gun_type)
            self.gun.body.position = (self.bodies[self.bodies_enum["LOWER_ARM_L"]].position.x + BODY_THICKNESS/2,
                                      self.bodies[self.bodies_enum["LOWER_ARM_L"]].position.y + LOWER_ARM_LENGTH)
            self.gun.constraints = [pymunk.PivotJoint(self.bodies[self.bodies_enum["LOWER_ARM_L"]], self.gun.body, (BODY_THICKNESS/2, LOWER_ARM_LENGTH), self.gun.handle),  # stick 'em together
                                    pymunk.RotaryLimitJoint(self.bodies[self.bodies_enum["LOWER_ARM_L"]], self.gun.body, -pi/8, 0)  # set a rotary limit so the gun can't rotate around the whole arm
                                    ]
        else:
            self.gun = None

        for b in self.bodies:
            b.velocity_limit = CHARACTER_VELOCITY_LIMIT
            #b.angular_velocity_limit = CHARACTER_ANGULAR_VELOCITY_LIMIT

        for b in self.body_shapes:
            b.color = pygame.color.THECOLORS["black"]
            b.friction = BODY_FRICTION
            b.collision_type = COLLISION_TYPE["character"]

    def move(self, force, angle, body_part="HEAD"):
        #print angle
        v = pymunk.Vec2d(0, force)
        v.rotate(angle)
        #print v
        self.bodies[self.bodies_enum[body_part]].apply_impulse(v)  # multiply vector by scalar force

    def rotate(self, torque, body_part="HEAD"):
        self.bodies[self.bodies_enum[body_part]].angular_velocity = torque

    def update(self):
        self.gun.update()

    def shoot_gun(self, space):
        self.gun.shoot(space)
