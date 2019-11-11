import gurobipy as gp
#import numpy as np
#import time

def solve(Insts, Vessels, Times, fuel_cost):

    model = gp.Model()

    # ------ SETS -------------
    Voys = [0]#,1,2]
    
    # ------ PARAMETERS ------
    
    DemandNum = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,20,21,22,23,24,25,26]
#    Demand = DemandNum*100
#    VesselCap = [10000,10000,10000,10000,10000,10000]

    
    print("Number of Installations:",len(Insts))
    print("Number of vessels:      ",len(Vessels))
    print("Number of time periods: ",len(Times))
    print("Number of voyages:      ",len(Voys))

    
    departure_times = [[[[]for j in Insts] for i in Insts] for v in Vessels]
    
    for v in Vessels:
        for i in Insts:
            for j in Insts:
                for t in Times:
                    count = 0
                    for tau in Times:
                        if fuel_cost[v][i][t][j][tau] != 0:
                            count += 1
                    if count != 0:
                        departure_times[v][i][j].append(t)

    arrival_times = [[[[]for j in Insts] for i in Insts] for v in Vessels] 
    
    for v in Vessels:
        for i in Insts:
            for j in Insts:
                for tau in Times:
                    count = 0
                    for t in Times:
                        if fuel_cost[v][i][t][j][tau] != 0:
                            count += 1
                    if count != 0:
                        arrival_times[v][i][j].append(tau)




    specific_departure_times = [[[[[] for t in Times] for j in Insts] for i in Insts] for v in Vessels]
    
    for v in Vessels:
        for i in Insts:
            for t in Times:
                for j in Insts:
                    for tau in arrival_times[v][i][j]:
                        if fuel_cost[v][i][t][j][tau] != 0:
                            specific_departure_times[v][i][j][t].append(t)
                    
                    
                    


    specific_arrival_times = [[[[[] for j in Insts] for t in Times] for i in Insts] for v in Vessels]
                    
    for v in Vessels:
        for i in Insts:
            for j in Insts:
                for t in departure_times[v][i][j]:
                    for tau in Times:
                        if fuel_cost[v][i][t][j][tau] != 0:
                            specific_arrival_times[v][i][t][j].append(tau)
                    

                    
        
    for j in Insts:
        for v in Vessels:
            for i in Insts:
                if i != j:
                    for t in departure_times[v][i][j]:
                        for tau in specific_arrival_times[v][i][t][j]:
                            for m in Voys: 
                                if fuel_cost[v][i][t][j][tau] == 0:
                                    print("PROOOOOOOOBLEM!!! UUhhh OOoooooOOHHhhhhh..............")


    count = 0            
    for j in Insts:
        for v in Vessels:
            for i in Insts:
                if i != j:
                    for t in departure_times[v][i][j]:
                        for tau in specific_arrival_times[v][i][t][j]:
                            for m in Voys:
                                if fuel_cost[v][i][t][j][tau] != 0: 
                                    count += 1
    print("Number of variables:    ",count)
  
    
    # ------ VARIABLES --------

    x = [[[[[[None for m in Voys]for tau in Times]for j in Insts]for t in Times]for i in Insts]for v in Vessels]
    
    
    for v in Vessels:
        for i in Insts:
            for t in Times:
                for j in Insts:
                    for tau in Times:
                        if fuel_cost[v][i][t][j][tau] != 0:
                            for m in Voys:
                                    x[v][i][t][j][tau][m] = model.addVar(vtype=gp.GRB.BINARY, name=("x_" + str(v) + "_" + str(i) + "_" + str(t) + "_" + str(j) + "_" + str(tau) + "_" + str(m)))



#            print("\rGenerating variables: %d%% "%math.ceil(counter*100/(np.size(Vessels)*np.size(Insts))), end="\r", flush = True)
#            counter += 1

    print("\n\nAll variables created successfully!\n")
    
    
    print("testing variables and sets")
    print(x[0][0][0][1][23][0])
    
    for v in Vessels:
        for i in Insts:
            for j in Insts:
                if j != i:  
                    for t in departure_times[v][i][j]:
                        for tau in specific_arrival_times[v][i][t][j]:
                            for m in Voys:
                                print(x[v][i][t][j][tau][m])

    for v in Vessels:
        for i in Insts:
            for j in Insts:  
                for t in Times:
                    for tau in Times:
                        for m in Voys:
                            if type(x[v][i][t][j][tau][m]) != None:
                                print(x[v][i][t][j][tau][m])
                                

    # ------- CONSTRAINTS --------

    constrCounter = 1

