import gurobipy as gp
import data
import plotSol
#import numpy as np
#import time

def solve(fuel_cost):

    model = gp.Model()

    # =============== SETS ===============
    
    
    # --------------- Voys ---------------
    
    Voys = data.Voys
    
    Insts = data.Insts
    
    Vessels = data.Vessels
    
    Times = data.Times
    
    
    
    # --------------- node_times ---------------
    
    node_times = [[[]for i in Insts]for v in Vessels]
    
    for v in Vessels:
        for i in Insts:
            for t in Times:
                count = 0
                for j in Insts:
                    for tau in Times:
                        if fuel_cost[v][j][tau][i][t] != 0 or fuel_cost[v][i][t][j][tau] != 0:
                            count += 1
                if count != 0:
                    node_times[v][i].append(t)
    
    
    
    # --------------- to_insts ---------------
                    
    to_insts = [[[[]for t in Times]for i in Insts]for v in Vessels] # tror denne er riktig
    
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
                        
                        
                        
    # --------------- from_insts ---------------

    from_insts = [[[[]for tau in Times]for j in Insts]for v in Vessels]
    
    for v in Vessels:
        for j in Insts:
            for tau in node_times[v][j]:
                for i in Insts:
                    count = 0
                    for t in Times:
                        if fuel_cost[v][i][t][j][tau] != 0:
                            count += 1
                    if count > 0:
                        from_insts[v][j][tau].append(i)
                
                
                
    # --------------- departure_times ---------------
    
    departure_times = [[[[]for j in Insts] for i in Insts] for v in Vessels]    #ser riktig ut
    
    for v in Vessels:
        for i in Insts:
            for j in Insts:
                for t in Times:
                    count = 0
                    for tau in Times:                                           #kan evt skrive for tau større enn t (for å øke leseligheten)
                        if fuel_cost[v][i][t][j][tau] != 0:
                            count += 1
                    if count != 0:
                        departure_times[v][i][j].append(t)
                        
                        
                        
    # --------------- arrival_times ---------------

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



    # --------------- specific_departure_times ---------------

    specific_departure_times = [[[[[] for tau in Times] for j in Insts] for i in Insts] for v in Vessels]
    
    for v in Vessels:
        for i in Insts:
            for j in Insts:
                for tau in arrival_times[v][i][j]:
                    for t in Times:
                        if fuel_cost[v][i][t][j][tau] != 0:
                            specific_departure_times[v][i][j][tau].append(t)
                            
                            
                            
    # --------------- specific_arrival_times ---------------

    specific_arrival_times = [[[[[] for j in Insts] for t in Times] for i in Insts] for v in Vessels]
                    
    for v in Vessels:
        for i in Insts:
            for j in Insts:
                for t in departure_times[v][i][j]:
                    for tau in Times:
                        if fuel_cost[v][i][t][j][tau] != 0:
                            specific_arrival_times[v][i][t][j].append(tau)
    
    
    
    # =============== PARAMETERS ===============
    
    DemandNum = data.DemandNum
    
    Demand = data.Demand
    
    VesselCap = data.VesselCap
    
    # =============== VARIABLES ===============

    x = [[[[[[None for m in Voys]for t in Times]for j in Insts]for t in Times]for i in Insts]for v in Vessels]
    
    
    for v in Vessels:
        for m in Voys:
            for i in Insts:
                for j in Insts:
                    if j != i:
                        for t in departure_times[v][i][j]:
                            for tau in specific_arrival_times[v][i][t][j]:
                               x[v][i][t][j][tau][m] = model.addVar(vtype=gp.GRB.BINARY, name=("x_" + str(v) + "_" + str(m) + "_" + str(i) + "_" + str(t) + "_" + str(j) + "_" + str(tau)))
                        
    


