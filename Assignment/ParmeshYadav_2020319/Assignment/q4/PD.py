import numpy as np
from LPSolution import Solution


def get_dual(nf):
    '''
    function to get dual constraints and objective function from an adjacency matrix
    '''

    # assumes that first row is source and last is sink like in the question
    # edges will be numbered as if they are being read row-by-row left to right
    # vertices will be numbered by row

    num_edges = np.count_nonzero(nf)
    num_vertices = nf.shape[0] - 2     # non terminal vertices
    numslacks = num_edges
    slack_counter = 0
    edge_counter = 0
    dual_constraints = np.zeros(
        (num_edges, num_edges + num_vertices + numslacks + 1))
    objective = np.zeros(2 * num_edges + num_vertices)

    for i in range(num_vertices + 2):
        for j in range(num_vertices + 2):
            if nf[i, j] != 0:

                objective[edge_counter] = nf[i, j]

                if i == 0:
                    dual_constraints[edge_counter, edge_counter] = 1
                    dual_constraints[edge_counter, num_edges + j - 1] = 1
                    dual_constraints[edge_counter, num_edges +
                                     num_vertices + slack_counter] = -1
                    dual_constraints[edge_counter, -1] = 1
                    edge_counter += 1
                    slack_counter += 1

                elif j == num_vertices + 1:
                    dual_constraints[edge_counter, edge_counter] = 1
                    dual_constraints[edge_counter, num_edges + i - 1] = -1
                    dual_constraints[edge_counter, num_edges +
                                     num_vertices + slack_counter] = -1
                    dual_constraints[edge_counter, -1] = 0
                    edge_counter += 1
                    slack_counter += 1

                else:
                    dual_constraints[edge_counter, edge_counter] = 1
                    dual_constraints[edge_counter, num_edges + i - 1] = -1
                    dual_constraints[edge_counter, num_edges + j - 1] = 1
                    dual_constraints[edge_counter, num_edges +
                                     num_vertices + slack_counter] = -1
                    edge_counter += 1
                    slack_counter += 1

    return np.vstack((dual_constraints, np.block([
        [np.eye(num_edges), np.zeros(
            (num_edges, num_vertices + numslacks + 1))],
        [np.zeros((numslacks, num_edges + num_vertices)),
         np.eye(numslacks), np.ones(num_edges).reshape(1, num_edges).T]
    ]))), objective


def get_primal(nf):
    '''
    function to get primal constraints and objective function from an adjacency matrix
    '''

    numedges = np.count_nonzero(nf)  # number of edges
    numvertices = nf.shape[0] - 2  # number of non terminal vertices
    numslacks = numedges  # number of slacks
    slack_counter = 0
    edge_counter = 0

    # numedges gives the flow capacity constraints
    # numvertices gives the flow conservation constraints
    # rows = numedges + numvertices + 2 = total number of constraints

    # columns = numedges + numslacks + 1 = total number of variables + 1
    # +1 for the RHS of the constraints

    primal_constraints = np.zeros(
        (numedges + numvertices + 2, numedges + numslacks + 1))

    obj = np.zeros(numedges + numslacks)  # objective function

    for i in range(numvertices + 2):  # for each row
        for j in range(numvertices + 2):  # for each column
            if nf[i, j] != 0:  # if there is an edge
                if i == 0:  # if it is the source
                    obj[edge_counter] = -1  # objective function
                    # flow capacity constraint
                    primal_constraints[edge_counter, edge_counter] = 1
                    primal_constraints[edge_counter,
                                       numedges + slack_counter] = 1  # slack constraint
                    # RHS of flow capacity constraint
                    primal_constraints[edge_counter, -1] = nf[i, j]
                    # flow conservation constraint
                    primal_constraints[numedges + j, edge_counter] = 1
                    edge_counter += 1  # increment edge counter
                    slack_counter += 1  # increment slack counter
                elif j == numvertices + 1:  # if it is the sink
                    # flow capacity constraint
                    primal_constraints[edge_counter, edge_counter] = 1
                    primal_constraints[edge_counter,
                                       numedges + slack_counter] = 1  # slack constraint
                    # RHS of flow capacity constraint
                    primal_constraints[edge_counter, -1] = nf[i, j]
                    # flow conservation constraint
                    primal_constraints[numedges + i, edge_counter] = -1
                    edge_counter += 1  # increment edge counter
                    slack_counter += 1  # increment slack counter
                else:  # if it is an edge between two vertices
                    # flow capacity constraint
                    primal_constraints[edge_counter, edge_counter] = 1
                    primal_constraints[edge_counter,
                                       numedges + slack_counter] = 1  # slack constraint
                    # RHS of flow capacity constraint
                    primal_constraints[edge_counter, -1] = nf[i, j]
                    # flow conservation constraint
                    primal_constraints[numedges + i, edge_counter] = -1
                    # flow conservation constraint
                    primal_constraints[numedges + j, edge_counter] = 1
                    edge_counter += 1  # increment edge counter
                    slack_counter += 1  # increment slack counter

    return np.vstack((np.vstack((primal_constraints[:numedges], primal_constraints[
        numedges + 1:numedges + numvertices + 1])), np.hstack(
        (np.eye(2 * numedges), np.zeros(2 * numedges).reshape(1, 2 * numedges).T)))), obj

