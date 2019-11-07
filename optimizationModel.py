import gurobipy as gp
import numpy as np
import math
import time

def solve(InstallationNums, VesselNums, Times, LegNet):

    model = gp.Model()

    # ------ SETS -------------
    Legs = LegNet
    Insts = InstallationNums
    Vessels = VesselNums
    Times = Times
    Voys = np.array([0,1,2])
    
    # ------ PARAMETERS ------
    
    DemandNum = np.array([1,1,1,1,1,1,1,2,3,4,2,1,2,3,1,1,1,17,18,19,20,21,22,23,24,25,26])
    Demand = DemandNum*100
    VesselCap = np.array([10000,10000,10000,10000,10000,10000])
    
    InstTimes = [[[] for i in Insts] for v in Vessels]
    for v in Vessels:
        for i in Insts:
            for t in Times:
                count = 0
                for j in Insts:
                    for tau in Times:
                        if Legs[v,j,tau,i,t] != 0:
                            count += 1
                if count != 0:
                    InstTimes[v][i].append(t)
                    
    
    
    InTimes = [[[[[] for t in Times] for i in Insts] for j in Insts] for v in Vessels]

    for v in Vessels:
        for j in Insts:
            for i in Insts:
                for t in Times:
                    InTimes[v][j][i].append((np.nonzero(Legs[v,j,:,i,t])[0]))

    OutTimes = [[[[[] for j in Insts] for t in Times] for i in Insts] for v in Vessels]
    for v in Vessels:
        for i in Insts:
            for t in Times:
                for j in Insts:
                    OutTimes[v][i][t].append((np.nonzero(Legs[v, i, t, j, :])[0]))
                    


    #Out-times
    
    
    
    # ------ VARIABLES --------

    x = {}
    
    counter = 0
    
    for v in Vessels:
        for i in Insts:
            print("\rGenerating variables: %d%% "%math.ceil(counter*100/(np.size(Vessels)*np.size(Insts))), end="\r", flush = True)
            counter += 1
            for t1 in Times:
                for j in Insts:
                    for t2 in Times:
                        if Legs[v,i,t1,j,t2] != 0:
                            for m in Voys:
                                x[v, i , t1, j, t2, m] = model.addVar(vtype=gp.GRB.BINARY, name=("x_" + str(v) + "_" + str(i) + "_" + str(t1) + "_" + str(j) + "_" + str(t2) + "_" + str(m)))

    print("\n\nAll variables created successfully!\n")

    # ------- CONSTRAINTS --------

    constrCounter = 1



    # Flow conservation
    

    for v in Vessels:
        for i in Insts:
            if i != 0:
                for t in InstTimes[v][i]:
                    for m in Voys:
                        model.addConstr(gp.quicksum(model.x[v, j, tau, i, t, m]
                        for j in Insts if j!=i
                        for tau in InTimes[v][j][i][t])
                        - gp.quicksum(model.x[v, i, t, j, tau, m]
                        for j in Insts if j!= i
                        for tau in OutTimes[v][i][t][j])
                        == 0, "Flow Constraint")

    print("\n\nAll ConstrN%d created successfully!\n" % constrCounter)


    # Any installation can only be visited once per voyage
    
    constrCounter += 1
    
    for j in Insts:
        if j != 0:
            for v in Vessels:
                counter += 1
                for m in Voys:
                    model.addConstr(gp.quicksum(model.x[v,i,t,j,tau,m] 
                        for i in Insts
                        for t in InstTimes[v][i] 
                        for tau in InTimes[v][j][i][t])
                        <= 1 , "Only one Inst visit per voy")

    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)
    
    
    
    # Evry PSV can only sail from the depot once per voyage
    
    constrCounter += 1
    
    for v in Vessels:
        for m in Voys:
            counter += 1
            model.addConstr(gp.quicksum(model.x[v,0,t,j,tau,m] 
                for t in Times
                for j in Insts 
                for tau in OutTimes[v][0][t][j]) 
                <= 1, "Only sail from depot once per voyage")
    
    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)
    
    
    
    # Next voyage must start after the last one
    
    counter = 0
    constrCounter += 1
    
    for v in Vessels:
        for m in Voys:
            if m != 0:
                model.addConstr(gp.quicksum(model.x[v,i,t,0,tau,m-1]*tau 
                    for i in Insts 
                    for t in InstTimes[v][i] 
                    for tau in OutTimes[v][i][t][0]) 
                    - gp.quicksum(m.x[v,0,t1,j,t2,m]*t 
                    for j in Insts 
                    for t in InstTimes[v][i] 
                    for tau in OutTimes[v][0][t][j]) 
                    - gp.quicksum(1-m.x[v,0,t1,j,t2,m]*300 
                    for j in Insts 
                    for t in InstTimes[v][i]
                    for tau in OutTimes[v][0][t][j]) 
                    >= 0 , "Next voyage must start after current voyage" )
    
    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)
    
    
    
    # All service jobs must be performed
    
    constrCounter += 1
    
    for j in Insts:
        model.addConstr(gp.quicksum(model.x[v,i,t,j,tau,m] 
            for v in Vessels
            for i in Insts 
            for j in Insts if j != 0
            for t in InstTimes[v][i]
            for tau in OutTimes[v][i][t][j] 
            for m in Voys) 
            >= DemandNum[j], "All service jobs must be performed")
    
    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)
    
    
    
    # PSV capacity
    
    constrCounter += 1
    
    for v in Vessels:
        for m in Voys:
            model.addConstr(gp.quicksum(model.x[v,i,t,j,tau,m]*Demand[j] 
                for i in Insts 
                for j in Insts if j != 0
                for t in InstTimes[v][i] 
                for tau in OutTimes[v][i][t][j]) 
                <= VesselCap[v])

    print("\n\nAll ConstrN%d created successfully!\n" %constrCounter)



    # ------- OBJECTIVE ----------
    
    model.setObjective(gp.quicksum(model.x[v,i,t,j,tau,m]*Legs[v,i,t,j,tau] 
        for v in Vessels 
        for i in Insts 
        for t in InstTimes[v][i]
        for j in Insts 
        for tau in OutTimes[v][i][t][j]), 
        gp.GRB.MINIMIZE)
                        
                        
    model.computeIIS()
    print("------------------------------")
    model.write("model.ilp")
    print()
    print("------------------------------")

    model.optimize()
    
    print("------------------------------")

    # Print variable names and solutions
    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))


    # Inspect solution and return output
    if m.status == gp.GRB.OPTIMAL:
        print('\nOptimal objective value: %g\n' % m.ObjVal)

    else:
        print('No optimal solution found. Status: %i' % (m.status))

    return m



"""OLD STUFF

print("\rGenerating all ConstrN%d: %d%% "%(constrCounter, math.ceil(counter*100/(np.size(Insts)*np.size(Vessels)))), end="\r", flush = True)
            
            
            
"""