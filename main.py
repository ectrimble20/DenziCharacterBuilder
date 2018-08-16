"""
PG Denzi Character Builder

This is a library to let me build custom 32x32 character/RPG/icon guys from the Denzi images found
on




images:
32x32_character_armor_paperdoll_Denzi091016-3.png
32x32_character_jewelry_paperdoll_Denzi091016-1.png
32x32_character_weapons_paperdoll_Denzi091016-2.png
32x32_characters_paperdoll_Denzi091016-4.png
"""
import pygame

# from spritebuilder.spritebuilder_dev import SpriteBuilderDev
from spritebuilder.spritebuilder import SpriteBuilder

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.key.set_repeat(50, 50)
    builder = SpriteBuilder()
    builder.run()
