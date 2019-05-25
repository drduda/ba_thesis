import numpy as np
from unittest import TestCase

# Values from Safaee-Rad et al. 3-D LOCATION ESTIMATION OF CIRCULAR FEATURES 
# p. 632f
t0 = np.array([[1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 1, 1],
               [0, 0, 0, 1]])

t1 = np.array([[-0.413957, 0.836516, -0.358998, 0],
                        [0.875989, 0.258819, -0.407009, 0],
                        [-0.247554, -0.482963, -0.839919, 0],
                        [0, 0, 0, 1])

t2 = np.array([[1, 0, 0, 0.247554],
               [0, 1, 0, 0.482964],
               [0, 0, 1, 0.839915],
               [0, 0, 0, 1]])

t3 = np.array([[0, -0.906890, 0.421367, 0],
               [1, 0, 0, 0],
               [0, 0.4213567, 0.906, 0],
               [0, 0, 0, 1]])

#Assert if total transformation is still calculated
np.testing.assert_almost_equal(t1.dot(t3), t0.dot(t1.dot(t2.dot(t3))), decimal=2)

la1, la2, la3 = 274.281, 225, -3.281

t3_alternative = np.array([[0, 0.906890, -0.421367, 0],
                          [1, 0, 0, 0],
                          [0, 0.4213567, 0.906, 0],
                          [0, 0, 0, 1]])

val, vec = np.linalg.eig(t1)
