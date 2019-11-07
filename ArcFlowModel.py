import numpy as np
import math
import gurobipy as gp
import plotly.graph_objects as go
import networkx as nx
import plot

import optimizationModel as om

print("\n\n\n-----------------OLJA KJORER--------------------\n\n\n")

# -----------DATA----------


#Installations
InstallationNames = np.array(['TRO','TRB','TRC','CPR','SEN','SDO','SEQ','OSE','OSB','OSC','OSO','SSC','OSS','DSD','KVB','VMO','WEL','VFB','WEP','HUL','STA','STB','STC','GFA','GFB','GFC','SOD'])

InstallationNums = np.array([0,1,2])#,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26])

Distance = np.array([[0.00,43.47,47.25,43.76,44.47,44.65,43.21,41.73,71.65,71.65,70.54,64.49,64.49,75.08,89.05,76.84,81.18,81.18,64.88,71.58,71.58,97.52,97.69,96.75,87.12,86.97,85.01,37.67],
                     [43.47,0.00,10.14,14.85,6.83,19.08,12.96,15.09,28.27,28.27,28.11,23.53,23.53,31.64,46.71,44.07,47.01,47.01,25.81,33.86,33.86,65.74,64.90,65.90,55.13,55.70,54.09,15.85],
                     [47.25,10.14,0.00,7.23,3.70,11.07,5.96,8.76,26.56,26.56,23.78,17.26,17.26,31.44,48.84,34.32,37.58,37.58,17.91,25.37,25.37,56.04,55.36,56.08,45.38,45.86,44.19,11.98],
                     [43.76,14.85,7.23,0.00,8.42,4.25,1.90,2.13,33.24,33.24,29.62,22.43,22.43,38.37,56.00,34.04,37.99,37.99,21.65,27.85,27.85,55.52,55.24,55.20,44.86,45.04,43.21,6.26],
                     [44.47,6.83,3.70,8.42,0.00,12.65,6.62,9.18,28.05,28.05,26.12,20.13,20.13,32.47,49.18,38.02,41.27,41.27,21.27,28.91,28.91,59.74,59.06,59.76,49.07,49.54,47.86,11.26],
                     [44.65,19.08,11.07,4.25,12.65,0.00,6.12,4.46,36.01,36.01,31.73,24.25,24.25,41.40,59.35,32.27,36.53,36.53,22.62,27.84,27.84,53.38,53.31,52.86,42.80,42.83,40.93,7.36],
                     [43.21,12.96,5.96,1.90,6.62,6.12,0.00,2.81,32.39,32.39,29.15,22.16,22.16,37.37,54.78,35.24,39.06,39.06,21.80,28.39,28.39,56.82,56.46,56.56,46.14,46.38,44.57,6.32],
                     [41.73,15.09,8.76,2.13,9.18,4.46,2.81,0.00,35.11,35.11,31.66,24.52,24.52,40.15,57.59,35.78,39.82,39.82,23.78,29.93,29.93,57.16,56.95,56.76,46.52,46.65,44.79,4.14],
                     [71.65,28.27,26.56,33.24,28.05,36.01,32.39,35.11,0.00,0.00,7.36,13.61,13.61,6.07,24.69,36.68,36.48,36.48,18.15,22.79,22.79,54.28,52.24,55.61,45.50,46.92,46.17,38.54],
                     [71.65,28.27,26.56,33.24,28.05,36.01,32.39,35.11,0.00,0.00,7.36,13.61,13.61,6.07,24.69,36.68,36.48,36.48,18.15,22.79,22.79,54.28,52.24,55.61,45.50,46.92,46.17,38.54],
                     [70.54,28.11,23.78,29.62,26.12,31.73,29.15,31.66,7.36,7.36,0.00,7.64,7.64,13.23,31.52,29.33,29.29,29.29,11.38,15.43,15.43,47.41,45.51,48.62,38.35,39.72,38.90,35.46],
                     [64.49,23.53,17.26,22.43,20.13,24.25,22.16,24.52,13.61,13.61,7.64,0.00,0.00,19.67,38.31,25.54,26.75,26.75,4.95,12.20,12.20,45.65,44.18,46.45,35.74,36.83,35.69,28.46],
                     [64.49,23.53,17.26,22.43,20.13,24.25,22.16,24.52,13.61,13.61,7.64,0.00,0.00,19.67,38.31,25.54,26.75,26.75,4.95,12.20,12.20,45.65,44.18,46.45,35.74,36.83,35.69,28.46],
                     [75.08,31.64,31.44,38.37,32.47,41.40,37.37,40.15,6.07,6.07,13.23,19.67,19.67,0.00,18.65,42.33,41.81,41.81,24.22,28.54,28.54,59.09,56.90,60.58,50.73,52.22,51.58,43.35],
                     [89.05,46.71,48.84,56.00,49.18,59.35,54.78,57.59,24.69,24.69,31.52,38.31,38.31,18.65,0.00,59.62,58.32,58.32,42.77,46.27,46.27,73.96,71.41,75.82,66.83,68.48,68.13,60.40],
                     [76.84,44.07,34.32,34.04,38.02,32.27,35.24,35.78,36.68,36.68,29.33,25.54,25.54,42.33,59.62,0.00,4.99,4.99,20.82,13.93,13.93,21.73,21.22,21.84,11.06,11.69,10.27,39.52],
                     [81.18,47.01,37.58,37.99,41.27,36.53,39.06,39.82,36.48,36.48,29.29,26.75,26.75,41.81,58.32,4.99,0.00,0.00,22.41,14.57,14.57,19.00,17.89,19.71,9.09,10.44,9.83,43.68],
                     [81.18,47.01,37.58,37.99,41.27,36.53,39.06,39.82,36.48,36.48,29.29,26.75,26.75,41.81,58.32,4.99,0.00,0.00,22.41,14.57,14.57,19.00,17.89,19.71,9.09,10.44,9.83,43.68],
                     [64.88,25.81,17.91,21.65,21.27,22.62,21.80,23.78,18.15,18.15,11.38,4.95,4.95,24.22,42.77,20.82,22.41,22.41,0.00,8.19,8.19,41.41,40.12,42.06,31.27,32.27,31.04,27.89],
                     [71.58,33.86,25.37,27.85,28.91,27.84,28.39,29.93,22.79,22.79,15.43,12.20,12.20,28.54,46.27,13.93,14.57,14.57,8.19,0.00,0.00,33.45,32.03,34.27,23.60,24.78,23.76,34.06],
                     [71.58,33.86,25.37,27.85,28.91,27.84,28.39,29.93,22.79,22.79,15.43,12.20,12.20,28.54,46.27,13.93,14.57,14.57,8.19,0.00,0.00,33.45,32.03,34.27,23.60,24.78,23.76,34.06],
                     [97.52,65.74,56.04,55.52,59.74,53.38,56.82,57.16,54.28,54.28,47.41,45.65,45.65,59.09,73.96,21.73,19.00,19.00,41.41,33.45,33.45,0.00,3.13,2.80,10.69,10.56,12.52,60.72],
                     [97.69,64.90,55.36,55.24,59.06,53.31,56.46,56.95,52.24,52.24,45.51,44.18,44.18,56.90,71.41,21.22,17.89,17.89,40.12,32.03,32.03,3.13,0.00,5.88,10.58,11.00,13.03,60.62],
                     [96.75,65.90,56.08,55.20,59.76,52.86,56.56,56.76,55.61,55.61,48.62,46.45,46.45,60.58,75.82,21.84,19.71,19.71,42.06,34.27,34.27,2.80,5.88,0.00,10.84,10.22,11.99,60.22],
                     [87.12,55.13,45.38,44.86,49.07,42.80,46.14,46.52,45.50,45.50,38.35,35.74,35.74,50.73,66.83,11.06,9.09,9.09,31.27,23.60,23.60,10.69,10.58,10.84,0.00,1.89,3.17,50.13],
                     [86.97,55.70,45.86,45.04,49.54,42.83,46.38,46.65,46.92,46.92,39.72,36.83,36.83,52.22,68.48,11.69,10.44,10.44,32.27,24.78,24.78,10.56,11.00,10.22,1.89,0.00,2.03,50.18],
                     [85.01,54.09,44.19,43.21,47.86,40.93,44.57,44.79,46.17,46.17,38.90,35.69,35.69,51.58,68.13,10.27,9.83,9.83,31.04,23.76,23.76,12.52,13.03,11.99,3.17,2.03,0.00,48.28],
                     [37.67,15.85,11.98,6.26,11.26,7.36,6.32,4.14,38.54,38.54,35.46,28.46,28.46,43.35,60.40,39.52,43.68,43.68,27.89,34.06,34.06,60.72,60.62,60.22,50.13,50.18,48.28,0.00]])

