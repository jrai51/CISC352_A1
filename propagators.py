# =============================
# Student Names: Mercy Doan, Yash Patel, Jagrit Rai
# Group ID: 51
# Date: February 1, 2023
# =============================
# CISC 352 - W23
# propagators.py
# desc:
#


# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''


def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple(vals):
                return False, []
    return True, []


def prop_FC(csp, newVar=None):
    # IMPLEMENT

    # Use a set to keep track of the pruned values, better than a list!
    # exit when the variable's domain is found

    pruned = set()  # Create a set of pruned values
    if not newVar:  # If there is no new variable...
        for c in csp.get_all_cons():  # Iterate through all constraints
            if c.get_n_unasgn() == 1:  # if there is only one unassigned variable usign the api call
                var = c.get_unasgn_vars()[0]  # get the variable
                for val in var.cur_domain():  # iterate through the variable's domain
                    # if the value is not in the domain...
                    if not c.check_var_val(var, val):
                        # prune the value according to the api call
                        var.prune_value(val)
                        # add the pruned value to the set of pruned values to keep track
                        pruned.add((var, val))
                        if var.cur_domain_size() == 0:  # if the domain size is 0, return false alongside the pruned values
                            return False, pruned
    else:  # If newVar has a value, we evaluate the constraints that include the newVar variable.
        # check all constraints that contain the newVar variable
        for c in csp.get_cons_with_var(newVar):
            if c.get_n_unasgn() == 1:  # If there is just 1 unassigned variable in the constraint
                var = c.get_unasgn_vars()[0]  # get said variable
                for val in var.cur_domain():  # for each value in the variable's domain
                    # if the value is not in the domain of the variable
                    if not c.check_var_val(var, val):
                        # prune the value according to the api call
                        var.prune_value(val)
                        # add the pruned value to the set of pruned values to keep track
                        pruned.add((var, val))
                        if var.cur_domain_size() == 0:  # if the domain size is 0, return false alongside the pruned values
                            return False, pruned
    return True, pruned


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''

    # Remember: deleting from the tail

    # IMPLEMENT

    # Queue has to be list of tuples.
    # Each tuple is head(Variable) and a tail(Constraint that includes the head variable).

    cons = []
    pruned = []

    if newVar == None:
        queue = []  # Initially all hyperarcs in the CSP
        cons = csp.get_all_cons()
        for con in cons:
            for var in con.scope:
                queue.append((var, con))
    else:
        queue = []
        cons = csp.get_cons_with_var(newVar)
        for con in cons:
            queue.append((newVar, con))

    while queue:
        Xi, C = queue.pop(0)  # Get a variable and a constraint
        print(Xi, C)
        removed = False
        for val in Xi.cur_domain():
            for Y in C.scope:
                if not C.check_var_val(val, Y):
                    print("check4", val, Y)
                    pair = (val, Y)
                    pruned.append(pair)
                    val.prune_value(Y)
                    removed = True
                    print('check2', removed)

        if removed:
            if Xi.cur_domain_size() == 0:
                return False, pruned

            for Xk in neighbours(Xi):
                # look at node Xk that is a neighbour of Xi, and the nodes that Xk are connected to
                neighbour_cons = csp.get_cons_with_var(Xk)
                for con in neighbour_cons:
                    queue.append((Xk, con))
    return True, pruned

    pass


def neighbours(csp, Xi):
    # Find the Constraints that contains Xi.
    cons = csp.get_all_cons_with_var(Xi)
    # Find the Variables that are in those Constraints, these Variables are the neighbours.
    vars = set(cons.scope)
    return vars
