import numpy as np
import scipy.sparse, scipy.sparse.linalg
import scqubits as scq
from tqdm import tqdm
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
    result = scipy.sparse.linalg.eigsh(matrix, k=10, v0=None)
    return result[1]

# get eigenvector of a matrix with power method with seed vector generated from base matrix
def experiment_power_method(matrix, eigenvectors):
    v0 = None
    v0 = sum(eigenvectors)

    #v0 = np.ones((eigenvectors)[0].shape)

    #num_e = eigenvectors.shape[0]
    #v0 = eigenvectors[np.random.choice(num_e)]
    #while np.all(v0 == np.zeros(eigenvectors[0].shape)):
    #    v0 = eigenvectors[np.random.choice(num_e)]
    #
    result = scipy.sparse.linalg.eigsh(matrix, k=10, v0=v0)
    return result[1]

""" 
functions for generating diagonal matrices
"""

def make_herm(matrix):
    return (matrix + matrix.transpose().conjugate())*0.5

def make_dia(size, offset):
    data_original = ((np.random.rand(size)-0.5)*2).tolist()
    data = np.array([data_original]).repeat((len(offset)), axis=0)
    offset = np.array(offset)
    return scipy.sparse.dia_matrix((data,offset), shape=(size,size))

def change_matrix(matrix, variance):
    size = matrix.shape[0]
    new = scipy.sparse.dia_matrix((((np.random.rand(size)-0.5)*variance), -20), shape=(size, size))
    return make_herm(np.add(matrix, new))

"""
functions for generating zero pi matrices
"""

def get_zero_pi_hamiltonian(flux):
    phi_grid = scq.Grid1d(-6*np.pi, 6*np.pi, 200)
    EJ_CONST = 1/3.95 
    zero_pi = scq.ZeroPi(
        grid = phi_grid,
        EJ   = EJ_CONST,
        EL   = 10.0**(-2),
        ECJ  = 1/(8.0*EJ_CONST),
        EC = None,
        ECS  = 10.0**(-3),
        ng   = 0.1,
        flux = flux,
        ncut = 30
    )
    ham = zero_pi.hamiltonian()
    return ham

"""
functions for building testing sets
"""

# get all eigenvectors of a matrix
def get_eigenvectors(matrix):
    eigenvalues, eigenvectors = scipy.sparse.linalg.eigsh(matrix, k=10)
    return eigenvectors

# build a testing set with desired parameters
def generate_testing_set(count, size, spread, matrix_type='diagonal'):
    print('generating testing set')
    original_matrices, modified_matrices, eigenvectors = [], [], []
    
    if matrix_type == 'diagonal':
        for i in tqdm(range(count)):
            original = make_herm(make_dia(size, [-20,-1,0]))
            original_matrices.append(original)
            modified = change_matrix(original, spread)
            modified_matrices.append(modified)
            eigenvectors.append(get_eigenvectors(original))
    
    if matrix_type == 'zero_pi':
        flux_list = np.linspace(0, 0.1, count + 1)
        for i in tqdm(range(count + 1)):
            original = get_zero_pi_hamiltonian(flux_list[i])
            original_matrices.append(original)

            if i != 0:
                modified = original_matrices[i - 1]#get_zero_pi_hamiltonian(flux_list[i + 1])
                modified_matrices.append(modified)
                eigenvectors.append(get_eigenvectors(original))

        original_matrices = original_matrices[1:] 

    return original_matrices, modified_matrices, eigenvectors

def store_testing_set(original_matrices, modified_matrices, eigenvectors):
    print('storing generated set')
    np.save('original_matrices.npy', original_matrices)
    np.save('modified_matrices.npy', modified_matrices)
    np.save('eigenvectors.npy', eigenvectors)
    return

def get_testing_set():
    print('retrieving testing set')
    original_matrices = np.load('original_matrices.npy', allow_pickle = True)
    modified_matrices = np.load('modified_matrices.npy', allow_pickle = True)
    eigenvectors = np.load('eigenvectors.npy', allow_pickle = True)
    return original_matrices, modified_matrices, eigenvectors

def run_experiment(new_set=True, store_set=False, count=100, size=10000, spread=.01, repititions=1, matrix_type='diagonal'):
    
    if new_set:
        original_matrices, modified_matrices, eigenvectors = generate_testing_set(count, size, spread, matrix_type)
        if store_set:
            store_testing_set(original_matrices, modified_matrices, eigenvectors)
    else:
        original_matrices, modified_matrices, eigenvectors = get_testing_set()

    # experiment
    print('running experiment')
    eigenvectors = np.real(eigenvectors)
    experiment_start = timeit.default_timer()
    for i in range(repititions):
        for i, matrix in enumerate(tqdm(modified_matrices)):
            experiment_power_method(matrix, eigenvectors[i].T)
    experiment_end = timeit.default_timer()
    print('experiment time:', experiment_end - experiment_start)

    # control
    print('running control')
    control_start = timeit.default_timer()
    for i in range(repititions):
        for matrix in tqdm(modified_matrices):
            control_power_method(matrix)
    control_end = timeit.default_timer()
    print('control time:', control_end - control_start)

    # printables
    #for i, matrix in enumerate(modified_matrices):
    #    print(original_matrices[i])
    #    print(np.linalg.eig(original_matrices[i])[0])
    #    print(eigenvectors[i])
    #    print(matrix)
    #    print(control_power_method(matrix))

run_experiment(new_set=True, store_set=True, count=100, matrix_type='zero_pi')