ClosingInsts =  np.array([0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

#Vessels

Vessels = np.array([0])#,1,2,3,4,5])

VesselNames = np.array(['A','B','C','D','E','F'])

AvaliableTime = np.array([0,24,48,0,24,48])

#Times

Times = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216])

#WeatherForecast
Weather = np.array([0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,2,2,2,2,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,3,3,3,3,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,3,3,3,3,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,3,3,3,3,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1])
SpeedImpact = np.array([0,0,-2,-3])

#Numbers
nInstallations = np.size(InstallationNums)
nVessels = np.size(Vessels)
nTimes = np.size(Times)

#SingleParameters
fuelPrice = 400
maxSpeed = 16
minSpeed = 7
serviceTime = 2
dpFuelConsume = 200
idleFuelConsume = 150
depConsumption = 1
Voyages = np.array([0,1,2])


#----------PARAMETER GENERATION---------------

#SailingLeg Objects


    
# Main



LegNet = np.zeros((np.size(Vessels), np.size(InstallationNums), np.size(Times), np.size(InstallationNums), np.size(Times)), float)  #Network is represented by a five dimensional np array




def service_not_possible(inst, time):
    if (Weather[time] == 3) or ((ClosingInsts[inst] == True) and ((time % 24 < 6) or (time % 24 > 18))) or ((inst == 0) and (time % 24 != 0)):
        return True
    else:
        return False
    
    
    
    
