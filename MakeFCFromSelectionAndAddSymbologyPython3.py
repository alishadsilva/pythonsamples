import arcpy, os, sys

arcpy.env.workspace = r"D:\Data\Alisha\TemplateData (1)\States.gdb"
in_layer=r"D:\Data\Alisha\TemplateData (1)\States.gdb\states" #Path to the input feature class
out_feature_class=r"D:\Data\Alisha\TemplateData (1)\States.gdb\selected" #Path to the output feature class
# p = arcpy.mp.ArcGISProject(r"Path to the project aprx file here") #If you are using it from Pro IDLE.
p = arcpy.mp.ArcGISProject("CURRENT") #If you are using the script within the project in the Python Analysis window
m = p.listMaps('Map')[0]
print("Copy features and Add data")
FeatureClass= arcpy.SelectLayerByAttribute_management(in_layer, "NEW_SELECTION", "'AREA'>100000")
arcpy.CopyFeatures_management(FeatureClass, out_feature_class)
# m.addDataFromPath(r"path to the copied data") #Use this if executing the script from IDLE
l = m.listLayers('selected')[0] #Enter the layer name here
sym = l.symbology

if hasattr(sym, 'renderer'):
  # if sym.renderer.type == 'SimpleRenderer':
    sym.updateRenderer('GraduatedColorsRenderer')
    sym.renderer.classificationField = 'Shape_Area'
    sym.renderer.breakCount = 10
    sym.renderer.colorRamp = p.listColorRamps('Cyan to Purple')[0] 
    l.symbology = sym

p.save() #If you want to save the symbology in the current project
# p.saveACopy(r"Path to the new project file you want to save") If you want to create a copy of the project
