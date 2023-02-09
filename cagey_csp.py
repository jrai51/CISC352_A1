# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
import itertools

def _cor_to_idx(x, y, N):
    """ Takes x,y coordinates and size N of grid and returns the index in the variable list"""
    return N*(x-1) + y - 1 

def binary_ne_grid(cagey_grid):
    binary_csp = CSP("BinaryCSP") #construct csp 
    vars = []
    N = cagey_grid[0]

    #Create all variables (cells in the grid)
    for i in range (1, N+1):
        for j in range(1, N+1):
            dom = range(1, N+1)
            var_name = f"Cell({i},{j})"
            var = Variable(var_name, dom)
            vars.append(var)

   #cages = cagey_csp_model[1]

    valid_bin_tuples = [(i, j) for i in range(1, N+1) 
                        for j in range(1, N+1) 
                        if i != j ]
    
    #No two cells in a row can be the same
    #rows = [vars[x:x+N] for x in range(0, len(vars), N)]


    for i in range(1, N+1):
        for j in range(1, N+1):

            # Add column constraints
            for j2 in range(j+1, N+1):
                con = Constraint(
                    f"NEQ(({i},{j}),({i},{j2}))",
                    [
                        vars[_cor_to_idx(i,j,N)],
                        vars[_cor_to_idx(i,j2,N)]
                    ]
                )
                con.add_satisfying_tuples(valid_bin_tuples)
                binary_csp.add_constraint(con)
            
            # Add row constraints
            for i2 in range(i+1, N+1):
                con = Constraint(
                    f"NEQ(({i},{j}),({i2},{j}))",
                    [
                        vars[_cor_to_idx(i,j,N)],
                        vars[_cor_to_idx(i2,j,N)]
                    ]
                )
                con.add_satisfying_tuples(valid_bin_tuples)
                binary_csp.add_constraint(con)


    return (binary_csp, vars)
            

    
    #No two cells in one row are the same
   

    #No two cells in one column are the same 
        

def nary_ad_grid(cagey_grid):
    n = cagey_grid[0]
    domain = [i + 1 for i in range(n)]
    var_array = [Variable("Cell({},{})".format(row, col), domain)
                 for row in domain for col in domain]
    grid_vars = [[var_array[(row - 1) * n + col - 1]
                  for col in domain] for row in domain]

    satisfying_tuples = list(itertools.permutations(domain, n))
    constraints = [
        Constraint("C(Row{})".format(i + 1), grid_row) for i, grid_row in enumerate(grid_vars)
    ] + [
        Constraint("C(Col{})".format(i + 1),
                   [grid_vars[j][i] for j in range(n)])
        for i in range(n)
    ]
    for constraint in constraints:
        constraint.add_satisfying_tuples(satisfying_tuples)

    csp = CSP("{}-Cagey-nary-ad".format(n), var_array)
    for constraint in constraints:
        csp.add_constraint(constraint)

    return csp, var_array

def cagey_csp_model(cagey_grid):
    ##IMPLEMENT
    pass

