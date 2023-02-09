from second_commit import *
import mesa
import matplotlib.pyplot as plt
import geopandas as gpd
from geopandas import GeoDataFrame, GeoSeries



evacuation = Evacuation(buildings)


for i in range(1):
    evacuation.step()
    

    
    

buildings.plot()
plt.show()

