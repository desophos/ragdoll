'''
Created on Feb 22, 2013

@author: desophos
'''
from Character import Character
import pymunk
from globals import PLAYER_ID, ENEMY_MAX_SPEED

class Enemy(Character):        
    targeter = None
    
    def find_player(self, characters):
        return [ c for c in characters if c.cid==PLAYER_ID ][0]
        
    def angle_to_player(self, player):
        p_loc = player.bodies[self.bodies_enum["HEAD"]].position
        my_loc = self.bodies[self.bodies_enum["HEAD"]].position
        return (my_loc - p_loc).angle
    
    def distance_from_player(self, player):
        p_loc = player.bodies[self.bodies_enum["HEAD"]].position
        my_loc = self.bodies[self.bodies_enum["HEAD"]].position
        return (my_loc - p_loc).length
    
    def move_toward_player(self, characters, speed):
        #print "toward"
        from math import pi
        self.move(speed, pi/2+self.angle_to_player(self.find_player(characters)))
    
    def move_away_from_player(self, characters, speed):
        #print "away"
        from math import pi
        self.move(speed, -pi/2+self.angle_to_player(self.find_player(characters)))
        
    def maintain_distance(self, characters, min_dist, max_dist, speed):
        player_dist = self.distance_from_player(self.find_player(characters))
        if player_dist > max_dist:
            self.move_toward_player(characters, speed)
        elif player_dist < min_dist:
            self.move_away_from_player(characters, speed)
    
    def target_player(self, space, body_part_name):
        from math import pi
        from copy import deepcopy
        
        #previous_targeter = [ c for c in space.characters if c==self ][0].targeter
        if self.targeter:
            space.remove(self.targeter)
            
        player = self.find_player(space.characters)
        body_to_target = player.bodies[self.bodies_enum[body_part_name]]
        target = pymunk.Body(.01,.01)
        target.position = body_to_target.position
        space.add(target)
        space.add(pymunk.PinJoint(target, body_to_target, (0,0), (0,0)))
        
        self.targeter = pymunk.RotaryLimitJoint(self.gun.body, target, pi, pi)
        space.add(self.targeter)
        
    def avoid_bullets(self, space):
        from math import pi
        for b in space.bullets:
            # move away from the bullets
            self.move(ENEMY_MAX_SPEED, -(self.bodies[self.bodies_enum["HEAD"]].position - b.body.position).angle)
        
    def shoot_gun(self, space):
        clear_shot = True # i have a clear shot to the player
        gun_pos = self.gun.body.position
        target_pos = self.targeter.b.position
        for s in self.body_shapes:
            if s.segment_query(gun_pos, target_pos): # if the ray intersects my own body
                clear_shot = False # i don't have a clear shot to the player
        
        if clear_shot:
            self.gun.shoot(space)
        
    def basic_ai(self, space):
        # calculate ideal min_dist, max_dist, and speed
        min_dist = 100
        max_dist = 200
        speed = ENEMY_MAX_SPEED
        self.maintain_distance(space.characters, min_dist, max_dist, speed)
        if self.targeter == None:
            # calculate which body part to target
            body_part_name = "HEAD"
            self.target_player(space, body_part_name)
        self.avoid_bullets(space)
        self.shoot_gun(space)
