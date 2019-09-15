import arcpy
from arcpy import env

mxd = arcpy.mapping.MapDocument("Current")
df = arcpy.mapping.ListDataFrames(mxd,"")[0]
for lyr in arcpy.mapping.ListLayers(mxd, "",df):
	if lyr.name == 'CityLimit':
		SymbologyLyr = r'C:\Versaterm\MXDforSymbols\LYR_files\FPD_CAD_Regular\Parks.lyr'
		arcpy.ApplySymbologyFromLayer_management(lyr, SymbologyLyr)
		lyr.minScale = 256000
		lyr.maxScale = 500
		
	if lyr.name == 'PoliceZones':
		SymbologyLyr = r'C:\Versaterm\MXDforSymbols\LYR_files\FPD_CAD_Regular\Police Zones.lyr'
		arcpy.ApplySymbologyFromLayer_management(lyr, SymbologyLyr)
		lyr.minScale = 64000
		lyr.maxScale = 500
