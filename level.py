import pygame
from settings import *
from tile import Tile, Chest, TileBorder
from player import Player
from debugging import debug
from support import *


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprite = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

    def create_map(self):
        layouts = {
                'boundary' : import_csv_layout('map/Border_Border.csv')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for column_index, col in enumerate(row):
                    if col != '-1':
                        x = column_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            NewX= x/4
                            NewY= y/4
                            TileBorder((NewX,NewY), [self.obstacle_sprites], 'invisible')
                #if col == 'x':
                #    Tile((x, y), [self.visible_sprite, self.obstacle_sprites])
                #if col == 'p':
                #   self.player = Player((x, y), [self.visible_sprite], self.obstacle_sprites)
                #if col == 'c':
                #    Chest((x, y), [self.visible_sprite, self.obstacle_sprites])
        self.player = Player((1603, 100), [self.visible_sprite], self.obstacle_sprites)
    def run(self):
        self.visible_sprite.custom_draw(self.player)
        self.visible_sprite.update()
        debug(self.player.direction)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_heigth = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.floor_surf = pygame.image.load('map/ForestMap.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_heigth
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
