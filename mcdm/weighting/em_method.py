# Copyright (c) 2020-2021 Dimitrios-Georgios Akestoridis
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

u"""
Python implementation of the EM weighting method. For more information, see
the following publications:

* C.-L. Hwang and K. Yoon, *Multiple Attribute Decision Making*, ser. Lecture
  Notes in Economics and Mathematical Systems. Springer-Verlag Berlin
  Heidelberg, 1981, vol. 186, isbn: 9783540105589.

* H. Deng, C.-H. Yeh, and R. J. Willis, “Inter-company comparison using
  modified TOPSIS with objective weights,” *Comput. Oper. Res.*, vol. 27, no.
  10, pp. 963–973, 2000, doi: `10.1016/S0305-0548(99)00069-6
  <https://doi.org/10.1016/S0305-0548(99)00069-6>`_.

"""

import numpy as np


def em(z_matrix):
    """
    Return the weight vector of the provided decision matrix using the Entropy
    Measure method.
    """
    # Make sure that the provided decision matrix is a float64 NumPy array
    z_matrix = np.array(z_matrix, dtype=np.float64)

    # Make sure that the provided decision matrix is normalized
    if (np.sum(np.less(z_matrix, 0.0)) > 0
            or np.sum(np.greater(z_matrix, 1.0)) > 0):
        raise ValueError("The decision matrix must be normalized "
                         "in order to apply the EM weighting method")

    # Make sure that the columns of the decision matrix sum to 1
    if not np.all(np.isclose(np.sum(z_matrix, axis=0),
                             np.ones(z_matrix.shape[1]))):
        raise ValueError("The columns of the decision matrix must sum to 1 "
                         "in order to apply the EM weighting method")

    # Compute the normalization constant
    k_constant = 1.0 / np.log(z_matrix.shape[0])

    # Compute the entropy of each criterion
    e_vector = np.zeros(z_matrix.shape[1], dtype=np.float64)
    for j in range(z_matrix.shape[1]):
        tmp_sum = 0.0
        for i in range(z_matrix.shape[0]):
            if z_matrix[i, j] > 0.0:
                tmp_sum += z_matrix[i, j] * np.log(z_matrix[i, j])
        e_vector[j] = -k_constant * tmp_sum

    # The importance of each criterion corresponds to
    # its normalized degree of divergence
    return (1.0 - e_vector) / np.sum(1.0 - e_vector)