import gurobipy as gp
import data
#import numpy as np
#import time

def solve(Insts, Vessels, Times, fuel_cost):

    model = gp.Model()

    # ------ SETS -------------
    Voys = data.Voys
    
    # ------ PARAMETERS ------
    DemandNum = data.DemandNum
#    Demand = data.Demand
#    VesselCap = data.VesselCap
    
    print("Number of Installations:",len(Insts))
    print("Number of vessels:      ",len(Vessels))
    print("Number of time periods: ",len(Times))
    print("Number of voyages:      ",len(Voys))


    node_times = [[[]for i in Insts]for v in Vessels]
    
    for v in Vessels:
        for i in Insts:
            for t in Times:
                count = 0
                for j in Insts:
                    for tau in Times:
                        if fuel_cost[v][i][t][j][tau] != 0:
                            count += 1
                if count != 0:
                    node_times[v][i].append(t)
                    
    to_insts = [[[[]for t in Times]for i in Insts]for v in Vessels]
    
    for v in Vessels:
        for i in Insts:
            for t in node_times[v][i]:
                for j in Insts:
                    count = 0
                    for tau in Times:
                        if fuel_cost[v][i][t][j][tau] != 0:
                            count += 1
                    if count > 0:
                        to_insts[v][i][t].append(j)

    from_insts = [[[[]for t in Times]for i in Insts]for v in Vessels]
    for v in Vessels:
        for j in Insts:
            for tau in node_times[v][i]:
                for i in Insts:
                    count = 0
                    for t in Times:
                        if fuel_cost[v][i][t][j][tau] != 0:
                            count += 1
                    if count > 0:
                        from_insts[v][j][tau].append(i)

    
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
                            specific_departure_times[v][i][j][tau].append(t)
                    
                    
                    


    specific_arrival_times = [[[[[] for j in Insts] for t in Times] for i in Insts] for v in Vessels]
                    
    for v in Vessels:
        for i in Insts:
            for j in Insts:
                for t in departure_times[v][i][j]:
                    for tau in Times:
                        if fuel_cost[v][i][t][j][tau] != 0:
                            specific_arrival_times[v][i][t][j].append(tau)
                    


    # Finding number of variables:
    count = 0            
    for i in Insts:
        for v in Vessels:
            for j in Insts:
                if i != j:
                    
#                    print("Departures:",v,i,j,departure_times[v][i][j])
                    
                    for t in departure_times[v][i][j]:
                        
#                        print("Arrivals:",v,i,t,j,specific_arrival_times[v][i][t][j])
                        
                        for tau in specific_arrival_times[v][i][t][j]:
                            for m in Voys:
                                if fuel_cost[v][i][t][j][tau] != 0: 
                                    count += 1
                                    
    print("Number of variables:    ",count)
    
    # ------ Parameter Testing ------
    
    print("testing...")
    A = [[[[[0 for tau in Times]for j in Insts]for t in Times]for i in Insts]for v in Vessels]
    
    for v in Vessels:
        for j in Insts:
            for i in Insts:
                for tau in arrival_times[v][i][j]:
                    for t in specific_departure_times[v][i][j][tau]:
                        A[v][i][t][j][tau] = 1
    
    print("verification...")
    for v in Vessels:
        for j in Insts:
            for tau in node_times[v][j]:
                for i in from_insts[v][j][tau]:
                    for t in specific_departure_times[v][i][j][tau]:
                        if A[v][i][t][j][tau] != 1:
                            print("1 - NOT EQUAL!!!")
                        A[v][i][t][j][tau] = 2
    
    for v in Vessels:
        for j in Insts:
            for i in Insts:
                for tau in arrival_times[v][i][j]:
                    for t in specific_departure_times[v][i][j][tau]:
                        if A[v][i][t][j][tau] != 2:
                            print("2 - NOT EQUAL!!!")

  
    
    # ------ VARIABLES --------

    x = [[[[[[None for m in Voys]for t in Times]for j in Insts]for t in Times]for i in Insts]for v in Vessels]
    
    
    for v in Vessels:
        for i in Insts:
            for j in Insts:
                if j != i:
                    for t in departure_times[v][i][j]:
                        for tau in specific_arrival_times[v][i][t][j]:
                            for m in Voys:
                               x[v][i][t][j][tau][m] = model.addVar(vtype=gp.GRB.BINARY, name=("x_" + str(v) + "_" + str(i) + "_" + str(t) + "_" + str(j) + "_" + str(tau) + "_" + str(m)))
                        
    


