import pytest

from littlebigo import Dataset
from littlebigo.master import get_dataset, find_first_dataset_any, \
    find_datasets_any, clear_datasets


def test_register_dataset_str_id():
    clear_datasets()
    data = Dataset('test-dataset', './tests/test-dataset.txt')

    assert data.id == 'test-dataset'
    assert get_dataset('test-dataset') == data


def test_register_dataset_dict_id():
    clear_datasets()
    id_ = {
        'name': 'emp-test',
        'subsampled': False,
        'dimension': 512
    }
    data = Dataset(id_, './tests/test-dataset.txt')

    assert data.id == id_
    assert get_dataset(id_) == data


def test_ne():
    clear_datasets()
    d1 = Dataset('d1', './tests/test-dataset.txt')
    d2 = Dataset('d2', './tests/test-dataset.txt')

    assert d1 != d2

    d1 = Dataset({'name': 'd1'}, './tests/test-dataset.txt')
    d2 = Dataset({'name': 'd2'}, './tests/test-dataset.txt')

    assert d1 != d2


def test_find_first_any():
    clear_datasets()
    test1 = Dataset('test1', './tests/test-dataset.txt')

    d = find_first_dataset_any('test1')
    d_fail = find_first_dataset_any('unknown')

    assert d.id == test1.id
    assert d_fail is None

    test2 = Dataset({'name': 'dada'}, './tests/test-dataset.txt')

    d = find_first_dataset_any({'name': 'dada'})
    d_fail = find_first_dataset_any({'name': 'dadalife'})

    assert d.id == test2.id
    assert d_fail is None


def test_find_any():
    clear_datasets()
    # test where id is simple string and there are multiple matches
    # but one duplicate is returned. This illustrates expected behavior.
    test1 = Dataset('testa', './tests/test-dataset.txt')

    with pytest.raises(ValueError):
        Dataset('testa', './tests/test-dataset.txt')

    results = find_datasets_any('testa')
    assert len(results) == 1
    assert results[0].id == test1.id

    # test where id is dict and there are multiple matches
    test2 = Dataset({'name': 'dupe1'}, './tests/test-dataset.txt')
    test3 = Dataset({'name': 'dupe1', 'otherkey': 'blah'},
                    './tests/test-dataset.txt')

    results = find_datasets_any({'name': 'dupe1'})
    results_fail = find_datasets_any({'name': 'dadalife'})

    assert len(results) == 2

    d1 = results[0]
    d2 = results[1]

    assert d1.id == test2.id
    assert d2.id == test3.id
    assert len(results_fail) == 0

    # test where id is dict and there are multiple matches, but only
    # one duplicate is returned. This illustrates expected behavior.
    Dataset({'name': 'dupe2'}, './tests/test-dataset.txt')

    with pytest.raises(ValueError):
        Dataset({'name': 'dupe2'}, './tests/test-dataset-small.txt')
