import mesa 
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from geopandas import GeoSeries, GeoDataFrame
import random
from mesa.time import RandomActivation
from shapely.geometry import Point
import shapely
import matplotlib.pyplot as plt
import numpy as np
from mesa.datacollection import DataCollector



buildings = gpd.read_file('buildings.shp')
buildings = buildings.drop(columns = ['FID'])


class Person(mesa.Agent):
    def __init__(self, unique_id, model, home_polygon, move_range):
        super().__init__(unique_id, model)
        self.home_polygon = home_polygon
        self.current_location = home_polygon.centroid     
        self.unique_id = unique_id
        self.move_range = move_range
    
    def agent_portrayal(self):
        x, y = self.current_location.x, self.current_location.y
        if self.home_polygon.contains(Point(x, y)): 
            color = 'yellow'
        else:
            color = 'red'
        portrayal = {
            'shape' : 'circle',
            'layer' : 1,
            'r' : 10,
            'color' : color,
            'x' : x,
            'y' : y
        }
        return portrayal

    def move(self):
    
        dx = random.randint(-self.move_range, self.move_range)
        dy = random.randint(-self.move_range, self.move_range)
        update_location = Point(self.current_location.x + dx, self.current_location.y + dy)
        if self.home_polygon.contains(update_location):
            self.current_location = update_location
            print (update_location, self.current_location, self.home_polygon)
        #print ('UPDate: ',update_location, 'Current :', self.current_location)
        
    def step(self):
        self.move()
        self.agent_portrayal()
        
    
class Evacuation(mesa.Model):
    
    def __init__(self, buildings, FID = None):
        self.buildings = buildings
        self.schedule = RandomActivation(self)
        self.FID = FID
        for i, row in self.buildings.iterrows():
            polygon = row['geometry']
            
            person = Person(i, self, polygon, move_range=2)
            
            self.schedule.add(person)

    def step(self):
        self.schedule.step()
        current_position = []
        for agent in evacuation.schedule.agents: 
            current_position.append(agent.current_location)
            agent.step()
            

    def plot_model(self):

        fig, ax = plt.subplots()
        ax.clear()
        # Plot the polygon
        buildings.plot(ax=ax)

        # Plot the persons
        x = []
        y = []
        for person in evacuation.schedule.agents:
            portrayal = person.agent_portrayal()
            x.append(portrayal['x'])
            y.append(portrayal['y'])
        scat = ax.scatter(x, y, c=[portrayal['color'] for portrayal in [person.agent_portrayal() for person in evacuation.schedule.agents]], s=[portrayal['r'] for portrayal in [person.agent_portrayal() for person in evacuation.schedule.agents]])
        plt.pause(0.1)
        scat.set_offsets(np.c_[x, y])

evacuation = Evacuation(buildings)

for i in range(10):
    evacuation.step() 
    evacuation.plot_model()
