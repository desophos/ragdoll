from RagdollSpace import RagdollSpace
from Character import Character
from Enemy import Enemy
from globals import SCREEN_SIZE, FPS, STEP_TIME, CROSSHAIRS_SIZE, WALL_WIDTH, \
    COLLISION_GROUP, COLLISION_TYPE, PLAYER_MOVEMENT_SPEED, PLAYER_ID, \
    BULLET_PRUNING_VELOCITY, CHARACTER_ANGULAR_VELOCITY_LIMIT
from utility import *
from pymunk import pygame_util
import pygame
import pymunk
from random import random
from math import fabs, pi
from time import time

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(pygame.color.THECOLORS["white"])

space = RagdollSpace()
#space.gravity = (0.0,-900.0)

# used for keeping track of number of characters; the player is the first character defined
character_index = PLAYER_ID

me = Character(gun_type="shotgun", cid=character_index)
space.add_character(me)
character_index += 1
# create sprite group for the player
me_sprite = pygame.sprite.RenderPlain(me, me.gun)

num_enemies = 2
for i in range(num_enemies):
    pos = ( random() * (SCREEN_SIZE - WALL_WIDTH), random() * (SCREEN_SIZE - WALL_WIDTH) )
    space.add_character( Enemy( gun_type="pistol", pos=pos, cid=character_index ) )
    character_index += 1

# add walls

walls = [
    pymunk.Segment(space.static_body, (0, WALL_WIDTH/2), (SCREEN_SIZE, WALL_WIDTH/2), WALL_WIDTH),  # bottom
    pymunk.Segment(space.static_body, (WALL_WIDTH/2, 0), (WALL_WIDTH/2, SCREEN_SIZE), WALL_WIDTH),  # left
    pymunk.Segment(space.static_body, (0, SCREEN_SIZE-WALL_WIDTH/2), (SCREEN_SIZE, SCREEN_SIZE-WALL_WIDTH/2), WALL_WIDTH),  # top
    pymunk.Segment(space.static_body, (SCREEN_SIZE-WALL_WIDTH/2, 0), (SCREEN_SIZE-WALL_WIDTH/2, SCREEN_SIZE), WALL_WIDTH)  # right
]

for w in walls:
    w.color = pygame.color.THECOLORS["black"]
    w.friction = 1.0
    w.group = COLLISION_GROUP["wall"]
    w.collision_type = COLLISION_TYPE["wall"]

space.add(walls)


def get_bullet_body_owner(body):
    return [ b for b in space.bullets if b.body == body ][0]


def get_character_body_owner(body):
    return [ c for c in space.characters if body in c.bodies ][0]


def remove_body(shape):
    bullet_body_list = [b.body for b in space.bullets]
    character_body_list = collapse_list([c.bodies for c in space.characters])

    if shape.body in bullet_body_list:  # if this body is a bullet body
        # remove the bullet that owns this body
        space.remove_bullet( get_bullet_body_owner(shape.body) )
    elif shape.body in character_body_list:  # if this body is one of the bodies of a character
        # remove this body
        space.remove_character_body_part( shape.body, get_character_body_owner(shape.body) )


def check_hp(body_part_shape):
    if body_part_shape.body.hp <= 0:
        space.add_post_step_callback(remove_body, body_part_shape)


def hit(space, arbiter):
    # arbiter.shapes[0] is the bullet shape, [1] is the character body shape
    space.add_post_step_callback(remove_body, arbiter.shapes[0])
    arbiter.shapes[1].body.hp -= arbiter.total_impulse.length
    check_hp(arbiter.shapes[1])

space.add_collision_handler(COLLISION_TYPE["bullet"], COLLISION_TYPE["character"], begin=None, pre_solve=None, post_solve=hit, separate=None)

# add crosshairs at the location of the mouse
pointer_body = pymunk.Body()
pointer_shape1 = pymunk.Segment(pointer_body, (0, CROSSHAIRS_SIZE), (0, -CROSSHAIRS_SIZE), 1)  # vertical segment
pointer_shape2 = pymunk.Segment(pointer_body, (-CROSSHAIRS_SIZE, 0), (CROSSHAIRS_SIZE, 0), 1)  # horizontal segment

# add a spring that will angle the gun toward the mouse
#spring = pymunk.constraint.DampedRotarySpring(me.gun.body, pointer_body, 0, 125000., 6000.)
spring = pymunk.constraint.RotaryLimitJoint(me.gun.body, pointer_body, pi, pi)

space.add(pointer_shape1, pointer_shape2, spring)

pygame.key.set_repeat(1, 50)  # if a key is held down, continue sending KEYDOWN events

while True:
    # handle event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()

        elif event.type == pygame.KEYDOWN:

            # move head
            if event.key == pygame.K_w:
                me.move(PLAYER_MOVEMENT_SPEED, me.direction_enum["UP"])
            elif event.key == pygame.K_a:
                me.move(PLAYER_MOVEMENT_SPEED, me.direction_enum["LEFT"])
            elif event.key == pygame.K_d:
                me.move(PLAYER_MOVEMENT_SPEED, me.direction_enum["RIGHT"])
            elif event.key == pygame.K_s:
                me.move(PLAYER_MOVEMENT_SPEED, me.direction_enum["DOWN"])

            # rotate head
            #torso_vector = (me.bodies[me.bodies_enum["HEAD"]].position - me.bodies[me.bodies_enum["TORSO"]].position)
            #torso_rotate_angle = torso_vector.angle
            #elif event.key == pygame.K_q:
            #    me.rotate(CHARACTER_ANGULAR_VELOCITY_LIMIT, "TORSO")
            #elif event.key == pygame.K_e:
            #    me.rotate(-CHARACTER_ANGULAR_VELOCITY_LIMIT, "TORSO")

        elif event.type == pygame.MOUSEMOTION:
            # update location of pointer
            pointer_body.position = pygame_util.get_mouse_pos(screen)
            # update angle of pointer
            pointer_body.angle = (pointer_body.position - me.gun.body.position).angle

        elif event.type == pygame.MOUSEBUTTONDOWN:
            me.shoot_gun(space)

    for c in [c for c in space.characters if c.cid != PLAYER_ID]:  # eliminate player
        #print c.cid, "running basic ai"
        c.basic_ai(space)

    # prune a bullet if the bullet is outside the screen or has stopped moving
    for b in space.bullets[:]:  # iterate over a copy of the list
        if fabs(b.body.position.x - SCREEN_SIZE) > SCREEN_SIZE or \
           fabs(b.body.position.y - SCREEN_SIZE) > SCREEN_SIZE:
            space.remove_bullet(b)

        #print b.body.velocity.length
        if b.body.velocity.length < BULLET_PRUNING_VELOCITY:
            space.remove_bullet(b)

    # prune a character if the character's head or torso is gone
    for c in space.characters[:]:  # iterate over a copy of the list
        if c.bodies[c.bodies_enum["HEAD"]] not in space.bodies or \
           c.bodies[c.bodies_enum["TORSO"]] not in space.bodies:
            space.remove_character(c)

    for c in space.characters:
        if c.gun:
            c.gun.cooldown_timer = time()

    # blit background
    screen.blit(background, (0, 0))
    # draw stuff
    pygame_util.draw(screen, space)
    # update physics
    space.step(STEP_TIME)
    # flip display
    pygame.display.flip()
    # maintain FPS
    clock.tick(FPS)
