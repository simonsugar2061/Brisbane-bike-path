# Visualisation of bike paths in Brisbane

This project visualises bike paths in Brisbane using open data obtained from Brisbane Council. The source data is obtained from Brisbane Council open data [website] (https://data.brisbane.qld.gov.au/data/dataset/bikeways). The geolocation data of the bike paths is not in a latitude and longitude format, so python is used to convert the coordinates in the source data to latitude and longitude format, which can be directly read by Tableau.

## Converting coordinates

The source data is packed in a zip file, which contains a set of files. The two that are used in this project are:
* AIM_BIKEWAY_SECTIONS_2015.shp
* AIM_BIKEWAY_SECTIONS_2015.prj

The shape file with the extension .shp stores the coordinates that defines the bike paths. The projection file with the extension .prj contains the information on what projected coordinate system that is used for the coordinates in the shape file. What I did is firstly extract the projected coordinates in the shape file, then convert the projected coordinates back to the longitude and latitude format based on the projected coordinate system information stored in the projection file.

Two python packages, **pyshp** and **pyproj**, are used for the coordinate conversion.

#### Extracting coordinates from shapefile

A sample code for extracting a pari of coordinates for a particular bike path:

```python
import shapefile as sf
region = sf.Reader('AIM_BIKEWAY_SECTIONS_2015.shp')
geomet = region.shapeRecords()
geo = geomet[0]
coords = geo.shape.points
x = coords[0][0]
y = coords[0][1]
```

#### Converting coordinates

First, I checked which projected coordinate system is being used by checking the projection file AIM_BIKEWAY_SECTIONS_2015.prj. The particular information in the projection file is the coordinate system name **GDA_1994_MGA_Zone_56**. Using this name, I got the associated EPSG code, which is EPSG: 28356. I did the lookup [here] (http://prj2epsg.org/search) and confirmed it [here] (http://spatialreference.org/ref/epsg/gda94-mga-zone-56/) and [here] (http://www.supermap.com/EN/online/iServer%20Java%206R/Appendix/CoordSystem/PCS_Code.htm).

A sample code for the coordinate conversion:

```python
import pyproj
coord_proj = pyproj.Proj(init = 'EPSG:28356')
lon, lat = coord_proj(x,y,inverse = True)
```

The two variabls, `lon` and `lat` are longitude and latitude values of the input coordinates.

## Exporting

All the longitude and latitude coordinates and other corresponding attributes are written to a CSV file for Tableau.

## Visualisation

The visualisation is completed in Tableau. The CSV file is used for the visualisation. Instead of only plotting coordinate points on the map, this time lines need to be plotted in order to represent the paths. I followed the tutorial [here] (https://public.tableau.com/s/blog/2015/07/taking-path-function). In order to correctly to plot the paths, the data in the CSV file needs to be presented in a paritular way, which is well demonstrated in the tutorial.

The completed visualisation can be found [here] (https://public.tableau.com/profile/simon.su#!/vizhome/QldBikePathv1/BrisbaneBikePathMap).

## Note
Other useful articles/tutorials/documentations I used in this project are:
* <http://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/>
* <http://jswhit.github.io/pyproj/pyproj-module.html#transform>
* <http://geoinformaticstutorial.blogspot.com.au/2014/06/converting-coordinates-between-map.html>

