# Description
# This script copies selected features from source feature class to the target feature class
# And applies symbology to the target feature class 


import arcpy

#Set the environment workspace
arcpy.env.workspace = r"D:\Data\Alisha\TemplateData (1)\States.gdb"
arcpy.env.overwriteOutput = True

#Define the variables
in_layer=r"D:\Data\Alisha\TemplateData (1)\States.gdb\states"
out_feature_class=r"D:\Data\Alisha\TemplateData (1)\States.gdb\selected4"
out_layer_file=r"D:\Data\Records\Bruce_Sym\selected1.lyr" #Created by exporting a layer from ArcMap with the required symbology

FeatureLayer= arcpy.MakeFeatureLayer_management(in_layer, "in_layer")
NewLayer= arcpy.SelectLayerByAttribute_management("in_layer", "NEW_SELECTION", '"OBJECTID">25')
arcpy.CopyFeatures_management(NewLayer, out_feature_class)
p2=arcpy.mapping.MapDocument(r"D:\Data\Records\Bruce_Sym\Test.mxd")
m2 = arcpy.mapping.ListDataFrames(p2)[0] #Name of the Dataframe
newlayer=arcpy.mapping.Layer(out_feature_class)
arcpy.mapping.AddLayer(m2, newlayer,"BOTTOM")
l2 = arcpy.mapping.ListLayers(p2,'selected4',m2)[0] #Name of the feature layer you need to assign symbology on
arcpy.ApplySymbologyFromLayer_management(l2,out_layer_file)
print "Symbology applied"

p2.save()
print "Project2 Saved"
