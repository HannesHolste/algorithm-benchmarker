import os
from subprocess import call

from skbio import DistanceMatrix

from littlebigo import Dataset
from littlebigo import Pipeline

from mdsa import subsample


def test_pipeline():
    def load_emp_dataset():
        data = Dataset('test-dataset',
                       './tests/test-dataset.txt')

    p = Pipeline('test-subsample')
    p.add(load_emp_dataset, 'Load test dataset')

    p.execute()


def test_emp_subsample_pipeline():
    OUT_PATH = './outputs/test-dataset-subsampled.txt'
    SUBSAMPLE_DIM = 10

    # Delete output file if exists to 'reset' test
    if os.path.exists(OUT_PATH):
        os.remove(OUT_PATH)

    def load_emp_dataset():
        data = Dataset('test-dataset',
                       './tests/test-dataset.txt')
        return data

    def subsamp(dataset):
        input_matrix = DistanceMatrix.read(dataset.filepath, format='lsmat')
        subsampled_matrix = subsample.subsample(input_matrix, SUBSAMPLE_DIM)
        return subsampled_matrix

    def save(subsampled_matrix):
        subsampled_matrix.write(OUT_PATH)

        # Track metadata (output file location)
        out_data = Dataset({
            'name': 'emp',
            'subsampled': True,
            'dimension': SUBSAMPLE_DIM
        }, OUT_PATH)

    p = Pipeline('test-subsample')
    # load EMP dataset
    p.add(load_emp_dataset, 'Load test dataset')

    # send to subsampler
    p.add(subsamp, 'Subsample dataset')

    p.add(save, 'Save subsampled matrix to disk')

    p.execute()

    assert os.path.exists(OUT_PATH)
