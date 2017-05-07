import littlebigo

datasets = {}


def add_dataset(dataset):
    if not isinstance(dataset, littlebigo.Dataset):
        raise ValueError('Dataset must be subclass of Dataset')

    datasets[hash(dataset)] = dataset
    print ([(k, v.id) for (k, v) in datasets.items()])


def get_dataset(dataset_id):
    return datasets[littlebigo.Dataset.hash_id(dataset_id)]