#
#
#    """Flow conservation"""
#    
#
#    for v in Vessels:
#        for i in Insts:
#            if i != 0:
#                for t in Times:                    
#                    if np.size(np.nonzero(fuel_cost[v,i,t,:,:])[0]) + np.size(np.nonzero(fuel_cost[v,:,:,i,t])[0]) != 0:
#                        for m in Voys:
#                            model.addConstr(
#                                    
#                                    gp.quicksum(
#                                            
#                                            model.x[v, j, tau, i, t, m]
#                                    
#                                            for j in Insts if j!=i
#                                            for tau in specific_departure_times[v][j][i][t])
#                                    
#                                    - gp.quicksum(
#                                            
#                                            model.x[v, i, t, j, tau, m]
#                                    
#                                            for j in Insts if j!= i
#                                            for tau in specific_arrival_times[v][i][t][j])
#                            
#                                    == 0, "Flow Conservation")
#                                    
#                                    
#
#    print("\n\nAll ConstrN%d created successfully!\n" % constrCounter)
#
#
#    """Any installation can only be visited once per voyage"""
#    
#    constrCounter += 1
#    
#    for j in Insts:
#        for v in Vessels:
#            for m in Voys:
#                model.addConstr(
#                        
#                        gp.quicksum(
#                                
#                                model.x[v,i,t,j,tau,m] 
#                                
#                                for i in Insts if i != j
#                                for t in departure_times[v][i][j]
#                                for tau in specific_arrival_times[v][j][t][j])
#                        
#                        <= 1 , "Only one Inst visit per voy")
#                            
#                            
#
#    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)
#    
#    
#    
#    """Evry PSV can only sail from the depot once per voyage"""
#    
#    constrCounter += 1
#    
#    for v in Vessels:
#        for m in Voys:
#            model.addConstr(
#                    
#                    gp.quicksum(
#                            
#                            model.x[v,0,t,j,tau,m] 
#                            
#                            for j in Insts 
#                            for t in departure_times[v][0][j]
#                            for tau in specific_arrival_times[v][0][t][j]) 
#                                
#                    <= 1, "Only sail from depot once per voyage")
#                                
#                                
#    
#    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)
#    
#    
#    
#    """Next voyage must start after the last one"""
#
#    constrCounter += 1
#    
#    for v in Vessels:                                                              # For all vessels
#        for m in Voys:                                                             # and all voyages
#            if m != 0:                                                             # if it isnt the first voyage
#                model.addConstr(
#                        
#                        gp.quicksum(
#                                
#                                tau * model.x[v,i,t,0,tau,m-1]                     # The sum of finnishing times multiplied by the edge-variable for the last leg
#                                
#                                for i in Insts                                     # of all installation
#                                for t in departure_times[v][i][0]                  # and all possible departure times when sailing from i to j
#                                for tau in specific_arrival_times[v][i][t][0])     
#                        
#                        - gp.quicksum(
#                                
#                                t * model.x[v,0,t,j,tau,m] 
#                                
#                                for j in Insts 
#                                for t in departure_times[v][0][j] 
#                                for tau in specific_arrival_times[v][0][t][j])
#                        
#                        - 300 * (1 - gp.quicksum(
#                                
#                                model.x[v,0,t,j,tau,m]
#                                
#                                for j in Insts 
#                                for t in departure_times[v][0][j]
#                                for tau in specific_arrival_times[v][0][t][j])) 
#                        
#                        >= 0 , "Next voyage must start after current voyage" )
#
#
#
#
#    
#    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)
    
    
    
    """All service jobs must be performed"""
    
    constrCounter += 1
    
    for j in Insts:                                                             # for all installations j
        if j != 0:                                                              # which is not the depot
            model.addConstr(
                    
                    gp.quicksum(
                            
                            model.x[v][i][t][j][tau][m]                         # sum over all x
                            
                            for v in Vessels                                    # for all vessels v
                            for i in Insts 
                            if i != j                                           # and installations i
                            for t in departure_times[v][i][j]                   # from the times where you can sail from i to j with s v
                            for tau in specific_arrival_times[v][i][t][j]       # to the times where you can arrive at j when sailing from i at time t
                            for m in Voys)                                      # and for all the voyages
    
                    == DemandNum[j], "All service jobs must be performed")      # must be equal to the demand at j
    
                                    
    
    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)
    
    
#    """PSV capacity"""
#    
#    constrCounter += 1
#    
#    for v in Vessels:
#        for m in Voys:
#            model.addConstr(
#                    
#                    gp.quicksum(
#                            
#                            model.x[v,i,t,j,tau,m] * Demand[j] 
#                            
#                            for i in Insts 
#                            for j in Insts if j != 0
#                            for t in departure_times[v][i][j]
#                            for tau in specific_arrival_times[v][i][t][j]) 
#                    
#                    <= VesselCap[v], "PSV capacity")
#
#    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)



    # ------- OBJECTIVE ----------
    
    model.setObjective(
            
            gp.quicksum( model.x[v,i,t,j,tau,m] * fuel_cost[v][i][t][j][tau] 
                for v in Vessels 
                for i in Insts 
                for j in Insts if j != i
                for t in departure_times[v][i][j]
                for tau in specific_arrival_times[v][i][t][j]), 
            
            gp.GRB.MINIMIZE)
                        
                        
#    model.computeIIS()
#    print("------------------------------")
#    model.write("model.ilp")
#    print(model)
#    print("------------------------------")

    model.optimize()
    
#    print("------------------------------")
#
#    # Print variable names and solutions
#    for v in model.getVars():
#        print('%s %g' % (v.varName, v.x))
#
#
##    Inspect solution and return output
#    
#    if model.status == gp.GRB.OPTIMAL:
#        print('\nOptimal objective value: %g\n' % model.ObjVal)
#
#    else:
#        print('No optimal solution found. Status: %i' % (model.status))
#
#    return model



"""OLD STUFF

print("\rGenerating all ConstrN%d: %d%% "%(constrCounter, math.ceil(counter*100/(np.size(Insts)*np.size(Vessels)))), end="\r", flush = True)
            
            
            
"""