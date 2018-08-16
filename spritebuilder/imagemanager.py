import pygame
import json
import os
from datetime import datetime


class ImageManager(object):

    def __init__(self):
        self.images = {}
        self._load()

    def _load(self):
        fp = open("data\\image_mapping.json", "r")
        image_data = json.load(fp)
        fp.close()
        images = image_data["images"]
        for image_file_object in images:
            file_name = image_file_object["key"]
            alpha = (image_file_object["alpha"]["r"], image_file_object["alpha"]["g"], image_file_object["alpha"]["b"])
            slice_size = (image_file_object["slice_size"]["width"], image_file_object["slice_size"]["height"])
            image_map = image_file_object["map"]
            path = os.path.join("resources\\images", file_name)
            if not os.path.isfile(path):
                raise FileNotFoundError("Couldn't find file expected at {}".format(path))
            surface = pygame.image.load(path).convert_alpha()  # this fixed transparency issues with bliting
            surface.set_colorkey(alpha)
            # load from the map
            for i in image_map:
                sl = pygame.Surface([slice_size[0], slice_size[1]])
                sl.blit(surface, (0, 0), (i["x"], i["y"], i["x"]+slice_size[0], i["y"]+slice_size[1]))
                sl.set_colorkey(alpha)
                self.images[i["key"]] = sl.convert_alpha()
        # so this should load all the images if I got the structure right
        # lets do a "debug dump of all images loaded
        print("Image Manager has finished loading images from image_mapping.json, loaded {} images.".format(len(self.images)))

    def get(self, key):
        return self.images.get(key, None)

    def get_keys(self):
        keys = []
        for key in self.images.keys():
            keys.append(key)
        return keys


class BuildAnImage(object):

    def __init__(self, keys=None):
        if not keys:
            keys = []
        self.keys = keys
        self.image = None
        self.built = False

    def add(self, key):
        self.keys.append(key)

    def revert_last(self):
        if len(self.keys) > 0:
            self.keys.pop(len(self.keys)-1)

    def get(self):
        if not self.built:
            raise FileNotFoundError("You haven't built the image yet")
        if self.built:
            return self.image
        else:
            return None

    def save_image(self):
        if not self.built:
            raise FileNotFoundError("You haven't built the image yet")
        image_name = "img_"
        image_name += datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        image_name += ".png"
        pygame.image.save(self.image, os.path.join("data\\saved_images", image_name))

    def build(self, image_manager):
        if len(self.keys) > 0:
            base_image = image_manager.get(self.keys[0]).copy()
            for i in range(1, len(self.keys)):
                base_image.blit(image_manager.get(self.keys[i]), (0, 0))
            self.image = base_image
            self.built = True
        else:
            self.built = False

    def clear(self):
        self.keys.clear()
        self.built = False
        self.image = None


class ImageManagerV2(object):
    """
    ImageManagerV2 is a revamped version of V1.  The biggest difference is how it reads in the JSON mapping file.
    The old mapping style required you to put in an X and Y pixel coordinate, which could be quite tedious to
    figure out for a file.  V2 makes this easier by using "block position" rather than pixel positions.

    What this means is that you set a block size, and this is how the parser moves.  For instance if you have 32px
    sprites that might be spaced by 16px blocks, you can handle this by setting the sprite-size to 32 and the
    block-size to 16, then when you're populating the map you'll use multiples of the block-size to define the
    position.  So in this case, a position of x:4 y:3 would be calculated to x:64px y:48px and it would build the
    images Rect out to 64+32 (sprite-size) and 48+32.
    """

    def __init__(self):
        self.images = {}
        self._load()

    def _load(self):
        fp = open("data\\image_mapping_v2.json", "r")
        image_data = json.load(fp)
        fp.close()
        images = image_data["images"]
        for image_file_object in images:
            file_name = image_file_object["key"]
            alpha = (image_file_object["alpha"]["r"], image_file_object["alpha"]["g"], image_file_object["alpha"]["b"])
            # slice_size = (image_file_object["slice_size"]["width"], image_file_object["slice_size"]["height"])
            sizing = image_file_object["map_sizes"]
            image_map = image_file_object["map"]
            path = os.path.join("resources\\images", file_name)
            if not os.path.isfile(path):
                raise FileNotFoundError("Couldn't find file expected at {}".format(path))
            surface = pygame.image.load(path).convert_alpha()  # this fixed transparency issues with bliting
            surface.set_colorkey(alpha)
            # load from the map
            for i in image_map:
                sl = pygame.Surface((sizing["sprite_size"], sizing["sprite_size"]))
                x = i["x"]*sizing["block_size"]
                y = i["y"]*sizing["block_size"]
                sl.blit(surface, (0, 0), (x, y, x+sizing["sprite_size"], y+sizing["sprite_size"]))
                sl.set_colorkey(alpha)
                self.images[i["key"]] = sl.convert_alpha()
        # so this should load all the images if I got the structure right
        # lets do a "debug dump of all images loaded

    def get(self, key):
        return self.images.get(key, None)

    def get_keys(self):
        keys = []
        for key in self.images.keys():
            keys.append(key)
        return keys
