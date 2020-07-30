import numpy
import scipy.sparse, scipy.sparse.linalg
import timeit

# Dominic Hatch 2020
# https://github.com/dhatch207

"""
trying to optimize the power method for finding eigenvector of a matrix.

Given: A sparse matrix A with eigenvalues a_1, ..., a_n, and a matrix B with values 'close' to that of A.

By 'close' we mean (WHAT?)

"""

"""
functions being tested
"""
    
# get eigenvector of a matrix with power method 
def control_power_method(matrix):
    result = scipy.sparse.linalg.eigsh(matrix, k=1, v0=None)
    return result[1]

# get eigenvector of a matrix with power method with seed vector generated from base matrix
def experiment_power_method(matrix, eigenvectors):
    return

# generate orthonormal basis from eigenvectors

# convert matrix to basis

""" 
functions for testing and comparison
"""

# generate a random sparse matrix
def generate_matrix(size, density):
    return scipy.sparse.random(size, size, density=density).A

# get all eigenvectors of a matrix
def get_eigenvectors(matrix):
    eigenvalues, eigenvectors = numpy.linalg.eig(matrix)
    return eigenvectors

# generate a matrix with values 'close' to another
def generate_close_matrix(matrix, frac_changed, spread):
    # find where the original matrix is nonzero
    nonzeros = numpy.nonzero(matrix)

    # pick a sample to modify, and how much    
    sample_indexes = numpy.random.choice(numpy.arange(nonzeros[0].shape[0]), int(frac_changed * nonzeros[0].shape[0]), replace=False)
    deltas = numpy.random.uniform(-spread, spread, sample_indexes.shape[0])
    
    # modify and return new matrix
    result = numpy.copy(matrix)
    for sample, index in enumerate(sample_indexes):
        result[nonzeros[0][sample]][nonzeros[1][sample]] += result[nonzeros[0][sample]][nonzeros[1][sample]] * deltas[sample]

    return result 

# build a testing set with desired parameters
def generate_testing_set(count, size, density, frac_changed, spread):
    original_matrices, modified_matrices, eigenvectors = [], [], []
    for i in range(count):
        original = generate_matrix(size, density)
        original_matrices.append(original)
        modified_matrices.append(generate_close_matrix(original, frac_changed, spread))
        eigenvectors.append(get_eigenvectors(original))

    return original_matrices, modified_matrices, eigenvectors

def run_experiment():
    original_matrices, modified_matrices, eigenvectors = generate_testing_set(1000, 100, .1, .5, .2)

    # control
    control_start = timeit.default_timer()
    for matrix in modified_matrices:
        control_power_method(matrix)
    control_end = timeit.default_timer()
    print('control time:', control_end - control_start)

    # experiment
    experiment_start = timeit.default_timer()
    for i, matrix in enumerate(modified_matrices):
        experiment_power_method(matrix, eigenvectors[i])
    experiment_end = timeit.default_timer()
    print('experiment time:', experiment_end - experiment_start)

run_experiment()