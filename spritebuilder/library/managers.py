import os
import json
import pygame
from spritebuilder.library.mapper import ImageMapper


class PathManager(object):
    def __init__(self, config):
        self.resource_directory = config.SB_RESOURCES_DIRECTORY
        self.data_directory = config.SB_RESOURCES_DIRECTORY
        self.image_directory = config.SB_IMAGE_DIRECTORY
        self.saved_image_directory = config.SB_SAVE_IMAGE_DIRECTORY

    def find_image_file(self, image_name):
        image_path = os.path.join(self.image_directory, image_name)
        if os.path.isfile(image_path):
            return image_path
        else:
            return None

    def find_saved_image_file(self, saved_image_name):
        image_path = os.path.join(self.saved_image_directory, saved_image_name)
        if os.path.isfile(image_path):
            return image_path
        else:
            return None

    def find_data_file(self, file_name):
        file_path = os.path.join(self.data_directory, file_name)
        if os.path.isfile(file_path):
            return file_path
        else:
            return None

    @staticmethod
    def build_path(directory, append_path):
        return os.path.join(directory, append_path)


class ImageListManager(object):
    """
    Basically the "old" image manager.  Since image manager isn't a good name for this, it's been renamed
    to ImageListManger, which is designed to load and hold a sprite list as defined by our image mapping
    JSON file.

    This also implements optional "alpha"
    """

    def __init__(self):
        self._path_manager = PathManager()
        self.images = {}

    def import_mapping(self, mapping_file):
        file_path = self._path_manager.find_data_file(mapping_file)
        if not file_path:
            raise FileNotFoundError("Unable to find mapping file at {}".format(file_path))
        file_handle = open(file_path, "r")
        image_data = json.load(file_handle)
        file_handle.close()
        images = image_data.get("images", None)
        if not images:
            return None
        for image_object in images:
            mapper = ImageMapper(image_object)
            if not mapper.is_valid():
                raise RuntimeError("Unable to import JSON image object, invalid format")
            sprite_sheet_path = self._path_manager.find_image_file(mapper.key)
            if not sprite_sheet_path:
                raise FileNotFoundError("Unable to locate image sheet at {}".format(sprite_sheet_path))
            sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
            if mapper.alpha:
                sprite_sheet.set_colorkey(mapper.alpha.get())
            for sprite_map in mapper.sprites:
                sprite_surface = pygame.Surface((mapper.map_size.sprite_size, mapper.map_size.sprite_size))
                x = sprite_map.x * mapper.map_size.block_size
                y = sprite_map.y * mapper.map_size.block_size
                sprite_surface.blit(
                    sprite_sheet, (0, 0), (x, y, x+mapper.map_size.sprite_size, y+mapper.map_size.sprite_size)
                )
                if mapper.alpha:
                    sprite_surface.set_colorkey(mapper.alpha.get())
                self.images[sprite_map.key] = sprite_surface

    def get(self, key):
        return self.images.get(key, None)

    def get_keys(self):
        keys = []
        for key in self.images.keys():
            keys.append(key)
        return keys


class ImageManager(object):

    def __init__(self, config):
        self.config = config
        self.images = {}

    def add(self, image_key, surface):
        self.images[image_key] = surface

    def load(self, image_key, image_name, alpha=None):
        image_path = self.config.os_path_join_hook(self.config.SB_IMAGE_DIRECTORY, image_name)
        if not image_path:
            raise FileNotFoundError("Unable to locate image {} at {}".format(image_name, image_path))
        image_surface = pygame.image.load(image_path).convert_alpha()
        if alpha:
            image_surface.set_colorkey(alpha)
        self.add(image_key, image_surface)

    def get(self, image_key):
        return self.images.get(image_key, None)
