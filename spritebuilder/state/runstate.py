import pygame


class RunState(object):

    def __init__(self, application_ref, **kwargs):
        self.application = application_ref
        self._mouse_group = pygame.sprite.Group()
        self._mouse_sprite = pygame.sprite.Sprite(self._mouse_group)
        self._mouse_sprite.rect = pygame.Rect((0, 0), (1, 1))

    def handle_input(self):
        pass

    def handle_updates(self, delta_time):
        pass

    def handle_draw(self, display):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_destroy(self):
        pass

    def update_mouse_position(self):
        self._mouse_sprite.rect.topleft = pygame.mouse.get_pos()