import numpy as np
import numpy.linalg as npla
from Constants import Constants
import pandas as pd
from LPSolution import Solution
from PD import PrimalDual
from PD import get_primal
from PD import get_dual


class Main:

    def run_max_flow(self):

        constraints, c = get_primal(Constants.network)
        pd = PrimalDual(Constants.PRIMAL_VARIABLES,
                        Constants.PRIMAL_EQUATIONS, c, constraints, Constants.TOLERANCE)
        sol = pd.pdbarrier()
        print("Max-Flow:", sol.obj * (-1))
        sol.printSol("primal")

    def run_min_cut(self):
        constraints, c = get_dual(Constants.network)
        pd = PrimalDual(Constants.DUAL_VARIABLES,
                        Constants.DUAL_EQUATIONS, c, constraints, Constants.TOLERANCE)
        sol = pd.pdbarrier()
        print("Min-cut", sol.obj)
        sol.printSol("dual")


if __name__ == '__main__':
    main = Main()
    main.run_max_flow()
    main.run_min_cut()
