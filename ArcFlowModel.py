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
    
    
    
# Total conumption for an arc:    
def get_consumption(fromInst, toInst, loadingTime, depTime, arrTime, serStartTime, finTime):
    return depot_consumption(loadingTime) + sail_consumption(fromInst, toInst, depTime, arrTime, serStartTime) + idle_consumption(arrTime, serStartTime) + dp_consumption(serStartTime)
    


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



# Check if the vessel will have time to return to the depot within the end of weekif it sails to installation inst2:
def time_to_return(vessel, inst2, time2):
    if  math.ceil(Distance[inst2][0]/(maxSpeed - SpeedImpact[Weather[time2]])) + time2 <= AvaliableTime[vessel] + 168: #HER SJEKKER VI KUN WEATHER AV STARTTIDEN PÅ LEGGET
        return True
    else:
        return False


#Deciding what arcs to create & creating them
def build_arcs(vessel, time1, inst1, loadingTime):
    
    #For all installations
    for inst2 in Insts: 
        
        #That are not equal to the installation you are sailing from
        if inst2 != inst1: 
            
            #Calculate the earliest and latest possible arrival time
            tMin = (math.ceil(Distance[inst1][inst2]/maxSpeed) + loadingTime + time1)
            tMax = (math.ceil(Distance[inst1][inst2]/minSpeed) + loadingTime + time1) 
            
            #Initializa a variable that ensures we only sail to a closed installation at the latest possible arrival time
            closedVisit = 0 
            
            #iterate through all possible arrival times between tMax & tMin
            for time2 in range(tMax, tMin-1, -1):
                
                #Check if the vessel arrives at a time where service is not possible and that the vessel is not arriving at a later time
                if ((service_not_possible(inst2, time2)) == True) and (closedVisit == 0): 
                    
                    #update closed visit variable
                    closedVisit = 1 
                    
                    #initiate end of waiting time variable
                    time3 = time2 + 1 
                    
                    #While service cannot be performed
                    while (service_not_possible(inst2, time3)) == True:
                        
                        #update end of waiting time variable
                        time3 += 1 
                    
                    #if the arrival-installation is the depot
                    if inst2 == 0: 
                        
                        #create a to-depot specific edge
                        fuel_cost[vessel][inst1][time1][inst2][time2] = get_consumption(inst1, inst2, loadingTime, time1, time2, time2, time2)
                    
                    #else (if installation isnt depot) check if the vessel has time to return to depot after visiting the installation
                    elif time_to_return(vessel, inst2, time3 + serviceTime) == True:
                        fuel_cost[vessel][inst1][time1][inst2][time3 + serviceTime + loadingTime] = get_consumption(inst1, inst2, loadingTime, time1 + loadingTime, time2, time3, time3 + serviceTime) #Create an edge
                        
                else: 
                    
                    #if service can be performed upon arrival
                    if (service_not_possible(inst2, time2) == False):
                        
                        #and vessel has time to return to depot
                        if time_to_return(vessel, inst2, time2 + serviceTime) == True: 
                            
                            #if the arrival-installation is the depot
                            if inst2 == 0:
                                
                                #create depot-specific edge 
                                fuel_cost[vessel][inst1][time1][inst2][time2] = get_consumption(inst1, inst2, loadingTime, time1, time2, time2, time2)
                                
                            else:
                                
                                #create edge
                                fuel_cost[vessel][inst1][time1][inst2][time2 + serviceTime + loadingTime] = get_consumption(inst1, inst2, loadingTime, time1 + loadingTime, time2, time2, time2 + serviceTime) 


count = 0

#Deciding what nodes to create arcs from:
for vessel in Vessels:
    
    for time1 in range(AvaliableTime[vessel],AvaliableTime[vessel]+168,1):

        for inst1 in Insts:
            
            if time_to_return(vessel, inst1, time1):
                
                if inst1 == 0:
                    
                    if  time1 % 24 == 0 and time1 <= 144 + AvaliableTime[vessel]: #We define 8 o clock the first day as the first time index
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
    