import numpy as np
from q1 import Simplex
# formulation of the problem as a linear program

'''

Network:

[
    [0 1 0 0]
    [1 0 1 1]
    [0 1 0 1]
    [0 1 1 0]
]

there are a total of 4 edges in the network: e1, e2, e3, e4

let xi = 1 if edge ei is used, 0 otherwise

maximize z = x1 + x2 + x3 + x4 + 0s1 + 0s2 + 0s3 + 0s4 

subject to:

x1 + s1 = 1
x1 + x2 + x4 + s2 = 1
x2 + x3 + s3 = 1
x3 + x4 + s4 = 1

x1, x2, x3, x4, s1, s2, s3, s4 >= 0

'''

c = [-1, -1, -1, -1, 0, 0, 0, 0]

A = [[1, 0, 0, 0,
      1, 0, 0, 0],

     [1, 1, 0, 1,
      0, 1, 0, 0],

     [0, 1, 1, 0,
      0, 0, 1, 0],

     [0, 0, 1, 1,
      0, 0, 0, 1]]

b = [1, 1, 1, 1]
simplex = Simplex()

solution, objective = simplex.revised_simplex(4, 4, True, c, A, b)

if solution is None:
    print("The problem is unbounded.")
else:
    print("The optimal solution is: {}".format(solution))
    print("The optimal objective value is: {}".format(objective * -1))
