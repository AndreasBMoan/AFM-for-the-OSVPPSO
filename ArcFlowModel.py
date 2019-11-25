#import numpy as np
import math
import gurobipy as gp
import data as d, optimizationModel as om


#import plot

class model:
    
    # ================== INITIALIZATION ==================
    
    def __init__(self, nInsts, nVessels, nTimes, nVoys, instSetting, weatherSetting):
    
        max_waiting_time = max(d.AvaliableTime)
        
        self.Vessels = d.Vessels[:nVessels]
        self.Insts = d.Insts[:nInsts]
        self.Times = d.Times[:nTimes+max_waiting_time + 1]
        self.Voys = d.Voys[:nVoys]
        
        self.nTimes = nTimes
        self.nInsts = nInsts
        self.nVessels = nVessels
        self.nVoys = nVoys
        
        self.instSetting = instSetting
        self.weatherSetting = weatherSetting
        
        self.ClosingInsts = d.ClosingInsts[instSetting]
        self.Distance = d.Distance[instSetting]
        self.Weather = d.Weather[weatherSetting]
        self.LayTime = d.LayTime[instSetting]
        
        self.name = "Instance-"+str(self.nInsts)+"-"+str(self.nVessels)+"-"+str(self.nTimes)+"-"+str(self.nVoys)+"-"+str(self.instSetting)+"-"+str(self.weatherSetting)
        
        self.fuel_cost = [[[[[0 for tau in self.Times]for inst2 in self.Insts]for t in self.Times]for inst1 in self.Insts]for v in self.Vessels]
        
        self.run_model()



    # ================== RUNNING THE MODEL ==================
    
    def run_model(self):
        
        
        
        print("\n"+self.name+"\n\n================== INITIALIZING MODEL ==================\n")
        print("Model Settings:")
        print("Number of Installations: " + str(self.nInsts))
        print("Number of Vessels:       " + str(self.nVessels))
        print("Number of Time periods:  " + str(self.nTimes))
        print("Installation set used:   " + str(self.instSetting))
        print("Weather settings used:   " + str(self.weatherSetting) + "\n")
        self.build_model()
        print("\nNetwork generation successful!")
        print("------------------------------------------------")
        print("Plotting graph....")
        # plot.draw_routes(self.fuel_cost,self.Insts,self.Times,self.Vessels)
        print("-------------- OPTIMIZING MODEL ----------------\n")
        
        try:
            om.solve(self.fuel_cost, self.Vessels, self.Insts, self.Times, self.Voys, self.instSetting, self.name)
        
        except gp.GurobiError as e:
            print('Error code ' + str(e.errno) + ": " + str(e))
        
        except AttributeError:
            print('Encountered an attribute error: Mogadishu')
        
        
        
        
    # ================== BUILDING THE NETWORK ==================
    
    # ------------------ Deciding what nodes to sail from ------------------
    
    def build_model(self):
        for vessel in self.Vessels:
            
            for time1 in range(d.AvaliableTime[vessel],d.AvaliableTime[vessel]+self.nTimes,1):
                
                for inst1 in self.Insts: 
                    
                    if inst1 == 0:
                        
                        if time1 % 24 == 0 and time1 <= self.nTimes - 24 + d.AvaliableTime[vessel]:
                            self.build_arcs(vessel, time1, inst1, 8) 
                            
                    else: 
                        for tempinst in self.Insts:
                            
                            for temptime in self.Times:
                                
                                if self.fuel_cost[vessel][tempinst][temptime][inst1][time1] != 0:
                                    self.build_arcs(vessel, time1, inst1, 0)
                                    break
                            else:
                                continue
                            break
        
    
    
    
    # ------------------ Deciding what nodes to sail to ------------------
    
    def build_arcs(self, vessel, time1, inst1, loadingTime):
        
        for inst2 in self.Insts: 
            
            if inst2 != inst1: 
                tMin = (math.ceil(self.Distance[inst1][inst2]/d.maxSpeed) + loadingTime + time1)
                tMax = min((math.ceil(self.Distance[inst1][inst2]/d.minSpeed) + loadingTime + time1),self.nTimes + d.AvaliableTime[vessel])
                closedVisit = 0 
                
                for time2 in range(tMax, tMin-1, -1):
                    
                    if ((self.service_not_possible(inst2, time2)) == True) and (closedVisit == 0): 
                        closedVisit = 1 
                        time3 = time2
                        
                        while (self.service_not_possible(inst2, time3)) == True and time3 < self.nTimes + d.AvaliableTime[vessel]-1:
                            time3 += 1 
                            
                        if inst2 == 0: 
                            self.add_arc(vessel, inst1, inst2, time1, time1, time2, time2, time2)
                            
                        else:
                            self.add_arc(vessel, inst1, inst2, time1, time1 + loadingTime, time2 + loadingTime, time3 + loadingTime, time3 + self.LayTime[inst2] + loadingTime) #Create an edge  
                            
                    else: 
                        
                        if (self.service_not_possible(inst2, time2) == False): 
                            
                            if inst2 == 0:
                                self.add_arc(vessel, inst1, inst2, time1, time1, time2, time2, time2)
                                
                            else:
                               self.add_arc(vessel, inst1, inst2, time1, time1 + loadingTime, time2 + loadingTime, time2 + loadingTime, time2 + self.LayTime[inst2] + loadingTime) 
                               
    
   
    # ------------------ Adding arcs to the model ------------------
    
    def add_arc(self, vessel, fromInst, toInst, startTime, depTime, arrTime, serStartTime, finTime):
        
        if math.ceil(self.Distance[toInst][0]/(d.maxSpeed)) + finTime <= d.AvaliableTime[vessel] + self.nTimes:
            
            self.fuel_cost[vessel][fromInst][startTime][toInst][finTime] = (
                    self.depot_consumption(depTime - startTime)
                    + self.sail_consumption(fromInst, toInst, depTime, arrTime, serStartTime)
                    + self.idle_consumption(arrTime, serStartTime)
                    + self.dp_consumption(serStartTime, toInst))
    
    
    
    # ================== HELPING FUNCTIONS ==================
    
    # ------------------ Check weather or not service can be performed ------------------
    
    def service_not_possible(self, inst, time):
        if (self.Weather[time] == 3) or ((self.ClosingInsts[inst] == True) and ((time % 24 < 6) or (time % 24 > 18))) or ((inst == 0) and (time % 24 != 0)):
            return True
        else:
            return False
        
        
        
    # ------------------ Fuel consumption while at supply depot ------------------
    
    def depot_consumption(self, loadingTime):
        return loadingTime * d.depConsumption * d.fuelPrice
        
    
    
    # ------------------ Consumption from propulsion while sailing between platforms ------------------

    def sail_consumption(self, fromInst, toInst, depTime, arrTime, serStartTime): 
        if self.Distance[fromInst][toInst] != 0:
            speed = (arrTime - depTime)/self.Distance[fromInst][toInst]
            consumed = 0
            for time3 in range(depTime, arrTime + 1):
                consumed += 2.7679*(speed + d.SpeedImpact[self.Weather[time3]])**2 - 38.75*(speed + d.SpeedImpact[self.Weather[time3]])+450.71
            return consumed * d.fuelPrice
        else:
            return 0
        
    
    
    # ------------------ Consumption while idling, waiting for the installation to be ready for service ------------------
    
    def idle_consumption(self, arrTime, serStartTime):
        consumed = 0
        if (arrTime != serStartTime):
            for time3 in range(arrTime, serStartTime + 1):
                consumed += d.idleFuelConsume*(1 + self.Weather[time3] * 0.1)
        return consumed * d.fuelPrice
    
    
    
    # ------------------ Consumption while servicing the installation ------------------

    def dp_consumption(self, serStartTime, inst):
        consumed = 0
        if inst == 0:
            return 0
        for time3 in range(serStartTime, serStartTime + self.LayTime[inst] +1):
            consumed += d.dpFuelConsume*(1 + self.Weather[time3] * 0.1)
        return consumed * d.fuelPrice
    
    
    
        