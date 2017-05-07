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
        return self.hash_id(self.id)

    @staticmethod
    def hash_id(id_):
        if isinstance(id_, str):
            return hash(id_)
        elif isinstance(id_, dict):
            return hash(frozenset(id_.items()))
        else:
            raise ValueError('id must be either string or dict')

    def __eq__(self, other):
        """
        Shallow equality check: only compares ids of datasets
        :param other: other Dataset object
        :return: whether the ids of the Dataset objects are equal
        """
        if type(other) is not type(self):
            return False

        return self.id == other.id

    def __ne__(self, other):
        return not(self.__eq__(other))

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)