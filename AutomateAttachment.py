import sys
import arcpy
import os

arcpy.env.overwriteOutput = True
in_feature_class = r"D:\Data\Alisha\TemplateData (1)\Test.GDB\us_lakes"
folder = r"D:\Attach_test"
out_path=r"D:\Data\Alisha\TemplateData (1)\Test.GDB"
match_table = r"D:\Data\Alisha\TemplateData (1)\Test.GDB\matchtable"
path= str("D:\Attach_test\test.pdf")
os.listdir(folder)
arcpy.EnableAttachments_management(in_feature_class)
arcpy.CreateTable_management(out_path, "attach")
in_table= r"D:\Data\Alisha\TemplateData (1)\Test.GDB\attach"
arcpy.AddField_management(in_table, "Attach_field", "TEXT")
with arcpy.da.InsertCursor(in_table, ['OBJECTID', 'Attach_field']) as cursor:
    for filePDF in os.listdir(folder):
        fname, fExt = os.path.splitext(filePDF)
        print("Done")
        if fExt.upper() == '.PDF':
            arcpy.AddMessage(filePDF)
            cursor.insertRow([fName,os.path.join(folder,filePDF)])
arcpy.AddAttachments_management(in_feature_class, "ObjectID", in_table, "ObjectID", "Attach_field")

