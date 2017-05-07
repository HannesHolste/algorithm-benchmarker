import os

from littlebigo.master import add_dataset


class Dataset():
    def __init__(self, id, filepath, description=""):
        self.id = id
        self.filepath = filepath
        self.description = description

        if not os.path.exists(filepath):
            raise IOError('%s does not exist.' % filepath)

        add_dataset(self)
