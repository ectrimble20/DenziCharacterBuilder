import pygame


class SpriteLayerBuilder(object):

    def __init__(self):
        self.history = []
        self.image = None
        self._clear_image_surface()

    def add(self, image_surface):
        self._update_history()
        self.image.blit(image_surface, (0, 0))
        self.image.convert_alpha()

    def _update_history(self):
        self.history.append(self.image.copy())

    def revert(self):
        if len(self.history) > 0:
            self._clear_image_surface()
            self.image.blit(self.history.pop(), (0, 0))
            self.image.convert_alpha()

    def clear(self):
        self.history.clear()
        self._clear_image_surface()
        self._update_history()

    def _clear_image_surface(self):
        self.image = pygame.Surface([32, 32], flags=pygame.SRCALPHA).convert_alpha()
        self.image.fill((0, 0, 0, 0))


class SpriteComponentBuilder(object):

    def __init__(self):
        self.sprites = []

    def add(self, surface):
        self.sprites.append(surface)

    @property
    def image(self):
        i = pygame.Surface([32, 32], flags=pygame.SRCALPHA).convert_alpha()
        for surface in self.sprites:
            i.blit(surface, (0, 0))
        return i

    def revert(self):
        if len(self.sprites) > 0:
            self.sprites.pop()

    def clear(self):
        self.sprites.clear()