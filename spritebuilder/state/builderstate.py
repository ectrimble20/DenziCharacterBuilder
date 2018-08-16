from spritebuilder.state.runstate import RunState
from spritebuilder.imagemanager import ImageManagerV2
from spritebuilder.library.textrenderer import TextRenderer
from spritebuilder.library.managers import ImageManager
from spritebuilder.library.gui import Button
from spritebuilder.library.spritelayerbuilder import SpriteLayerBuilder
from datetime import datetime
import pygame


class BuilderState(RunState):

    def __init__(self, application_ref, **kwargs):
        super().__init__(application_ref, **kwargs)
        self._bg_image = pygame.image.load(
            self.application.config.os_path_join_hook(self.application.config.SB_IMAGE_DIRECTORY, "background_1.png")
        )
        self._text_renderer = TextRenderer()
        # sprite groups
        self._logo_group = pygame.sprite.Group()
        self._tool_tip_group = pygame.sprite.Group()
        self._btn_group = pygame.sprite.Group()
        self._logo_sprite = pygame.sprite.Sprite(self._logo_group)
        self._logo_sprite.image = self._text_renderer.large("Sprite Builder - Build New Sprite")
        self._logo_sprite.rect = self._logo_sprite.image.get_rect()
        self._logo_sprite.rect.center = (400, 50)
        # image manager
        self._image_manager = ImageManager(self.application.config)
        self._image_managerv2 = ImageManagerV2()  # we'll need to clean this up
        # load button icons
        self._image_manager.load('btn_scroll_up', 'arrowUp.png')
        self._image_manager.load('btn_scroll_down', 'arrowDown.png')
        self._image_manager.load('btn_save', 'save.png')
        self._image_manager.load('btn_trash', 'trashcan.png')
        self._image_manager.load('btn_undo', 'return.png')
        # lets create our buttons here
        btn_scroll_up = Button("scroll_up", self._image_manager.get('btn_scroll_up'), (550, 120))
        btn_scroll_down = Button("scroll_down", self._image_manager.get('btn_scroll_down'), (600, 120))
        btn_save = Button("save", self._image_manager.get('btn_save'), (400, 120))
        btn_trash = Button("trash", self._image_manager.get('btn_trash'), (450, 120))
        btn_undo = Button("undo", self._image_manager.get('btn_undo'), (500, 120))
        self._btn_group.add([btn_save, btn_scroll_down, btn_scroll_up, btn_trash, btn_undo])
        self._small_preview_area = pygame.Surface((32, 32))  # (117, 151, 32, 32)  # centered inside small box
        self._large_preview_area = pygame.Surface((64, 64))  # (133, 301, 64, 64)  # large, scaled preview box
        self._huge_preview_area = pygame.Surface((128, 128))
        self._image_label_entry_area = pygame.Surface((256, 32))
        self._image_label_entry_area_rect = pygame.Rect((70, 100), (256, 32))
        self._large_preview_scale = 2.0  # normal is 32x32 we want the preview to be 64x64 so 2x it's size
        self._build_select_area = pygame.Surface((416, 384))  # (301, 135, 448, 448)
        self._sprites_per_row = 12  # number of sprites to display per row in the select area, 448/32
        # TODO we'll need save/clear buttons at some point too
        # debug - lets fill the areas with various colors to make sure they're showing
        # where I expect them to show
        self._small_preview_area.fill((255, 255, 255))
        self._large_preview_area.fill((255, 255, 255))
        self._huge_preview_area.fill((255, 255, 255))
        self._build_select_area.fill((255, 255, 255))
        self._image_label_entry_area.fill((255, 255, 255))
        self._image_label_selected = False
        self._image_label_text = []
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont("Arial", 20, False, False)
        # self._image_manager = ImageManagerV2()
        self._build_sprites_all = pygame.sprite.Group()
        self._build_sprites_show = pygame.sprite.Group()
        self._sprite_layer_builder = SpriteLayerBuilder()
        # self._sprite_layer_builder = SpriteComponentBuilder()
        # click checks
        self._build_area_rect = pygame.Rect((300, 175), (416, 384))
        self._reload_sprite_groups = False
        self._build_position_offset = 0
        self._build_position_offset_max = 0

    def handle_input(self):
        self.update_mouse_position()
        self._tool_tip_group.empty()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.application.change_state("main_menu")
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    clicked = pygame.sprite.spritecollideany(self._mouse_sprite, self._build_sprites_show)
                    if clicked:
                        print("Clicked<{}>".format(clicked.tool_tip))
                        self._sprite_layer_builder.add(self._image_managerv2.get(clicked.tool_tip))
                    # check for any hits against our buttons
                    action = pygame.sprite.spritecollideany(self._mouse_sprite, self._btn_group)
                    if action:
                        # debug, make sure actions are working
                        print("Action<{}>".format(action.action))
                        if action.action == 'list_up':
                            self._move_images_up()
                        if action.action == 'list_down':
                            self._move_images_down()
                        if action.action == 'save':
                            if len(self._image_label_text) > 0:
                                ts_file_name = "{}.png".format("".join(self._image_label_text))
                            else:
                                ts_file_name = "img_{}.png".format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
                            pygame.image.save(self._sprite_layer_builder.image,
                                              self.application.config.os_path_join_hook(
                                                  self.application.config.SB_SAVE_IMAGE_DIRECTORY, ts_file_name)
                                              )
                            self._sprite_layer_builder.clear()
                            self._image_label_text.clear()
                        if action.action == 'trash':
                            self._sprite_layer_builder.clear()
                            self._image_label_text.clear()
                        if action.action == 'undo':
                            self._sprite_layer_builder.revert()
                    if self._image_label_entry_area_rect.colliderect(self._mouse_sprite.rect):
                        print("Clicked on entry")
                        self._image_label_selected = True
                    else:
                        self._image_label_selected = False
                if e.button == 5:
                    self._move_images_down()
                if e.button == 4:
                    self._move_images_up()
            # attempt to handle key input on the label
            if e.type == pygame.KEYDOWN:
                if pygame.key.get_focused():
                    if self._image_label_selected:
                        if e.key == pygame.K_DELETE or e.key == pygame.K_BACKSPACE:
                            if len(self._image_label_text) > 0:
                                self._image_label_text.pop()
                        else:
                            if len(self._image_label_text) < 30:
                                if pygame.K_a <= e.key <= pygame.K_z:
                                    alpha_key = pygame.key.name(e.key)
                                    if e.mod in [pygame.KMOD_CAPS, pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT]:
                                        alpha_key = alpha_key.upper()
                                    self._image_label_text.append(alpha_key)
                                if e.key == pygame.K_UNDERSCORE:
                                    self._image_label_text.append("_")
                                if e.key == pygame.K_MINUS:
                                    self._image_label_text.append("-")

        mouse_over = pygame.sprite.spritecollideany(self._mouse_sprite, self._build_sprites_show)
        if mouse_over:
            text = self._font.render(mouse_over.tool_tip, False, (0, 0, 0))
            text_sprite = pygame.sprite.Sprite()
            text_sprite.image = text
            text_sprite.rect = text_sprite.image.get_rect()
            text_sprite.rect.x = 315
            text_sprite.rect.y = 150
            self._tool_tip_group.add(text_sprite)

    def handle_updates(self, delta_time):
        self._small_preview_area.fill((255, 255, 255))
        self._large_preview_area.fill((255, 255, 255))
        self._huge_preview_area.fill((255, 255, 255))
        if self._image_label_selected:
            self._image_label_entry_area.fill((255, 255, 255))
        else:
            self._image_label_entry_area.fill((220, 220, 220))
        text = self._text_renderer.small("".join(self._image_label_text))
        self._image_label_entry_area.blit(text, (3, 5))

        image = self._sprite_layer_builder.image
        self._small_preview_area.blit(image, (0, 0))
        self._large_preview_area.blit(pygame.transform.scale(image, (64, 64)), (0, 0))
        self._huge_preview_area.blit(pygame.transform.scale(image, (128, 128)), (0, 0))
        if self._reload_sprite_groups:
            self._build_sprites_show.empty()
            for s in self._build_sprites_all.sprites():
                if self._build_area_rect.colliderect(s.rect):
                    self._build_sprites_show.add(s)
            self._reload_sprite_groups = False

    def handle_draw(self, display):
        display.fill((0, 0, 0))
        display.blit(self._bg_image, (0, 0))
        self._logo_group.draw(display)
        self._btn_group.draw(display)
        display.blit(self._small_preview_area, (252, 175))
        display.blit(self._large_preview_area, (220, 223))
        display.blit(self._huge_preview_area, (156, 303))
        display.blit(self._build_select_area, (300, 175))
        display.blit(self._image_label_entry_area, (70, 100))
        self._build_sprites_show.draw(display)
        self._tool_tip_group.draw(display)

    def _initialize_image_sprites(self):
        image_keys = self._image_managerv2.get_keys()
        image_count = len(image_keys)
        self._build_position_offset_max = image_count // self._sprites_per_row
        if image_count % self._sprites_per_row != 0:
            self._build_position_offset_max += 1
        current_index = 0
        y_max = (self._build_position_offset_max * 32) + (175 - 32)  # this evens out the container
        try:
            for y in range(175, y_max, 32):
                for x in range(300, 718, 32):
                    # index check to try and prevent index errors
                    if current_index >= image_count:
                        break
                    s = pygame.sprite.Sprite()
                    s.image = self._image_managerv2.get(image_keys[current_index])
                    s.rect = s.image.get_rect()
                    s.rect.x = x
                    s.rect.y = y
                    s.tool_tip = image_keys[current_index]
                    self._build_sprites_all.add(s)
                    current_index += 1
        except IndexError:
            print("Index out of range on index {}".format(current_index))
            self.application.change_state("main_menu")
        self._reload_sprite_groups = True

    def _move_images_up(self):
        if self._build_position_offset > 0:
            for s in self._build_sprites_all.sprites():
                s.rect.y += 32
            self._build_position_offset -= 1
            self._reload_sprite_groups = True

    def _move_images_down(self):
        if self._build_position_offset < self._build_position_offset_max:
            for s in self._build_sprites_all.sprites():
                s.rect.y -= 32
            self._build_position_offset += 1
            self._reload_sprite_groups = True

    def on_enter(self):
        self._initialize_image_sprites()

    def on_exit(self):
        self._sprite_layer_builder.clear()
        self._build_sprites_all.empty()
        self._build_sprites_show.empty()

    def on_destroy(self):
        pass


