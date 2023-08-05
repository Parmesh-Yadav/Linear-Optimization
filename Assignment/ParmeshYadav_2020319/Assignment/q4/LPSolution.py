import pandas as pd


class Solution(object):

    def __init__(self, num_vars=0, var_vals=list(), obj=0):

        self.num_vars = num_vars
        self.obj = obj
        self.var_vals = var_vals

    def printSol(self, type):

        # create a dictionary with variable names and values
        var_dict = {"x_" + str(i+1): [self.var_vals[i]]
                    for i in range(self.num_vars)}

        # create a DataFrame from the dictionary
        df = pd.DataFrame.from_dict(var_dict)

        # write the DataFrame to a csv file
        name = "solution_" + type + ".csv"
        df.to_csv(name, index=False)
