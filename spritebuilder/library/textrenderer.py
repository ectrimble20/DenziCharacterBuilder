import pygame


class TextRenderer(object):

    def __init__(self, font_name="Arial", size_sm=16, size_md=20, size_lg=24, color=(0, 0, 0)):
        self._font_color = color
        self._font_objects = {}
        sm_font = pygame.font.SysFont(font_name, size_sm)
        self._font_objects['small'] = sm_font
        md_font = pygame.font.SysFont(font_name, size_md)
        self._font_objects['medium'] = md_font
        lg_font = pygame.font.SysFont(font_name, size_lg)
        self._font_objects['large'] = lg_font

    def small(self, text, antialias=True):
        return self._font_objects['small'].render(text, antialias, self._font_color)

    def medium(self, text, antialias=True):
        return self._font_objects['medium'].render(text, antialias, self._font_color)

    def large(self, text, antialias=True):
        return self._font_objects['large'].render(text, antialias, self._font_color)
