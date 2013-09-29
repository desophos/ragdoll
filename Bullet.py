'''
Created on Feb 12, 2013

@author: desophos
'''
import sys
sys.path.insert(0,'''../pymunk/trunk''')

from globals import COLLISION_GROUP, COLLISION_TYPE
import pygame
import pymunk

class Bullet(pygame.sprite.Sprite):
    from math import pi
    _bullet_types = {"single":{"radius":1,
                              "mass":0.1,
                              "number":1,
                              "spread":0
                              },
                     "flak":{"radius":1,
                             "mass":0.1,
                             "number":5,
                             "spread":pi/6
                             }
                     }
    def __init__(self, bullet_type="single"):
        attrs = self._bullet_types[bullet_type]
        r = self.radius = attrs["radius"]
        n = self.number = attrs["number"]
        s = self.spread = attrs["spread"]
        m = self.mass = attrs["mass"]
        mo = self.moment = pymunk.moment_for_circle(m, 0, r)
        
        # pygame init
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([r, r])
        self.rect = self.image.get_rect()

        # pymunk init
        
        self.body = pymunk.Body(m, mo)
        self.body_shape = pymunk.Circle(self.body, r)
        self.body_shape.color = pygame.color.THECOLORS["black"]
        self.body_shape.collision_type = COLLISION_TYPE["bullet"]
        #self.body_shape.group = COLLISION_GROUP["bullet"]
        
        #self.body.velocity_limit = BULLET_VELOCITY_LIMIT
