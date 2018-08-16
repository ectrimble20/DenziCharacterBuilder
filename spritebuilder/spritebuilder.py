import pygame
from spritebuilder.imagemanager import BuildAnImage, ImageManagerV2


class SpriteBuilder(object):
    """
    SpriteBuilder

    This is a program designed to allow you to build layered sprites from a template sprite sheet.
    For instance, the Denzi 32x32 paper doll fantasy set with some of the images mapped out is used
    but you can load all the images you'd like and they'll work with this program.

    See the README.md in the data directory for information on how to add new sprite sheets into the
    JSON file.
    """

    def __init__(self):
        self._display = pygame.display.set_mode((800, 600))
        self._running = False
        self._background_image = pygame.image.load("resources\\images\\sprite_builder_bg.png")
        self._small_preview_area = pygame.Surface((32, 32))  # (117, 151, 32, 32)  # centered inside small box
        self._large_preview_area = pygame.Surface((64, 64))  # (133, 301, 64, 64)  # large, scaled preview box
        self._large_preview_scale = 2.0  # normal is 32x32 we want the preview to be 64x64 so 2x it's size
        self._build_select_area = pygame.Surface((448, 448))  # (301, 135, 448, 448)
        self._sprites_per_row = 14  # number of sprites to display per row in the select area, 448/32
        # TODO we'll need save/clear buttons at some point too
        # debug - lets fill the areas with various colors to make sure they're showing
        # where I expect them to show
        self._small_preview_area.fill((255, 255, 255))
        self._large_preview_area.fill((255, 255, 255))
        self._build_select_area.fill((255, 255, 255))
        self._clock = pygame.time.Clock()
        self._delta_time = 0
        self._font = pygame.font.SysFont("Arial", 20, False, False)
        self._image_manager = ImageManagerV2()
        self._build_sprites_all = pygame.sprite.Group()
        self._build_sprites_show = pygame.sprite.Group()
        self._mouse_sprite = pygame.sprite.Sprite()
        self._mouse_sprite.rect = pygame.Rect((0, 0), (1, 1))
        self._text_group = pygame.sprite.Group()
        self._button_group = pygame.sprite.Group()
        self._sprite_builder = BuildAnImage()
        # click checks
        self._build_area_rect = pygame.Rect((301, 135), (448, 448))
        self._reload_sprite_groups = False
        self._build_position_offset = 0
        self._build_position_offset_max = 0

    def run(self):
        self._initialize_image_sprites()
        self._initialize_button_sprites()
        self._running = True
        while self._running:
            self._display.fill((0, 0, 0))
            self.handle_input()
            self.handle_update(self._delta_time)
            self.handle_draw()
            pygame.display.update()
            self._delta_time = self._clock.tick(60)
        pygame.quit()

    def handle_input(self):
        self._mouse_sprite.rect.x = pygame.mouse.get_pos()[0]
        self._mouse_sprite.rect.y = pygame.mouse.get_pos()[1]
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self._running = False
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    clicked = pygame.sprite.spritecollideany(self._mouse_sprite, self._build_sprites_show)
                    if clicked:
                        self._sprite_builder.add(clicked.tool_tip)
                        self._sprite_builder.build(self._image_manager)
                    # check for any hits against our buttons
                    action = pygame.sprite.spritecollideany(self._mouse_sprite, self._button_group)
                    if action:
                        if action.action == 'list_up':
                            self._move_images_up()
                        if action.action == 'list_down':
                            self._move_images_down()
                        if action.action == 'save':
                            if self._sprite_builder.built:
                                self._sprite_builder.save_image()
                                self._clear_preview()
                        if action.action == 'clear':
                            self._clear_preview()
                        if action.action == 'undo':
                            self._clear_preview(preserve_builder=True)
                            self._sprite_builder.revert_last()
                            self._sprite_builder.build(self._image_manager)
                if e.button == 5:
                    self._move_images_down()
                if e.button == 4:
                    self._move_images_up()
        self._text_group.empty()
        mouse_over = pygame.sprite.spritecollideany(self._mouse_sprite, self._build_sprites_show)
        if mouse_over:
            text = self._font.render(mouse_over.tool_tip, False, (0, 0, 0))
            text_sprite = pygame.sprite.Sprite()
            text_sprite.image = text
            text_sprite.rect = text_sprite.image.get_rect()
            text_sprite.rect.x = 450
            text_sprite.rect.y = 100
            self._text_group.add(text_sprite)

    def handle_update(self, delta_time):
        if self._sprite_builder.built:
            self._small_preview_area.blit(self._sprite_builder.get(), (0, 0))
            self._large_preview_area.blit(pygame.transform.scale(self._sprite_builder.get(), (64, 64)), (0, 0))
        if self._reload_sprite_groups:
            self._build_sprites_show.empty()
            for s in self._build_sprites_all.sprites():
                if self._build_area_rect.colliderect(s.rect):
                    self._build_sprites_show.add(s)
            self._reload_sprite_groups = False

    def handle_draw(self):
        self._display.blit(self._background_image, (0, 0))
        self._display.blit(self._small_preview_area, (118, 147))
        self._display.blit(self._large_preview_area, (134, 249))
        self._display.blit(self._build_select_area, (301, 135))
        self._build_sprites_show.draw(self._display)
        self._text_group.draw(self._display)

    def _initialize_image_sprites(self):
        image_keys = self._image_manager.get_keys()
        image_count = len(image_keys)
        print("Image Count: {}".format(image_count))
        self._build_position_offset_max = image_count // self._sprites_per_row
        if image_count % self._sprites_per_row != 0:
            self._build_position_offset_max += 1
        print("Calculated offset max: {}".format(self._build_position_offset_max))
        current_index = 0
        y_max = (self._build_position_offset_max * 32) + 135  # we need to this go on over the size of the container
        for y in range(135, y_max, 32):
            for x in range(301, 749, 32):
                s = pygame.sprite.Sprite()
                s.image = self._image_manager.get(image_keys[current_index])
                s.rect = s.image.get_rect()
                s.rect.x = x
                s.rect.y = y
                s.tool_tip = image_keys[current_index]
                self._build_sprites_all.add(s)
                current_index += 1
                if current_index >= image_count:
                    break
        self._reload_sprite_groups = True

    def _initialize_button_sprites(self):
        buttons = [
            {"key": "list_up", "rect": pygame.Rect((410, 118), (28, 13))},
            {"key": "list_down", "rect": pygame.Rect((410, 102), (28, 13))},
            {"key": "save", "rect": pygame.Rect((371, 100), (33, 32))},
            {"key": "clear", "rect": pygame.Rect((339, 94), (26, 38))},
            {"key": "undo", "rect": pygame.Rect((302, 104), (30, 30))}
        ]
        for d in buttons:
            s = pygame.sprite.Sprite()
            s.action = d['key']
            s.rect = d['rect']
            self._button_group.add(s)

    def _clear_preview(self, preserve_builder=False):
        self._small_preview_area.fill((255, 255, 255))
        self._large_preview_area.fill((255, 255, 255))
        if not preserve_builder:
            self._sprite_builder.clear()

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