def get_consumption(fromInst, toInst, loadingTime, depTime, arrTime, serStartTime, finTime):
    return depot_consumption(loadingTime) + sail_consumption(fromInst, toInst, depTime, arrTime, serStartTime) + idle_consumption(arrTime, serStartTime) + dp_consumption(serStartTime)
    



def depot_consumption(loadingTime):
    return loadingTime*depConsumption
    



def sail_consumption(fromInst, toInst, depTime, arrTime, serStartTime): 
    consumed = 0
    for time3 in range(depTime, arrTime + 1):
        consumed += 1
    return consumed
    



def idle_consumption(arrTime, serStartTime):
    consumed = 0
    if (arrTime != serStartTime):
        for time3 in range(arrTime, serStartTime + 1):
            consumed += idleFuelConsume*(1 + Weather[time3] * 0.1)
    return consumed




def dp_consumption(serStartTime):
    consumed = 0
    for time3 in range(serStartTime, serStartTime + serviceTime +1):
        consumed += dpFuelConsume*(1 + Weather[time3] * 0.1)
    return consumed 




def time_to_return(vessel, inst2, time2):
    if inst2 == 0 and math.ceil(Distance[inst2,0]/(maxSpeed + SpeedImpact[Weather[time2]])) + time2 - serviceTime <= AvaliableTime[vessel] + 168:
        return True
    elif  math.ceil(Distance[inst2,0]/(maxSpeed + SpeedImpact[Weather[time2]])) + time2 <= AvaliableTime[vessel] + 168: #HER SJEKKER VI KUN WEATHER AV STARTTIDEN PÅ LEGGET
        return True
    else:
        return False



