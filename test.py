import numpy as np

A = np.zeros((3, 2, 4, 6))

B = np.ones((3, 6,6))

print(A.dot(B).shape)