class ImageMapper(object):

    def __init__(self, image_object):
        self.key = image_object.get("key", None)
        self.alpha = Alpha(image_object.get("alpha", None))
        self.map_size = MapSizes(image_object.get("map_sizes", None))
        self.sprites = []
        for sprite_map_object in image_object.get("map"):
            self.sprites.append(SpriteMap(sprite_map_object))

    def is_valid(self):
        if self.key and self.map_size and len(self.sprites) > 0:
            return True
        else:
            return False


class MapSizes(object):

    def __init__(self, map_size_object):
        self.sprite_size = map_size_object.get("sprite_size", None)
        self.block_size = map_size_object.get("map_size", None)
        if self.block_size is None:
            self.block_size = self.sprite_size


class Alpha(object):

    def __init__(self, alpha_object):
        self.undefined = False
        if alpha_object:
            self.r = alpha_object.get("r", 0)
            self.g = alpha_object.get("g", 0)
            self.b = alpha_object.get("b", 0)
        else:
            self.undefined = True

    def get(self):
        # return as a tuple
        return self.r, self.g, self.b


class SpriteMap(object):

    def __init__(self, sprite_map_object):
        self.key = sprite_map_object.get("key", None)
        self.x = sprite_map_object.get("x", 0)
        self.y = sprite_map_object.get("y", 0)