#            print("\rGenerating variables: %d%% "%math.ceil(counter*100/(np.size(Vessels)*np.size(Insts))), end="\r", flush = True)
#            counter += 1

    print("\n\nAll variables created successfully!\n")
    

    model.update()

    # ------- CONSTRAINTS --------

    constrCounter = 1
#
#
#
#    """Flow conservation"""
#    
#
#    
#    model.addConstrs((
#            
#            gp.quicksum(
#                    
#                    x[v, j, tau, i, t, m]
#            
#                    for j in from_insts[v][i][t]
#                    for tau in specific_departure_times[v][j][i][t])
#            
#            - gp.quicksum(
#                    
#                    x[v, i, t, j, tau, m]
#            
#                    for j in to_insts[v][i][t]
#                    for tau in specific_arrival_times[v][i][t][j])
#            
#            == 0
#            
#            for v in Vessels
#            for i in Insts
#            if i != 0
#            for t in node_times[v][i]
#            for m in Voys)
#            
#            , "Flow Conservation")
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
#
#    model.addConstr((
#            
#            gp.quicksum(
#                    
#                    x[v,i,t,j,tau,m] 
#                    
#                    for i in Insts if i != j
#                    for t in departure_times[v][i][j]
#                    for tau in specific_arrival_times[v][j][t][j])
#            
#            <= 1 
#            
#            for j in Insts
#            for v in Vessels
#            for m in Voys)
#            
#            , "Only one Inst visit per voy")
#                            
#                            
#
#    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)
    
#    
#    
#    """Evry PSV can only sail from the depot once per voyage"""
#    
#    constrCounter += 1
#    
#    model.addConstrs((
#            
#            gp.quicksum(
#                    
#                    x[v,0,t,j,tau,m] 
#                    
#                    for j in Insts 
#                    for t in departure_times[v][0][j]
#                    for tau in specific_arrival_times[v][0][t][j]) 
#                        
#            <= 1
#            
#            for v in Vessels
#            for m in Voys)
#            
#            , "Only sail from depot once per voyage")
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
#
#    model.addConstrs((
#            
#            gp.quicksum(
#                    
#                    tau * x[v,i,t,0,tau,m-1]                     # The sum of finnishing times multiplied by the edge-variable for the last leg
#                    
#                    for i in Insts                                     # of all installation
#                    for t in departure_times[v][i][0]                  # and all possible departure times when sailing from i to j
#                    for tau in specific_arrival_times[v][i][t][0])     
#            
#            - gp.quicksum(
#                    
#                    t * x[v,0,t,j,tau,m] 
#                    
#                    for j in Insts 
#                    for t in departure_times[v][0][j] 
#                    for tau in specific_arrival_times[v][0][t][j])
#            
#            - 300 * (1 - gp.quicksum(
#                    
#                    x[v,0,t,j,tau,m]
#                    
#                    for j in Insts 
#                    for t in departure_times[v][0][j]
#                    for tau in specific_arrival_times[v][0][t][j])) 
#            
#            >= 0 
#            
#            for v in Vessels
#            for m in Voys
#            if m != 0)
#            
#            , "Next voyage must start after current voyage" )
#
#
#
#
#    
#    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)
#    
    
    
    print("All service jobs must be performed")
    
    constrCounter += 1
    
    model.addConstrs((
            
            gp.quicksum(
                    
                    x[v][i][t][j][tau][m]
                    
                    for v in Vessels
                    for i in Insts 
                    if i != j
                    for t in departure_times[v][i][j]
                    for tau in specific_arrival_times[v][i][t][j]
                    for m in Voys)
            
            == DemandNum[j]
            
            for j in Insts
            if j != 0)
            
            , name = ('Demanded_visits_' + str(j)))
    
                                    
    
    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)
    
    
    """PSV capacity"""
    
    constrCounter += 1
    
#    model.addConstr((
#            
#            gp.quicksum(
#                    
#                    x[v,i,t,j,tau,m] * Demand[j] 
#                    
#                    for i in Insts 
#                    for j in Insts if j != 0
#                    for t in departure_times[v][i][j]
#                    for tau in specific_arrival_times[v][i][t][j]) 
#            
#            <= VesselCap[v]
#            
#            for v in Vessels
#            for m in Voys)
#            
#            , "PSV capacity")
#
#    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)


    model.update()

    # ------- OBJECTIVE ----------
    
    model.setObjective(
            
            gp.quicksum(x[v][i][t][j][tau][m] * fuel_cost[v][i][t][j][tau] 
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
    
    model.printAttr('x')
    
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