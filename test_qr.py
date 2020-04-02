from qr_householder import qr_factorization1, qr_factorization2, qr_factorization3
import numpy as np
#from utils import norm
from numpy.linalg import norm
from data_manager import read_data
import time
import matplotlib.pyplot as plt

functions = [np.linalg.qr, qr_factorization1, qr_factorization2, qr_factorization3]

A, b = read_data('data/ML-CUP19-TR.csv')
m, n = A.shape


def conditioning_angle(a_, b_, x_):
    '''
    if this value is little, we know that the angle between b and Ax is little and so b is close to the ImA, and
    the problem is well conditioned
    '''
    return np.arccos(np.divide(norm(np.matmul(a_, x_)), norm(b_)))


for i, qr_factorization in enumerate(functions):
    print("**********************************************")
    print(qr_factorization.__name__)
    start = time.monotonic_ns()
    Q, R = qr_factorization(A)
    done = time.monotonic_ns()
    elapsed = done - start
    # Calcolo soluzione
    R1 = R[:n, :n]
    Q1 = Q[:, :n]
    Q1T = np.transpose(Q1)
    x = np.matmul(np.linalg.inv(R1), np.matmul(Q1T, b))
    # R = np.around(R, decimals=6)
    print("QR Factorization n° {} ended".format(i+1))
    print("ns spent: ", elapsed)
    print("||A - QR|| =", norm(A - np.matmul(Q1, R1)))
    print("||A - QR||/||A||", np.divide(norm(A - np.matmul(Q1, R1)), norm(A)))
    print("||Ax - b|| =", norm(np.matmul(A, x) - b))
    print("||Ax - b||/||b|| =", np.divide(norm(np.matmul(A, x) - b), norm(b)))
    print("Conditioning angle: ", conditioning_angle(A, b, x))

# Check if computational cost scale with m
print("**********************************************************")
print("Factorizing for various m...")
times = []
sizes = range(n, m, 100)
for k in sizes:
    print(k/m)
    A_ = A[:k, :]
    start = time.monotonic_ns()
    Q, R = qr_factorization(A_)
    done = time.monotonic_ns()
    elapsed = done - start
    times.append(elapsed)

# Creating plot
print("Creating plot...")
plt.plot(sizes, times)
plt.ylabel("Time for QR factorization")
plt.xlabel("Largest dimension of A")
plt.show()

exit()

# Now with m>>n
print("**********************************************************")
print("m>>n: Factorizing for various m...")
times = []
n = 10
m = 10000
sizes = range(n, m, 1000)
for k in sizes:
    print(k/m)
    A_ = np.random.rand(k, n)
    start = time.monotonic_ns()
    Q, R = qr_factorization3(A_)
    done = time.monotonic_ns()
    elapsed = done - start
    times.append(elapsed)

# Creating plot
print("Creating plot...")
plt.plot(sizes, times)
plt.ylabel("Time for QR factorization")
plt.xlabel("Largest dimension of A")
plt.show()
