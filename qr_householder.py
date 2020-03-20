import numpy as np
from utils import norm, row_to_column, column_to_row


def householder_vector(x):
    '''
    This function creates a householder_reflector that can be used to form H as I - 2*v*v' to zero first entry
    :param x: a column vector
    :return: a column vector useful to form H
    '''
    norm_x = -np.sign(x[0]) * norm(x)
    vec = np.copy(x)
    vec[0] = vec[0] - norm_x
    vec = np.true_divide(vec, norm(vec))
    return vec, norm_x


def qr_factorization1(x_):
    '''
    First version of the algorithm, the slowest and simplest one
    It returns the QR factorization of the matrix x_, inside the function it uses a copy of the matrix
    :param x_: the matrix we want to factorize
    :return: orthogonal matrix Q and upper triangular R
    '''
    x_ = np.copy(x_)
    [m, n] = x_.shape
    Q_ = np.identity(m)
    for j in range(n):
        col = row_to_column(x_[j:, j])
        v_, _ = householder_vector(col) # v_ is a column vector (3, 1)
        v_size = v_.shape[0]
        v_T = column_to_row(v_) # v_T is a row vector (1, 3)
        H = np.identity(v_size) - (2 * np.matmul(v_, v_T))  # colonna x riga
        x_[j:, j:] = np.matmul(H, x_[j:, j:])
        Q_[:, j:] = np.matmul(Q_[:, j:], H)
    R_ = x_
    return Q_, R_


def qr_factorization2(x_):
    '''
    Variant of the first algorithm, which uses the fast product Householder-vector.
    It returns the QR factorization of the matrix x_, inside the function it uses a copy of the matrix
    :param x_: the matrix we want to factorize
    :return: orthogonal matrix Q and upper triangular R
    '''
    x_ = np.copy(x_)
    [m, n] = x_.shape
    Q_ = np.identity(m)
    for j in range(min(m-1, n)):
        col = row_to_column(x_[j:, j])
        v_, s_ = householder_vector(col) # v_ is a column vector (3, 1)
        v_T = column_to_row(v_) # v_T is a row vector (1, 3)
        x_[j, j] = s_
        x_[j+1:, j] = 0
        x_[j:, j+1:] = x_[j:, j+1:] - 2 * np.matmul(v_, np.matmul(v_T, x_[j:, j+1:]))
        Q_[:, j:] = Q_[:, j:] - np.matmul(Q_[:, j:], 2*np.matmul(v_, v_T))
    R_ = x_
    return Q_, R_


def qr_factorization3(x_):
    '''
    Last variant of the algorithm, which does not form the matrix Q, but stores the v's
    It returns the QR factorization of the matrix x_, inside the function it uses a copy of the matrix
    :param x_: the matrix we want to factorize
    :return: orthogonal matrix Q and upper triangular R
    '''
    x_ = np.copy(x_)
    [m, n] = x_.shape
    Q_ = np.identity(m)
    V =[]
    for j in range(min(m-1, n)):
        col = row_to_column(x_[j:, j])
        v_, s_ = householder_vector(col) # v_ is a column vector (3, 1)
        v_T = column_to_row(v_) # v_T is a row vector (1, 3)
        x_[j, j] = s_
        x_[j+1:, j] = 0
        x_[j:, j+1:] = x_[j:, j+1:] - 2 * np.matmul(v_, np.matmul(v_T, x_[j:, j+1:]))
        V.append(v_)

    for j, v_ in enumerate(V):
        Q_[:, j:] = Q_[:, j:] - np.matmul(Q_[:, j:], 2*np.matmul(v_, column_to_row(v_)))
    R_ = x_
    return Q_, R_
