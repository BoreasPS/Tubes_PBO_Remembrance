import pygame
from settings import *
from entity import Entity
from spritesheets import *
import random


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics enemy
        self.animations = {
            'idle': [skeleton_idle1.convert_alpha(), skeleton_idle2.convert_alpha(), skeleton_idle3.convert_alpha(),
                     skeleton_idle4.convert_alpha(), skeleton_idle5.convert_alpha(), skeleton_idle6.convert_alpha()],
            'move_down': [skeleton_walk_down1.convert_alpha(), skeleton_walk_down2.convert_alpha(),
                          skeleton_walk_down3.convert_alpha(), skeleton_walk_down4.convert_alpha(),
                          skeleton_walk_down5.convert_alpha(), skeleton_walk_down6.convert_alpha()],
            'move_left': [skeleton_walk_left1.convert_alpha(), skeleton_walk_left2.convert_alpha(),
                          skeleton_walk_left3.convert_alpha(), skeleton_walk_left4.convert_alpha(),
                          skeleton_walk_left5.convert_alpha(), skeleton_walk_left6.convert_alpha()],
            'move_right': [skeleton_walk_right1.convert_alpha(), skeleton_walk_right2.convert_alpha(),
                           skeleton_walk_right3.convert_alpha(), skeleton_walk_right4.convert_alpha(),
                           skeleton_walk_right5.convert_alpha(), skeleton_walk_right6.convert_alpha()],
            'move_up': [skeleton_walk_up1.convert_alpha(), skeleton_walk_up2.convert_alpha(),
                        skeleton_walk_up3.convert_alpha(), skeleton_walk_up4.convert_alpha(),
                        skeleton_walk_up5.convert_alpha(), skeleton_walk_up6.convert_alpha()],
            'attack': [skeleton_attack1.convert_alpha(), skeleton_attack2.convert_alpha(),
                       skeleton_attack3.convert_alpha(), skeleton_attack4.convert_alpha(),
                       skeleton_attack5.convert_alpha(), skeleton_attack6.convert_alpha(),
                       skeleton_attack7.convert_alpha(), skeleton_attack8.convert_alpha()]
            }

        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # movement
        self.hitbox = self.rect.inflate(-5, -5)
        self.obstacle_sprites = obstacle_sprites
        self.direction = pygame.math.Vector2()

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # interaksi
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 700

        # iframes
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300


    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        direction = self.get_player_distance_direction(player)[1]
        player_vec = pygame.math.Vector2(player.rect.center)
        enemy_vec = pygame.math.Vector2(self.rect.center)
        direc = player_vec - enemy_vec
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif self.notice_radius >= distance > self.attack_radius:
            if direction[0] < 0 and abs(direc[0]) >= abs(direc[1]):
                self.status = 'move_left'
            elif direction[1] > 0:
                self.status = 'move_down'
            elif direction[0] > 0 and abs(direc[0]) >= abs(direc[1]):
                self.status = 'move_right'
            elif direction[1] < 0:
                self.status = 'move_up'
        else:
            self.status = 'idle'

    def action(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
        if 'move' in self.status:
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        return distance, direction

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player):
        if self.vulnerable:
            self.health -= random.randint(player.stats['attack'] - 5, player.stats['attack'] + 10)
            print(self.health)
            if self.health <= 0:
                self.kill()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def update(self):
        self.move(self.speed)
        self.animate()
        self.cooldown()

    def enemy_update(self, player):
        self.get_status(player)
        self.action(player)
