import os

from littlebigo.master import add_dataset


class Dataset():
    def __init__(self, id, filepath, description=""):
        """
        Initializes a data file, thus keeping track of it globally.

        :param id: string identifier or dict of key-value pairs. A dict is
            generally used when there are several identifiers used to track
            this item (for example: name, date, location) that might be
            queried or extracted separately later. Note that the dict cannot
            have any levels of nesting.
        :param filepath:
        :param description:
        """
        if not isinstance(id, str) and not isinstance(id, dict):
            raise ValueError('id must be either string or dict')

        if isinstance(id, dict):
            for v in id.values():
                if isinstance(v, dict):
                    raise ValueError('id as dict must have no deeper levels of'
                                     ' nesting')

        self.id = id
        self.filepath = filepath
        self.description = repr(description)

        if not os.path.exists(filepath):
            raise IOError('%s does not exist.' % filepath)

        add_dataset(self)

    def __hash__(self):
        if isinstance(self.id, str):
            return hash(self.id)
        elif isinstance(self.id, dict):
            return hash(frozenset(self.id.items()))
        else:
            raise ValueError('id must be either string or dict')