def build_arcs(vessel, time1, inst1, loadingTime):
    
    for inst2 in InstallationNums: #For all installations
        
        if inst2 != inst1: #That are not equal to the installation you are sailing from
            tMin = (math.ceil(Distance[inst1,inst2]/maxSpeed) + loadingTime + time1) #Calculate the earliest possible arrival time
            tMax = (math.ceil(Distance[inst1,inst2]/minSpeed) + loadingTime + time1) #and the latest possible arrival time
#            print(tMax - tMin)
            
            
            closedVisit = 0 #Initializa a variable that ensures we only sail to a closed installation at the latest possible arrival time
            
            
            
            for time2 in range(tMax, tMin-1, -1): #iterate through all possible arrival times between tMax & tMin
                
                
                if ((service_not_possible(inst2, time2)) == True) and (closedVisit == 0): #Check if the vessel arrives at a time where service is not possible and that the vessel is not arriving at a later time
                    
                    closedVisit = 1 #update closed visit variable

                    time3 = time2 + 1 #initiate end of waiting time variable
                    
                    while (service_not_possible(inst2, time3)) == True: #While service cannot be performed
                        time3 += 1 #update end of waiting time variable
                        
                    if inst2 == 0: #if the arrival-installation is the depot
                        LegNet[vessel, inst1, time1, inst2, time2] = get_consumption(inst1, inst2, loadingTime, time1, time2, time2, time2) #create a to-depot specific edge
                        
                    elif time_to_return(vessel, inst2, time3 + serviceTime) == True: #else (if installation isnt depot) check if the vessel has time to return to depot after visiting the installation
                        LegNet[vessel, inst1, time1, inst2, time3 + serviceTime + loadingTime] = get_consumption(inst1, inst2, loadingTime, time1 + loadingTime, time2, time3, time3 + serviceTime) #Create an edge
                        
                else: 
                    if (service_not_possible(inst2, time2) == False): #if service can be performed upon arrival
                        
                        if time_to_return(vessel, inst2, time2 + serviceTime) == True: #and vessel has time to return to depot
                            
                            if inst2 == 0: #if the arrival-installation is the depot
                                 LegNet[vessel, inst1, time1, inst2, time2] = get_consumption(inst1, inst2, loadingTime, time1, time2, time2, time2) #create depot-specific edge
                                 
                            else:
                                LegNet[vessel, inst1, time1, inst2, time2 + serviceTime + loadingTime] = get_consumption(inst1, inst2, loadingTime, time1 + loadingTime, time2, time2, time2 + serviceTime) #create edge


count = 0

for vessel in Vessels:
    for time1 in range(AvaliableTime[vessel],AvaliableTime[vessel]+167,1):
#        count+=1
#        print("\rGenerating variables: %d%% "%math.ceil((count/(Vessels.size + 168))*100/5.8), end="\r", flush = True)
        for inst1 in InstallationNums:
            if time_to_return(vessel, inst1, time1):
                if inst1 == 0:
                    if  time1 % 24 == 0 and time1 < 143 + AvaliableTime[vessel]: #We define 8 o clock the first day as the first time index
                        build_arcs(vessel, time1, inst1, 8)
                else: 
                    if (np.size(np.nonzero(LegNet[vessel,:, :, inst1, time1])) > 0 ):
                        build_arcs(vessel, time1, inst1, 0)


print("\n\nNetwork generation successful!")
print("------------------------------------------------")
print("number of edges generated:       ", np.size(np.nonzero(LegNet)))
print("number of total potential edges: ", np.size(LegNet))
print("------------------------------------------------\n")
print("Plotting graph....")

plot.draw_routes(LegNet,InstallationNums,Times,Vessels)

for v in Vessels:
    for i in InstallationNums:
        for t in Times:
            for j in InstallationNums:
                for tau in Times:
                    if LegNet[v,i,t,j,tau] != 0:
                        print(v,i,t,j,tau)
                
                        
    
print("-------------- OPTIMIZING MODEL ----------------\n")

try:
    om.solve(InstallationNums, Vessels, Times, LegNet)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error: Mogadishu')
    