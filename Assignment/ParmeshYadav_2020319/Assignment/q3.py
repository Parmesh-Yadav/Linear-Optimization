

'''

Network: 

[
    [ 1 1 0 0 ]
    [ 0 1 1 0 ]
    [ 0 0 1 1 ]
    [ 0 1 0 1 ]
]

minimize z = x1 + x2 + x3 + x4

subject to:

x1 + s1 = 1 
x1 + x2 + x3 + s2 = 1
x2 + x3 + s3 = 1
x3 + x4 + s4 = 1

x1, x2, x3, x4 >= 0
x1, x2, x3, x4 are integers


'''

from q1 import Simplex

c = [1, 1, 1, 1,
     0, 0, 0, 0]

A = [

    [1, 0, 0, 0,
     1, 0, 0, 0],

    [1, 1, 1, 0,
     0, 1, 0, 0],

    [0, 1, 1, 0,
     0, 0, 1, 0],

    [0, 0, 1, 1,
     0, 0, 0, 1],


]

b = [1, 1, 1, 1]

simplex = Simplex()
solution, objective = simplex.revised_simplex(8, 4, False, c, A, b)

if solution is None:
    print("The problem is unbounded.")
else:
    print("The optimal solution is: {}".format(solution))
    print("The optimal objective value is: {}".format(objective*-1))
