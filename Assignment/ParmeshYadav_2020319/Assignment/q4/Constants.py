import numpy as np


class Constants:
    # Constants for the problem
    # static variables

    PRIMAL_VARIABLES = 39
    DUAL_VARIABLES = 29

    PRIMAL_EQUATIONS = 58
    DUAL_EQUATIONS = 68
    TOLERANCE = 10**-30

    network = np.array([
        np.array([0, 11, 15, 10, 0, 0, 0, 0, 0, 0, 0, 0]),
        np.array([0, 0, 0, 0, 0, 18, 4, 0, 0, 0, 0, 0]),
        np.array([0, 3, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0]),
        np.array([0, 0, 0, 0, 6, 0, 0, 3, 11, 0, 0, 0]),
        np.array([0, 0, 0, 4, 0, 0, 0, 17, 6, 0, 0, 0]),
        np.array([0, 0, 0, 0, 3, 0, 0, 0, 0, 13, 0, 0]),
        np.array([0, 12, 0, 0, 4, 0, 0, 0, 0, 0, 0, 21]),
        np.array([0, 0, 0, 0, 0, 0, 0, 0, 4, 9, 4, 3]),
        np.array([0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 5, 4]),
        np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 9]),
        np.array([0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 15]),
        np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    ])
