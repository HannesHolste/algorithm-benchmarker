import pytest
from littlebigo import Dataset
from littlebigo import Pipeline


def test_pipeline():
    def load_emp_dataset():
        data = Dataset('test-dataset',
                       './tests/test-dataset.txt')

    p = Pipeline('test-subsample')
    p.add(load_emp_dataset, 'Load test dataset')

    p.execute()
