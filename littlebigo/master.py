import littlebigo

datasets = {}


def add_dataset(dataset):
    if not isinstance(dataset, littlebigo.Dataset):
        raise ValueError('Dataset must be subclass of Dataset')

    datasets[dataset.id] = dataset


def get_dataset(dataset_id):
    return datasets[dataset_id]