# resource - https://github.com/justachetan/linear-optimisation/blob/5b9a76a8700a07c7dc3912a612b3ef13ecfe0d20/assn4/pdbarrier.py#L248


class PrimalDual(object):

    def __init__(self, num_eq_constraints, num_vars, c, constraints=None, tol=10**-20, A=None, b=None):
        self.num_eq_constraints = num_eq_constraints
        self.num_vars = num_vars
        self.A = A
        self.b = b
        self.tol = tol
        self.constraints = constraints
        if constraints is not None:
            self.A = constraints[:self.num_eq_constraints, :-1]
            self.b = constraints[:self.num_eq_constraints, -1]
        self.c = c
        if A is not None:
            self.num_vars = A.shape[1]
        self.x = None
        self.s = None
        self.l = None
        self.obj = 0

    def fetch_constraints(self, filename):
        constraints = np.loadtxt(filename)
        self.A = constraints[:self.num_eq_constraints, :-1]
        self.b = constraints[:self.num_eq_constraints, -1]

    def pdbarrier(self):

        A = self.A.copy()
        b = self.b.copy()
        c = self.c.copy()

        # Initialize problem data

        np.random.seed(42)  # set seed

        n = A.shape[1]  # number of variables
        x = np.random.random(A.shape[1])  # initial x
        l = np.random.random(A.shape[0])  # initial lamda
        s = np.random.random(A.shape[1])  # initial
        e = np.ones(x.shape[0])  # vector of ones

        # Set barrier method parameters
        mu = np.dot(x, s) / n
        sigma = 1 - (1 / np.sqrt(n))
        eta = 0.9999

        while mu > self.tol:  # while mu is greater than the tolerance
            X, S = np.diag(x), np.diag(s)

            I = np.eye(x.shape[0])  # identity matrix
            bmatrix = np.block([  # block matrix
                [A, np.zeros((A.shape[0], A.shape[0])),
                 np.zeros((A.shape[0], x.shape[0]))],
                [np.zeros((A.shape[1], A.shape[1])), A.T, I],
                [S, np.zeros((S.shape[0], A.shape[0])), X]
            ])
            rhs = -1 * np.hstack((  # right hand side
                np.dot(A, x) - b,
                np.dot(A.T, l) + s - c,
                np.dot(np.dot(X, S), e) - (sigma * mu * e)
            ))
            delta = np.linalg.solve(bmatrix, rhs)  # delta

            delx, dell, dels = delta[:x.shape[0]
                                     ], delta[x.shape[0]:-s.shape[0]], delta[-s.shape[0]:]

            alphax = min(1, eta * np.min(-x[delx < 0] / delx[delx < 0]))
            alphas = min(1, eta * np.min(-s[dels < 0] / dels[dels < 0]))

            x, l, s = x + alphax * delx, l + alphas * dell, s + alphas * dels
            mu = np.dot(x, s) / n

        xc = x.copy()
        sc = s.copy()
        lc = l.copy()

        self.x = xc
        self.s = sc
        self.l = lc

        self.obj = np.dot(c, x)  # objective value

        var_vals = {i: self.x[i] for i in range(self.num_vars)}
        return Solution(self.num_vars, var_vals, self.obj)
