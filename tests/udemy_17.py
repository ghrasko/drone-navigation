import osmnx as ox
import matplotlib.pyplot as plt

district = ox.geocode_to_gdf("1st district, Budapest")
print(district.plot())