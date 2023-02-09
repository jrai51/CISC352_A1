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