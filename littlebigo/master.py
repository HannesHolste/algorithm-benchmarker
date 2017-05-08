import littlebigo

datasets = {}


def add_dataset(dataset):
    if not isinstance(dataset, littlebigo.Dataset):
        raise ValueError('Dataset must be subclass of Dataset')

    datasets[hash(dataset)] = dataset


def get_dataset(dataset_id):
    return datasets[littlebigo.Dataset.hash_id(dataset_id)]


def clear_datasets():
    datasets.clear()


def get_datasets():
    return datasets


def find_datasets_any(search_params):
    """
    Find datasets that match at least one of the given search parameters.

    :param search_params: Either a string denoting the id of a dataset being
        searched for or a dict of search parameters and their values.
        Search parameters and values are case-sensitive.
    :return: None if none found, else an unsorted list of instances of Dataset
        where each dataset had a key-value pair in its id dict that
        corresponded with at least one of the key-value pairs
        in the given search_params dict.
    """
    if (not isinstance(search_params, str) and
            not isinstance(search_params, dict)):
        raise ValueError('Expected search_params to be type dict or str.')

    results = set()

    if isinstance(search_params, str):
        for d in datasets.values():
            if type(d.id) == str and d.id == search_params:
                results.add(d)
    elif isinstance(search_params, dict):
        for d in datasets.values():
            if type(d.id) == dict:
                for param, val in search_params.items():
                    if d.id[param] == val:
                        results.add(d)
                        break

    return list(results)


def find_first_dataset_any(search_params):
    """
    Find first dataset that matches at least one of the given search
    parameters.

    :param search_params: Either a string denoting the id of a dataset being
        searched for or a dict of search parameters and their values.
        Search parameters and values are case-sensitive.
    :return: None if none found, else an instance of Dataset.
    """
    if (not isinstance(search_params, str) and
            not isinstance(search_params, dict)):
        raise ValueError('Expected search_params to be type dict or str.')

    if isinstance(search_params, str):
        for d in datasets.values():
            if type(d.id) == str and d.id == search_params:
                return d
    elif isinstance(search_params, dict):
        for d in datasets.values():
            if type(d.id) == dict:
                for param, val in search_params.items():
                    if d.id[param] == val:
                        return d

    return None
