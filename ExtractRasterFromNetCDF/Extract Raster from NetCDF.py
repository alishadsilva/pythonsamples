import os
import arcpy
from datetime import datetime

# PArameters required on the Tool interface
Workspace= arcpy.GetParameterAsText(0)
InNetCDF=arcpy.GetParameterAsText(1)
Output_gdb=arcpy.GetParameterAsText(2)
variable=arcpy.GetParameterAsText(3)
Projection=arcpy.GetParameterAsText(4)

# Setting the workspace
arcpy.env.workspace = Workspace

# Set variables

x_dimension="longitude"
y_dimension="latitude"

# Convert the NetCDF to a layer
Input_NetCDF_layer=arcpy.MakeNetCDFRasterLayer_md(InNetCDF, variable, x_dimension, y_dimension, out_raster_layer="layer", band_dimension="",dimension_values="" , value_selection_method="BY_VALUE")

# Get the NetCDF properties
ncFP = arcpy.NetCDFFileProperties(InNetCDF)  
ncDim = ncFP.getDimensions()
dimension_values=[]
count = 1
arcpy.AddMessage("Starting to slice the file")

# Loop through the dates to extract individual rasters
for dim in ncDim:
	if dim=='time':
		top =  ncFP.getDimensionSize(dim)
		for i in range(0,top):
			value=ncFP.getDimensionValue(dim,i)
			name_date=value.replace('-', '_') #'-' is the date separator used in my machine. Change your machine date format to hyphen separator or replace '-' with your machine date separator.
			temp_dim_val= ["time", value]
			dimension_values.append(temp_dim_val)
			while count<=len(dimension_values):
				Output_Raster1 = Output_gdb + os.sep + "NetCDF_Raster_"+str(name_date)
				valueSelectionMethod = ""
				in_raster=arcpy.SelectByDimension_md(Input_NetCDF_layer, dimension_values , valueSelectionMethod)
				out_raster=arcpy.CopyRaster_management(Input_NetCDF_layer, Output_Raster1, config_keyword="", background_value="", nodata_value="0,000000e+00", onebit_to_eightbit="NONE", colormap_to_RGB="NONE", pixel_type="", scale_pixel_value="NONE", RGB_to_Colormap="NONE", format="Cloud Optimized GeoTIFF", transform="NONE")
				count +=1
				arcpy.AddMessage("Raster for " +str(value) +" exported")
				arcpy.DefineProjection_management(out_raster, Projection)
				arcpy.AddMessage("Projection for "+str(value)+ " raster assigned")