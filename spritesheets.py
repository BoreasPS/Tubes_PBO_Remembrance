import pygame
from settings import *

spritesheets_props = pygame.image.load('Texture/TX Props.png')
spritesheets_player_idle = pygame.image.load('graphics/test/Male 02-3.png')

crate = spritesheets_props.subsurface(160, 18, 32, 48)
block = spritesheets_props.subsurface(288, 306, 32, 46)
chest = spritesheets_props.subsurface(96, 30, 32, 32)
player_idle = spritesheets_player_idle.subsurface(32, 0, 32, 32)
player_walk_up1 = spritesheets_player_idle.subsurface(0, 96, 32, 32)
player_walk_up2 = spritesheets_player_idle.subsurface(32, 96, 32, 32)
player_walk_up3 = spritesheets_player_idle.subsurface(64, 96, 32, 32)
