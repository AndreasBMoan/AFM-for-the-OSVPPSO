#import numpy as np
import math
import gurobipy as gp
import data
import optimizationModel as om
import plot

print("\n\n\n-----------------OLJA KJORER--------------------\n\n\n")

# -----------DATA----------


#Installations
InstNames = data.InstNames
Insts = data.Insts
Distance = data.Distance
ClosingInsts = data.ClosingInsts

#Vessels
Vessels = data.Vessels
VesselNames = data.VesselNames
AvaliableTime = data.AvaliableTime

#Times
Times = data.Times

#WeatherForecast
Weather = data.Weather
SpeedImpact = data.SpeedImpact

#Numbers
nInstallations = len(Insts)
nVessels = len(Vessels)
nTimes = len(Times)

#SingleParameters
fuelPrice = data.fuelPrice
maxSpeed = data.maxSpeed
minSpeed = data.minSpeed
serviceTime = data.serviceTime
dpFuelConsume = data.dpFuelConsume
idleFuelConsume = data.idleFuelConsume
depConsumption = data.depConsumption


#----------PARAMETER GENERATION---------------

#SailingLeg Objects


    
# Main


fuel_cost = [[[[[0 for tau in Times]for inst2 in Insts]for t in Times]for inst1 in Insts]for v in Vessels]


def service_not_possible(inst, time):
    if (Weather[time] == 3) or ((ClosingInsts[inst] == True) and ((time % 24 < 6) or (time % 24 > 18))) or ((inst == 0) and (time % 24 != 0)):
        return True
    else:
        return False
    
    

# Fuel consumption while at supply depot:
def depot_consumption(loadingTime):
    return loadingTime*depConsumption
    


# Consumption from propulsion while sailing between platforms:
def sail_consumption(fromInst, toInst, depTime, arrTime, serStartTime): 
    speed = (arrTime - depTime)/Distance[fromInst][toInst]
    consumed = 0
    for time3 in range(depTime, arrTime + 1):
        consumed += 2.7679*(speed + SpeedImpact[Weather[time3]])**2 - 38.75*(speed + SpeedImpact[Weather[time3]])+450.71
    return consumed * fuelPrice
    


# Consumption while idling, waiting for the installation to be ready for service:
def idle_consumption(arrTime, serStartTime):
    consumed = 0
    if (arrTime != serStartTime):
        for time3 in range(arrTime, serStartTime + 1):
            consumed += idleFuelConsume*(1 + Weather[time3] * 0.1)
    return consumed



# Consumption while servicing the installation:
def dp_consumption(serStartTime):
    consumed = 0
    for time3 in range(serStartTime, serStartTime + serviceTime +1):
        consumed += dpFuelConsume*(1 + Weather[time3] * 0.1)
    return consumed 



def add_arc(vessel, fromInst, toInst, startTime, depTime, arrTime, serStartTime, finTime):
    if math.ceil(Distance[toInst][0]/(maxSpeed)) + finTime <= AvaliableTime[vessel] + 168:
        fuel_cost[vessel][fromInst][startTime][toInst][finTime] = (
                depot_consumption(depTime - startTime) 
                + sail_consumption(fromInst, toInst, depTime, arrTime, serStartTime) 
                + idle_consumption(arrTime, serStartTime) 
                + dp_consumption(serStartTime))

def build_arcs(vessel, time1, inst1, loadingTime):
    
    for inst2 in Insts: 
        
        if inst2 != inst1: 
            tMin = (math.ceil(Distance[inst1][inst2]/maxSpeed) + loadingTime + time1)
            tMax = (math.ceil(Distance[inst1][inst2]/minSpeed) + loadingTime + time1) 
            closedVisit = 0 
            
            for time2 in range(tMax, tMin-1, -1):
                
                if ((service_not_possible(inst2, time2)) == True) and (closedVisit == 0): 
                    closedVisit = 1 
                    time3 = time2 + 1 
                    
                    while (service_not_possible(inst2, time3)) == True:
                        time3 += 1 
                        
                    if inst2 == 0: 
                        add_arc(vessel, inst1, inst2, time1, time1, time2, time2, time2)
                        
                    else:
                        add_arc(vessel, inst1, inst2, time1, time1 + loadingTime, time2 + loadingTime, time3 + loadingTime, time3 + serviceTime  + loadingTime) #Create an edge  
                        
                else: 
                    
                    if (service_not_possible(inst2, time2) == False): 
                        
                        if inst2 == 0:
                            add_arc(vessel, inst1, inst2, time1, time1, time2, time2, time2)
                            
                        else:
                           add_arc(vessel, inst1, inst2, time1, time1 + loadingTime, time2 + loadingTime, time2 + loadingTime, time2 + serviceTime + loadingTime) 


count = 0

#Deciding what nodes to create arcs from:
for vessel in Vessels:
    
    for time1 in range(AvaliableTime[vessel],AvaliableTime[vessel]+168,1):
        
        for inst1 in Insts: 
            
            if inst1 == 0:
                
                if  time1 % 24 == 0 and time1 <= 144 + AvaliableTime[vessel]:
                    build_arcs(vessel, time1, inst1, 8) 
                    
            else: 
                for tempinst in Insts:
                    
                    for temptime in Times:
                        
                        if fuel_cost[vessel][tempinst][temptime][inst1][time1] != 0:
                            build_arcs(vessel, time1, inst1, 0)
                            break
                    else:
                        continue
                    break


print("\n\nNetwork generation successful!")
print("------------------------------------------------")

print("Plotting graph....")

plot.draw_routes(fuel_cost,Insts,Times,Vessels)

#for v in Vessels:
#    for i in InstallationNums:
#        for t in Times:
#            for j in InstallationNums:
#                for tau in Times:
#                    if fuel_cost[v,i,t,j,tau] != 0:
#                        print(v,i,t,j,tau)
                
                        
    
print("-------------- OPTIMIZING MODEL ----------------\n")

try:
    om.solve(fuel_cost)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

##except AttributeError:
#    print('Encountered an attribute error: Mogadishu')
    