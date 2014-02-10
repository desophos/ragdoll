'''
Created on Feb 27, 2013

@author: desophos
'''
from utility import *
import pymunk
from Enemy import Enemy

class RagdollSpace(pymunk.Space):
    bullets = []
    characters = []
    
    def add_bullet(self, bullet):
        self.bullets.append(bullet)
        self.add(bullet.body, bullet.body_shape)
    
    def remove_bullet(self, bullet):
        self.bullets.remove(bullet)
        self.remove(*bullet.body.constraints)
        self.remove(*bullet.body.shapes)
        self.remove(bullet.body)
        
    def remove_gun(self, c):
        self.remove(*[j for j in c.gun.constraints if j in self.constraints])
        if c.gun.body_shape in self.shapes:
            self.remove(c.gun.body_shape)
        if c.gun.body in self.bodies:
            self.remove(c.gun.body)
    
    def add_character(self, c):
        self.characters.append(c)
        self.add(c.bodies, c.body_shapes, c.joints)
        if c.gun:
            self.add(c.gun.body, c.gun.body_shape, c.gun.constraints)
            
    def remove_character(self, c):
        self.characters.remove(c)
        if c.gun:
            self.remove_gun(c)
        if c.__class__ == Enemy:
            if c.targeter in self.constraints:
                self.remove(c.targeter)
        self.remove(*[j for j in c.joints if j in self.constraints])
        self.remove(*[s for s in c.body_shapes if s in self.shapes])
        self.remove(*[b for b in c.bodies if b in self.bodies])
            
    def remove_character_body_part(self, body, character):
        # if gun hand is removed, remove gun
        if body == character.bodies[character.bodies_enum["LOWER_ARM_L"]] and character.gun:
            self.remove_gun(character)
            if character.__class__ == Enemy:
                if character.targeter:
                    self.remove(character.targeter)
        
        #for c in body.constraints:
        #    for b in character.bodies:
        #        print c in b.constraints
        for i in range(len(character.bodies)):
            if body == character.bodies[i]:
                print "removing body", i, "from", character.cid
        self.remove(*[c for c in body.constraints if c in self.constraints])
        self.remove(*[s for s in body.shapes if s in self.shapes])
        self.remove(body)
