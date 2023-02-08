# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''


def ord_dh(csp):
    ''' return variables according to the Degree Heuristic 
    
    Degree	heuristic:	select		the	variable	that	is	involved	in	the	largest	number	of	
    constraints	on	other	unassigned	variables.	To	be	used	when	the	size	of	the	
    domains	is	the	same.	The	degree	heuristic	can	be	useful	as	a	tie-breaker	in	
    connection	with	MRV.
    '''
    vars = csp.get_all_unasgn_vars()
    curr = vars[0]  # current var with largest # of constraints
    maxval = 0
    for var in vars:
        vcons = csp.get_cons_with_var(var) # list of constraints for the current variable
        var_unasgn = []
        for con in vcons:
            for cvar in con.get_unasgn_vars():
                if cvar not in var_unasgn:
                    var_unasgn.append(cvar)
        if len(var_unasgn) > maxval:
            curr = var
            maxval = len(var_unasgn)
    return curr


def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic 

    Minimum-Remaining-Values (MRV) heuristic: Choosing the variable	with	the	
    fewest	“legal”	remaining	values	in	its	domain.
    Also	called	most	costrained variable	or	fail-first heuristics,	because	it	helps	in	
    discovering	inconsistencies	earlier.
    '''
    vars = csp.get_all_vars()
    curr = vars[0]  # current var with minimum remaining value
    minval = curr.cur_domain_size()
    for var in vars:
        if var.cur_domain_size() < minval:
            minval = var.cur_domain_size()
            curr = var
    return curr
