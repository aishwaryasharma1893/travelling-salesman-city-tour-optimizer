# -*- coding: utf-8 -*-
"""
Created on Sat May 17 22:51:53 2025

@author: DELL
"""

import csv
import math
from geojson import Feature, FeatureCollection, LineString, dump

def calculate_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return 6371 * 2 * math.asin(math.sqrt(a))

def main():
    places = []
    with open('places.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            places.append({
                'name': row['Name'],
                'lat': float(row['Lat']),
                'lon': float(row['Lon'])
            })
    
    n = len(places)
    dist_matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i][j] = calculate_distance(
                    places[i]['lat'], places[i]['lon'],
                    places[j]['lat'], places[j]['lon'])
    
    visited = [0]
    unvisited = set(range(1, n))
    total_distance = 0.0
    
    while unvisited:
        last = visited[-1]
        nearest = min(unvisited, key=lambda x: dist_matrix[last][x])
        total_distance += dist_matrix[last][nearest]
        visited.append(nearest)
        unvisited.remove(nearest)
    
    total_distance += dist_matrix[visited[-1]][visited[0]]
    visited.append(visited[0])
    
    print("Optimal tour (returns to start):")
    for i, idx in enumerate(visited):
        print(f"{i+1}) {places[idx]['name']}")
    print(f"Total distance: {total_distance:.1f} km")
    
    coordinates = [[places[idx]['lon'], places[idx]['lat']] for idx in visited]
    line_string = LineString(coordinates)
    feature = Feature(geometry=line_string)
    feature_collection = FeatureCollection([feature])
    
    with open('route.geojson', 'w') as f:
        dump(feature_collection, f)
    print("Route written to route.geojson")

if __name__ == "__main__":
    main()