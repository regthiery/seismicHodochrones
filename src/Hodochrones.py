import os
import sys
import math
import matplotlib.pyplot as plt
import numpy as np


#===========================================================================
class Hodochrones:
#===========================================================================

    def __init__(self):
        self.plotsFolderPath = "images/"
        self.scriptsFolderPath = "scripts/"
        self.filename = ""
        self.v1 = 3500
        self.v2 = 5000
        self.h = 20
        self.xmin = None
        self.xmax = None
        self.tmin = None
        self.tmax = None
        self.pxmin = None
        self.pxmax = None
        self.ptmin = None
        self.ptmax = None
        
    def readScript(self,filename):
        self.filename = filename
        
        with open (self.scriptsFolderPath + self.filename + ".txt", "r") as file:
            fileContent = file.read()
        
        lines = fileContent.strip().split("\n")
            
        points = []
        
        for line in lines:
            line = line.strip()
            index = line.find('#')
            if index != -1:
                line = line [:index]
                line.strip()

            if line == '':
                continue
            
            tokens = line.split()
            
            if tokens[0] == 'xmin':
                self.pxmin = float(tokens[1])
            elif tokens[0] == 'xmax':
                self.pxmax = float(tokens[1])
            elif tokens[0] == 'tmin':
                self.ptmin = float(tokens[1])
            elif tokens[0] == 'tmax':
                self.ptmax = float(tokens[1])
            
            else:
                x = float (tokens[0])
                t = float (tokens[1])
                type = tokens[2]
            
                point = {}
                point["x"] = x
                point["t"] = t
                point["type"] = type
            
                points.append (point)
            
        self.points = points    
            
    def analyzeData(self):
        self.directHodochrone = []
        self.reflectedHodochrone = []
        self.refractedHodochrone = []
        self.xmin = 1e8
        self.xmax = -1e8
        self.tmin = 1e8
        self.tmax = -1e8
        
        for point in self.points:
            x = point["x"]
            t = point["t"]
            type = point["type"]
            if self.xmin > x:
                self.xmin = x
            if self.xmax < x:
                self.xmax = x
            if self.tmin > t:
                self.tmin = t
            if self.tmax < t:
                self.tmax = t
            
            if type == 'd':
                point = {}
                point["x"] = x
                point["t"] = t
                self.directHodochrone.append (point)
            elif type == 'r':
                point = {}
                point["x"] = x
                point["t"] = t
                self.reflectedHodochrone.append (point)
            elif type == 'c':
                point = {}
                point["x"] = x
                point["t"] = t
                self.refractedHodochrone.append (point)
                
    def plotData(self):
        x = []
        t = []
        for point in self.directHodochrone:
            x.append(point['x'])
            t.append(point['t'])
        plt.plot (x,t, 'o', markerfacecolor='red', markersize=7)
        x = []
        t = []
        for point in self.reflectedHodochrone:
            x.append(point['x'])
            t.append(point['t'])
        plt.plot (x,t, 'o', markerfacecolor='green', markersize=7)
        x = []
        t = []
        for point in self.refractedHodochrone:
            x.append(point['x'])
            t.append(point['t'])
        plt.plot (x,t, 'o', markerfacecolor='blue', markersize=7)
        
        plt.xlabel('Distance (m)')
        plt.ylabel('Temps (ms)')
        plt.grid(True)
        
        if self.pxmin == None:
            xmin = np.floor(self.xmin) - 1
        else:
            xmin = self.pxmin

        if self.pxmax == None:                
            xmax = np.ceil(self.xmax) + 1
        else:
            xmax = self.pxmax    
            
            
        if self.ptmin == None:
            tmin = np.floor(self.tmin) - 1
        else:
            tmin = self.ptmin
        
        if self.ptmax == None:        
            tmax = np.ceil(self.tmax) + 1
        else:
            tmax = self.ptmax    

            
        plt.xlim(xmin,xmax)
        plt.ylim(tmin,tmax)            

        plt.savefig(self.plotsFolderPath+self.filename+'.png', dpi=300)
        plt.show()
plt.show()
        
        
        
            