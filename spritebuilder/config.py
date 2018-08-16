import os


class Config(object):
    SB_DATA_DIRECTORY = "data"
    SB_RESOURCES_DIRECTORY = "resources"
    SB_IMAGE_DIRECTORY = os.path.join(SB_RESOURCES_DIRECTORY, "images")
    SB_SAVE_IMAGE_DIRECTORY = os.path.join(SB_DATA_DIRECTORY, "saved_images")
    SB_SCREEN_WIDTH = 800
    SB_SCREEN_HEIGHT = 600
    SB_FPS = 60

    def os_path_join_hook(self, directory, join):
        return os.path.join(directory, join)

