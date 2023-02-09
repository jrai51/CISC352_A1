# =============================
# Student Names: Jagrit Rai, Mercy Doan, Yash Patel
# Group ID: 51
# Date: 2022 - 02 - 08
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc:
#

# Look for #IMPLEMENT tags in this file.
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

""" HELPER FUCTION"""


def _cor_to_idx(x, y, N):
    """ Takes x,y coordinates and size N of grid and returns the index in the variable list"""
    return N*(x-1) + y - 1


def binary_ne_grid(cagey_grid):
    binary_csp = CSP("BinaryCSP")  # construct csp
    vars = []  # Ordered list of variables
    N = cagey_grid[0]

    # Create all variables (cells in the grid)
    for i in range(1, N+1):
        for j in range(1, N+1):
            dom = range(1, N+1)
            var_name = f"Cell({i},{j})"
            var = Variable(var_name, dom)
            vars.append(var)

    for var in vars:  # add variables to the csp
        binary_csp.add_var(var)

    # valid tuples are all sets of two different numbers
    valid_bin_tuples = [(i, j) for i in range(1, N+1)
                        for j in range(1, N+1)
                        if i != j]

    # Get list of all rows
    rows = []
    for i in range(1, N+1):
        row = []
        for j in range(1, N+1):
            row.append((i, j))
        rows.append(row)

    # No two cells in a row can be the same
    for row in rows:
        row_pairs = [(a, b) for idx, a in enumerate(row)
                     for b in row[idx + 1:]]  # all pairs of tuples
        for pair in row_pairs:
            cell1, cell2 = pair
            x, y = cell1
            a, b = cell2
            con = Constraint(f"DIFF_CELL({x},{y})_CELL({a},{b})",
                             [vars[_cor_to_idx(x, y, N)], vars[_cor_to_idx(a, b, N)]])
            con.add_satisfying_tuples(valid_bin_tuples)
            binary_csp.add_constraint(con)

    # get list of all columns
    cols = []
    for i in range(1, N+1):
        col = []
        for j in range(1, N+1):
            col.append((j, i))
        cols.append(col)

    # No two cells in a column can be the same
    for col in cols:
        col_pairs = [(a, b) for idx, a in enumerate(col)
                     for b in col[idx + 1:]]  # all pairs of tuples
        for pair in col_pairs:
            cell1, cell2 = pair
            x, y = cell1
            a, b = cell2
            con = Constraint(f"DIFF_CELL({x},{y})_CELL({a},{b})",
                             [vars[_cor_to_idx(x, y, N)], vars[_cor_to_idx(a, b, N)]])
            con.add_satisfying_tuples(valid_bin_tuples)
            binary_csp.add_constraint(con)

    return (binary_csp, vars)


def nary_ad_grid(cagey_grid):
    n = cagey_grid[0]  # size of grid
    domain = [i + 1 for i in range(n)]  # domain of each variable
    var_array = [Variable("Cell({},{})".format(row, col), domain)
                 for row in domain for col in domain]
    grid_vars = [[var_array[(row - 1) * n + col - 1]
                  for col in domain] for row in domain]

    # defining all possible constraints and adding satisfying tuples to each constraint...
    satisfying_tuples = list(itertools.permutations(domain, n))
    constraints = [
        # row constraints
        Constraint("C(Row{})".format(i + 1), grid_row) for i, grid_row in enumerate(grid_vars)
    ] + [
        Constraint("C(Col{})".format(i + 1),
                   [grid_vars[j][i] for j in range(n)])  # Column constraints
        for i in range(n)
    ]
    for constraint in constraints:
        # Specify the constraint by adding its complete list of satisfying tuples
        constraint.add_satisfying_tuples(satisfying_tuples)

    csp = CSP("{}-Cagey-nary-ad".format(n), var_array)
    for constraint in constraints:
        csp.add_constraint(constraint)  # add constraints to the csp

    return csp, var_array


def cagey_csp_model(cagey_grid):
    # IMPLEMENT
    pass
