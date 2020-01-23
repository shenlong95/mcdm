# Copyright (c) 2020 Dimitrios-Georgios Akestoridis
# This project is licensed under the terms of the MIT license.

import csv
import numpy as np


def load(filepath, delimiter=",", skiprows=0, labeled_rows=False):
    """Load a matrix, and potentially row labels, from a text file."""
    matrix = None
    row_labels = None
    if labeled_rows:
        # Separate the row labels from the matrix data
        row_labels = []
        matrix_data = []
        num_columns = None
        with open(filepath, "r") as fp:
            rows = csv.reader(fp, delimiter=delimiter)
            for i, row in enumerate(rows, start=1):
                # Skip the selected number of rows
                if i <= skiprows:
                    continue

                # Determine the expected number of columns
                if num_columns is None:
                    num_columns = len(row) - 1

                # Sanity checks
                if len(row) <= 1:
                    raise ValueError("The matrix should have at "
                                     "least 1 column with data")
                elif len(row) - 1 != num_columns:
                    raise ValueError("Wrong number of columns at "
                                     "line {}".format(i))

                # The row labels are expected to be
                # in the first column of the text file
                row_labels.append(row[0])
                matrix_data.append(row[1:])
        # Convert the matrix data into a float64 NumPy array
        matrix = np.array(matrix_data, dtype=np.float64)
    else:
        # Load the matrix from the text file as a float64 NumPy array
        matrix = np.loadtxt(filepath, dtype=np.float64, delimiter=delimiter,
                            skiprows=skiprows)

    return matrix, row_labels
