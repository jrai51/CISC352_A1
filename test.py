"""
N = 4
vars = []
for i in range (1, N+1):
    for j in range(1, N+1):
        dom = range(1, N+1)
        var = (i, j)
        vars.append(var)

rows = [vars[x:x+N] for x in range(0, len(vars), N)]
for row in rows:
    row_pairs = [(a, b) for idx, a in enumerate(row) for b in row[idx + 1:]]
    

valid_bin_tuples = [(i, j) for i in range(1, N+1) 
                    for j in range(1, N+1) 
                    if i != j ]

print(valid_bin_tuples)

""" 

def _cor_to_idx(x, y, N):
    """ Takes x,y coordinates and size N of grid and returns the index in the variable list"""
    return N*(x-1) + y - 1 


from cspbase import *

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

    rows = []
    for i in range(1, N+1):
        row = []
        for j in range(1, N+1):
            row.append((i,j))
        rows.append(row)

    for row in rows:
        row_pairs = [(a, b) for idx, a in enumerate(row) for b in row[idx + 1:]]
        for pair in row_pairs:
            cell1, cell2 = pair
            print('TEST',cell1, cell2)
            x,y = cell1
            a,b = cell2
            con = Constraint(f"DIFF_CELL({x},{y})_CELL({a},{b})",
                            [ vars[_cor_to_idx(x,y,N)], vars[_cor_to_idx(a,b,N)]])
            con.add_satisfying_tuples(valid_bin_tuples)
            binary_csp.add_constraint(con)
        
    
    cols = []
    for i in range(1, N+1):
        col = []
        for j in range(1, N+1):
            col.append((j, i))
        cols.append(col)
    #No two cells in a column can be the same 
    for col in cols:
        col_pairs = [(a, b) for idx, a in enumerate(col) for b in col[idx + 1:]]
        for pair in col_pairs:
            cell1, cell2 = pair
            x,y = cell1
            a,b = cell2
            con = Constraint(f"DIFF_CELL({x},{y})_CELL({a},{b})",
                            [ vars[_cor_to_idx(x,y,N)], vars[_cor_to_idx(a,b,N)]])
            con.add_satisfying_tuples(valid_bin_tuples)
            binary_csp.add_constraint(con)


    return (binary_csp, vars)


def X_binary_ne_grid(cagey_grid):
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

csp, vars = binary_ne_grid([3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")]])

print()
print(vars)
print(csp.get_all_cons())
