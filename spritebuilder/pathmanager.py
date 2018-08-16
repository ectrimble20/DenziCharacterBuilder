import os


class PathManager(object):

    def __init__(self, resource_directory="resources", data_directory="data"):
        self._resource_directory = resource_directory
        self._data_directory = data_directory
        self._image_directory = None
        self._saved_image_directory = None

    def _initialize_sub_directories(self):
        self._image_directory = os.path.join(self._resource_directory, "images")
        self._saved_image_directory = os.path.join(self._data_directory, "saved_images")

    def find_image_file(self, image_name):
        image_path = os.path.join(self._image_directory, image_name)
        if os.path.isfile(image_path):
            return image_path
        else:
            return None

    def find_saved_image_file(self, saved_image_name):
        image_path = os.path.join(self._saved_image_directory, saved_image_name)
        if os.path.isfile(image_path):
            return image_path
        else:
            return None

    def find_data_file(self, file_name):
        file_path = os.path.join(self._data_directory, file_name)
        if os.path.isfile(file_path):
            return file_path
        else:
            return None

    @staticmethod
    def build_path(directory, append_path):
        return os.path.join(directory, append_path)
