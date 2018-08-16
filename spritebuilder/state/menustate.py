from spritebuilder.state.runstate import RunState
from spritebuilder.library.gui import Button
from spritebuilder.library.textrenderer import TextRenderer
import pygame


class MenuState(RunState):

    def __init__(self, application_ref, **kwargs):
        super().__init__(application_ref, **kwargs)
        self._bg_image = pygame.image.load(
            self.application.config.os_path_join_hook(self.application.config.SB_IMAGE_DIRECTORY, "background_1.png")
        )
        self._text_renderer = TextRenderer()  # we'll just use the defaults
        # init groups
        self._logo_group = pygame.sprite.Group()
        self._btn_group = pygame.sprite.Group()
        # init text sprites and buttons
        self._logo_sprite = pygame.sprite.Sprite(self._logo_group)
        self._logo_sprite.image = self._text_renderer.large("Sprite Builder - Main Menu")
        self._logo_sprite.rect = self._logo_sprite.image.get_rect()
        self._logo_sprite.rect.center = (400, 50)
        self._mouse_sprite = pygame.sprite.Sprite()
        self._mouse_sprite.rect = pygame.Rect(0, 0, 1, 1)
        btn_menu = Button("new", self._text_renderer.medium("New Image"), (400, 150))
        btn_exit = Button("exit", self._text_renderer.medium("Exit"), (400, 250))
        btn_load = Button("load", self._text_renderer.medium("Load Image"), (400, 200))
        self._btn_group.add([btn_menu, btn_exit, btn_load])
        # setup menu

    def handle_input(self):
        self.update_mouse_position()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.application.stop()
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:  # left mouse button
                    clicked = pygame.sprite.spritecollideany(self._mouse_sprite, self._btn_group)
                    if clicked:
                        print("Clicked on <action {}>".format(clicked.action))
                        if clicked.action == "new":
                            self.application.change_state("builder")
                        if clicked.action == "exit":
                            self.application.stop()

    def handle_updates(self, delta_time):
        pass

    def handle_draw(self, display):
        display.blit(self._bg_image, (0, 0))
        self._logo_group.draw(display)
        self._btn_group.draw(display)

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_destroy(self):
        pass
