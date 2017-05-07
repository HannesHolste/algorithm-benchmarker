from littlebigo import Dataset
from littlebigo.master import get_dataset


def test_register_dataset_str_id():
    data = Dataset('test-dataset', './tests/test-dataset.txt')

    assert data.id == 'test-dataset'
    assert get_dataset('test-dataset') == data


def test_register_dataset_dict_id():
    id_ = {
        'name': 'emp-test',
        'subsampled': False,
        'dimension': 512
    }
    data = Dataset(id_, './tests/test-dataset.txt')

    assert data.id == id_
    assert get_dataset(id_) == data


def test_eq():
    d1 = Dataset('d1', './tests/test-dataset.txt')
    d2 = Dataset('d2', './tests/test-dataset.txt')

    assert d1 != d2

    d3 = Dataset('d1', './tests/test-dataset.txt')

    assert d1 == d3

    d1 = Dataset({'name': 'd1'}, './tests/test-dataset.txt')
    d2 = Dataset({'name': 'd2'}, './tests/test-dataset.txt')

    assert d1 != d2

    d3 = Dataset({'name': 'd1'}, './tests/test-dataset.txt')

    assert d1 == d3
