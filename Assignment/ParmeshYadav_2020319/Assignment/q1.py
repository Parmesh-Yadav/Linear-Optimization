import numpy as np


class Simplex:

    def revised_simplex(self, n, m, maximize, c, A, b):
        # Create table
        table = np.zeros((len(b)+1, len(c)+len(b)+1))
        table[0, :len(c)] = c  # fill objective coefficients in first row
        # fill constraint coefficients in remaining rows
        table[1:, :len(c)] = A
        # fill identity matrix in slack variables
        table[1:, len(c):-1] = np.eye(len(b))
        table[1:, -1] = b  # fill right-hand side vector in last column

        # Perform Revised Simplex Method
        while True:
            # Check if optimal
            if np.all(table[0, :-1] >= 0):  # if all objective coefficients are non-negative
                break

            # Choose entering variable
            # choose the column with the most negative coefficient
            entering_col = np.argmin(table[0, :-1])

            # Choose leaving variable
            # calculate ratios of right-hand side values to entering column coefficients
            ratios = table[1:, -1] / table[1:, entering_col]
            # set ratios of negative or zero values to infinity to avoid division by zero
            ratios[~(ratios > 0)] = np.inf
            if np.all(ratios == np.inf):  # if all ratios are infinite, the problem is unbounded
                return None, np.inf

            # choose the row with the smallest ratio, adding 1 to account for the first row of the table
            leaving_row = np.argmin(ratios) + 1

            # Update table
            # choose the pivot element
            pivot = table[leaving_row, entering_col]
            # divide the leaving row by the pivot element to make it equal to 1
            table[leaving_row, :] /= pivot
            for i in range(table.shape[0]):  # iterate over all rows
                if i != leaving_row:  # skip the leaving row
                    # perform row operations to make all other entries in the entering column equal to zero
                    table[i, :] -= table[i, entering_col] * \
                        table[leaving_row, :]

        # Extract solution and objective value
        # the solution is the right-hand side values of the basic variables
        solution = table[1:, -1]
        # the objective value is the value in the bottom-right corner of the table
        objective = table[0, -1]

        return solution, -objective


if __name__ == '__main__':
    # Get input from user
    n = int(input("Enter the number of variables: "))
    m = int(input("Enter the number of constraints: "))
    if input("Do you want to maximize the objective function? (y/n): ").lower() == 'n':
        maximize = False
    else:
        maximize = True
    c = np.array(list(map(float, input(
        "Enter the coefficients of the objective function separated by spaces: ").split())))
    A = np.array([list(map(float, input(
        "Enter the coefficients of constraint {} separated by spaces: ".format(i+1)).split())) for i in range(m)])
    b = np.array(list(map(float, input(
        "Enter the right-hand side values of the constraints separated by spaces: ").split())))

    # Call the revised_simplex function with the input values
    simplex = Simplex()
    solution, objective = simplex.revised_simplex(n, m, maximize, c, A, b)

    # Print the solution and objective value
    if solution is None:
        print("The problem is unbounded.")
    else:
        if maximize:
            objective = -objective
        print("The optimal solution is: {}".format(solution))
        print("The optimal objective value is: {}".format(objective))
