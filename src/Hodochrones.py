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
        self.xdirect = []
        self.tdirect = []
        self.xreflex = []
        self.treflex = []
        self.xrefrac = []
        self.trefrac = []
        
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
                self.xdirect . append(x)
                self.tdirect . append(t)
            elif type == 'r':
                point = {}
                point["x"] = x
                point["t"] = t
                self.reflectedHodochrone.append (point)
                self.xreflex . append(x)
                self.treflex . append(t)
            elif type == 'c':
                point = {}
                point["x"] = x
                point["t"] = t
                self.refractedHodochrone.append (point)
                self.xrefrac . append(x)
                self.trefrac . append(t)
                
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


    def calculateParameters(self):
        self.slopedirect, self.y0direct = np.polyfit(self.xdirect,self.tdirect,1)         
        self.sloperefrac, self.y0refrac = np.polyfit(self.xrefrac,self.trefrac,1)        
        self.v1 = 1000 / self.slopedirect 
        self.v2 = 1000 / self.sloperefrac
        self.ic = math.asin (self.v1/self.v2) * 180 / math.pi
        self.h = self.y0refrac * 0.5e-3 * self.v1 * self.v2 / np.sqrt (self.v2**2 - self.v1**2 )
        
            # tangence onde réfléchie et onde conique
        self.xt = 2 * self.h * self.v1 / np.sqrt (self.v2**2 - self.v1**2 )
        
            # intersection onde conique et onde directe
        self.xb =  2 * self.h * np.sqrt (self.v2 + self.v1) / np.sqrt (self.v2 - self.v1)
        
    def calculateHodochrones(self):
        self.xx = np.linspace (self.pxmin, self.pxmax, 100)   
        self.t1 = self.xx / self.v1
        self.t2 = np.sqrt ( self.xx**2 + 4 * self.h**2 ) / self.v1
        self.t3 = 2 * self.h * np.sqrt (self.v2**2 - self.v1**2) / (self.v1 * self.v2) + self.xx / self.v2 
        self.t1 *= 1000
        self.t2 *= 1000
        self.t3 *= 1000
        
    def plotHodochrones(self):
        plt.plot(self.xx,self.t1, '-', color='red')
        plt.plot(self.xx,self.t2, '-', color='green')
        plt.plot(self.xx,self.t3, '-', color='blue')

    def showDiagram(self):            
        filepath = self.plotsFolderPath+self.filename+'.png'
        if os.path.exists(filepath):
            os.remove(filepath)
        plt.savefig(self.plotsFolderPath+self.filename+'.png', dpi=300)
        plt.show()

    def printData(self):
        i = 1 
        print ("Onde directe")
        for point in self.directHodochrone:
            print("{:>4}) x = {:>6.2f} m, t = {:>6.2f} ms".format(i, point["x"],point["t"]))
            i+=1
        print ("Onde réfléchie")
        for point in self.reflectedHodochrone:
            print("{:>4}) x = {:>6.2f} m, t = {:>6.2f} ms".format(i, point["x"],point["t"]))
            i+=1
        print ("Onde conique")
        for point in self.refractedHodochrone:
            print("{:>4}) x = {:>6.2f} m, t = {:>6.2f} ms".format(i, point["x"],point["t"]))
            i+=1
            
            
        
    def printParameters(self):    
        print("Vitesse v1                              = {:>8.2f} m/s".format(self.v1))
        print("Vitesse v2                              = {:>8.2f} m/s".format(self.v2))
        print("Profondeur réflecteur h                 = {:>8.2f} m".format(self.h))
        print("Angle critique ic                       = {:>8.2f} °".format(self.ic))
        print("Tangence ondes réfléchie et réfractée   = {:>8.2f} m".format(self.xt))
        print("Intersection ondes directe et réfléchie = {:>8.2f} m".format(self.xb))
        
    def run(self,filename):
        self.readScript (filename)
        self.analyzeData()
        self.calculateParameters()
        self.printData()
        self.printParameters()
        self.calculateHodochrones()
        self.plotHodochrones()
        self.plotData()
        self.showDiagram()
        
            