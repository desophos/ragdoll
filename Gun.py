'''
Created on Dec 29, 2012

@author: Daniel
'''
import sys
sys.path.insert(0,'''../pymunk/trunk''')

from globals import GUN_VELOCITY_LIMIT, GUN_ANGULAR_VELOCITY_LIMIT, COLLISION_GROUP
from Bullet import Bullet
import pygame
import pymunk

class Gun(pygame.sprite.Sprite):
    """ Describes a gun held by a Character.
        For now, this is just a line segment. """
    _gun_types = {"pistol":{"length":3,
                           "thickness":1,
                           "mass":1,
                           "force":50, # force exerted upon bullet upon firing
                           "handle":(3,0), # relative coordinates of the point at which the gun attaches to a Character's hand
                           "bullet":"single",
                           "cooldown":0.4 # seconds between each shot
                           },
                  "shotgun":{"length":6,
                             "thickness":1,
                             "mass":5,
                             "force":80,
                             "handle":(6,0),
                             "bullet":"flak",
                             "cooldown":1}
                 }
    
    def __init__(self, gun_type="pistol"):
        from time import time
        # set gun attributes
        
        attrs = self._gun_types[gun_type]
        l = self.length = attrs["length"]
        t = self.thickness = attrs["thickness"]
        m = self.mass = attrs["mass"]
        mo = self.moment = pymunk.moment_for_box(m, l, t)
        f = self.force = attrs["force"]
        h = self.handle = attrs["handle"]
        b = self.bullet = attrs["bullet"]
        c = self.cooldown = attrs["cooldown"]
        self.cooldown_timer = time() # timer between shots
        self.cooldown_timer_end = self.cooldown_timer + self.cooldown

        # pygame init
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([l, t])
        self.rect = self.image.get_rect()

        # pymunk init
        
        self.body = pymunk.Body(m, mo)
        self.body_shape = pymunk.Poly(self.body, [(0,0), (0,-t), (l,-t), (l,0)])
        self.body_shape.color = pygame.color.THECOLORS["black"]
        self.body_shape.group = COLLISION_GROUP["character"]
        self.constraints = []
        
        #self.body.velocity_limit = GUN_VELOCITY_LIMIT
        #self.body.angular_velocity_limit = GUN_ANGULAR_VELOCITY_LIMIT
    
    def shoot(self, space):
        if self.cooldown_timer_end - self.cooldown_timer <= 0:
            self.cooldown_timer_end = self.cooldown_timer + self.cooldown
            
            bullet = Bullet(self.bullet) # used just to access bullet.number -- bad way to do this :(
            bullets = []
            for i in range(bullet.number):
                bullets.append(Bullet(self.bullet))

            for b in bullets:
                space.add_bullet(b)
                b.body.position = self.body.position - self.handle
            
            f = pymunk.vec2d.Vec2d(self.force, 0)
            f.angle = self.body.angle
            
            if bullet.number == 1:
                bullets[0].body.apply_impulse(-f)
            elif bullet.number > 1:
                from random import random
                for b in bullets:
                    # calculate a random angle within the spread angle from the gun angle
                    f.angle = self.body.angle + random()*b.spread - b.spread
                    b.body.apply_impulse(-f)
            else:
                pass               
            
            # calculate the recoil using conservation of momentum
            recoil = 0
            for b in bullets:
                recoil += b.body.mass * b.body.velocity / self.body.mass

            from math import pi
            recoil.angle = -self.body.angle

            self.body.apply_impulse(recoil, self.handle)