#            print("\rGenerating variables: %d%% "%math.ceil(counter*100/(np.size(Vessels)*np.size(Insts))), end="\r", flush = True)
#            counter += 1

    print("\n\nAll variables created successfully!\n")
    
    
    
    # =============== MODEL UPDATE ===============

    model.update()



    # =============== SUMMARIZING MODEL ===============
    
    print("Number of Installations:",len(Insts))
    print("Number of vessels:      ",len(Vessels))
    print("Number of time periods: ",len(Times))
    print("Number of voyages:      ",len(Voys))
    
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



    # =============== CONSTRAINTS ===============


    # --------------- Flow conservation ---------------
    
    constrCounter = 1
    
    
    model.addConstrs((
            
            gp.quicksum(
                    
                    x[v][j][tau][i][t][m]
            
                    for j in from_insts[v][i][t]
                    for tau in specific_departure_times[v][j][i][t])
            
            - gp.quicksum(
                    
                    x[v][i][t][j][tau][m]
            
                    for j in to_insts[v][i][t]
                    for tau in specific_arrival_times[v][i][t][j])
            
            == 0
            
            for v in Vessels
            for i in Insts
            if i != 0
            for t in node_times[v][i]
            for m in Voys)
            
            , "Flow Conservation")
                                    

    print("\n\nAll ConstrN%d created successfully!\n" % constrCounter)


    
    # --------------- Any installation can only be visited once per voyage ---------------
    
    constrCounter += 1
    

    model.addConstrs((
            
            gp.quicksum(
                    
                    x[v][i][t][j][tau][m] 
                    
                    for i in Insts 
                    if i != j
                    for t in departure_times[v][i][j]
                    for tau in specific_arrival_times[v][i][t][j])
            
            <= 1 
            
            for j in Insts
            for v in Vessels
            for m in Voys)
            
            , "Only one Inst visit per voy")
                            
                            

    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)
    
    
    
    # --------------- Evry PSV can only sail from the depot once per voyage ---------------
    
    constrCounter += 1
    
    model.addConstrs((
            
            gp.quicksum(
                    
                    x[v][0][t][j][tau][m] 
                    
                    for j in Insts 
                    for t in departure_times[v][0][j]
                    for tau in specific_arrival_times[v][0][t][j]) 
                        
            <= 1
            
            for v in Vessels
            for m in Voys)
            
            , "Only sail from depot once per voyage")
                                
                                
    
    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)
    
    
    
    # --------------- Next voyage must start after the last one ---------------
    
    constrCounter += 1
    

    model.addConstrs((
            
            gp.quicksum(
                    
                    tau * x[v][i][t][0][tau][m-1]
                    
                    for i in Insts
                    for t in departure_times[v][i][0]
                    for tau in specific_arrival_times[v][i][t][0])    
            
            + 300 * (1 - gp.quicksum(
                    
                    x[v][i][t][0][tau][m-1]
                    
                    for i in Insts
                    for t in departure_times[v][i][0]
                    for tau in specific_arrival_times[v][i][t][0]))   
            
            - gp.quicksum(
                    
                    t * x[v][0][t][j][tau][m] 
                    
                    for j in Insts 
                    for t in departure_times[v][0][j] 
                    for tau in specific_arrival_times[v][0][t][j])
            
            - 300 * (1 - gp.quicksum(
                    
                    x[v][0][t][j][tau][m]
                    
                    for j in Insts 
                    for t in departure_times[v][0][j]
                    for tau in specific_arrival_times[v][0][t][j])) 
            
            <= 0 
            
            for v in Vessels
            for m in Voys
            if m != 0)
            
            , "Next voyage must start after current voyage" )



    
    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)
    
    
    
    # --------------- All service jobs must be performed ---------------
    
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
    
    
    
    # --------------- PSV capacity ---------------
    
    constrCounter += 1
    
    model.addConstrs((
            
            gp.quicksum(
                    
                    x[v][i][t][j][tau][m] * Demand[j] 
                    
                    for i in Insts 
                    for j in Insts 
                    if j != 0
                    for t in departure_times[v][i][j]
                    for tau in specific_arrival_times[v][i][t][j]) 
            
            <= VesselCap[v]
            
            for v in Vessels
            for m in Voys)
            
            , "PSV capacity")

    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)



    # =============== MODEL UPDATE ===============

    model.update()



    # =============== OBJECTIVE ===============
    
    model.setObjective(
            
            gp.quicksum(x[v][i][t][j][tau][m] * fuel_cost[v][i][t][j][tau] 
                for v in Vessels
                for m in Voys
                for i in Insts
                for j in Insts if j != i
                for t in departure_times[v][i][j]
                for tau in specific_arrival_times[v][i][t][j]), 
            
            gp.GRB.MINIMIZE)
                        
            
            
    # =============== MODEL UPDATE ===============

    model.update()



    # =============== RUN MODEL ===============
    
    model.optimize()
    
    model.printAttr('x')
    
    
    solEdges = [[[[[0 for tau in Times]for j in Insts]for t in Times]for i in Insts]for v in Vessels]
    
    for a in model.getVars():
        if a.varName[0] == 'x' and a.x == 1:
            temp = a.varName.split('_')
            solEdges[int(temp[1])][int(temp[3])][int(temp[4])][int(temp[5])][int(temp[6])] = 1
    
    
    tot = 0
    for v in Vessels:
        for i in Insts:
            for t in Times:
                for j in Insts:
                    for tau in Times:
                        tot += solEdges[v][i][t][j][tau]*fuel_cost[v][i][t][j][tau]
                        
    print(tot)
    
    plotSol.draw_routes(solEdges, fuel_cost)

