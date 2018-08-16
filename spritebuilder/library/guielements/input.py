import pygame
from spritebuilder.library.textrenderer import TextRenderer
from spritebuilder.library.keymap import keypad_set, mapping as key_map, shift_mapping


class TextInput(object):

    def __init__(self, parent, text="", default_text="", width="200", x=0, y=0, max_length=0
                 ):
        self._text_renderer = TextRenderer()
        self._text = []
        self._text_sprite = pygame.sprite.Sprite()
        self._text_sprite.image = pygame.Surface((width, 32))
        self._text_sprite.rect = self._text_sprite.image.get_rect()
        self._key_read_delay = 50
        self._key_read_timer = 0
        self._parent = parent

    def handle_input(self):
        if self._key_read_timer > self._key_read_delay:
            self._key_read_timer = 0
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self._parent.exit_hook()  # TODO remember to make this work
                if e.type == pygame.KEYDOWN:
                    k = key_map.get(e.key, None)
                    if k:
                        if e.mod in [pygame.KMOD_CAPS, pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT] \
                                and e.key not in keypad_set:
                            k = shift_mapping.get(k, k)
                        self._text.append(k)
                    # check for delete
                    if e.key in [pygame.K_DELETE, pygame.K_BACKSPACE] and len(self._text) > 0:
                        self._text.pop()

    def handle_updates(self, delta_time):
        self._key_read_timer += delta_time
        if len(self._text) > 0:
            text_rendered = self._text_renderer.small("".join(self._text))
            self._text_sprite.image.blit(text_rendered, (3, 5))

    def handle_draw(self, display):
        display.blit(self._text_sprite.image, self._text_sprite.rect)

    def mouse_over(self, mouse_rect):
        return self._text_sprite.rect.colliderect(mouse_rect)
