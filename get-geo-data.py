# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 22:00:26 2016

@author: Simon
"""

import shapefile as sf
import csv
import pyproj

region = sf.Reader('AIM_BIKEWAY_SECTIONS_2015.shp')
geomet = region.shapeRecords()

# prepare for geographical coordinate system conversion
coord_proj = pyproj.Proj(init = 'EPSG:28356')

# prepare CSV file
headers = ['PathID', 'Path Order', 'Lat', 'Long', 'Street', 'Suburb', 'Material',\
 'Traffic Type', 'Path Length']

rows = []

for geo in geomet:
    coords = geo.shape.points
    attrib = geo.record
    
    path_id = attrib[0]
    street = attrib[7]
    suburb = attrib[8]
    material = attrib[3]
    traffic_type = attrib[2]
    path_leng = attrib[11]
    
    count = 1
    for coord in coords:
        x = coord[0]
        y = coord[1]
        
        # convert
        long, lat = coord_proj(x,y,inverse = True)
        
        row = dict()
        row['PathID'] = path_id
        row['Path Order'] = count
        row['Lat'] = lat
        row['Long'] = long
        row['Street'] = street
        row['Suburb'] = suburb
        row['Material'] = material
        row['Traffic Type'] = traffic_type
        row['Path Length'] = path_leng
        rows.append(row)
        count += 1
        

# Write CSV file
with open('bike-path.csv', 'w') as csvfile:
    fieldnames = headers
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in rows:
        writer.writerow(row)