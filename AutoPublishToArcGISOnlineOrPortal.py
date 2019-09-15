import arcpy
import os, sys
from arcgis.gis import GIS

### Start setting variables
#Set the path to the project
prjPath = r"D:\Data\Records\Samuel\Test\Test.aprx"
prj = arcpy.mp.ArcGISProject(prjPath)
portal = "https://www.arcgis.com" # Can also reference a local portal
user = "username"
password = "P@ssword"
print("Connecting to {}".format(portal))
gis = GIS(portal, user, password)

for m in prj.listMaps():
    for lyr in m.listLayers():
        print(lyr)
        sd_fs_name = lyr.name
        ### End setting variables
        # Local paths to create temporary content
        relPath = r"D:\Data\Records\Samuel\Sd_files"
        sddraft = os.path.join(relPath, str(lyr) + ".sddraft")
        print(sddraft)
        sd = os.path.join(relPath, str(lyr) + ".sd")
        print(sd)
        # Create a new SDDraft and stage to SD
        print("Creating SD file")
        arcpy.env.overwriteOutput = True
        arcpy.mp.CreateWebLayerSDDraft(lyr, sddraft, sd_fs_name, 'MY_HOSTED_SERVICES', 'FEATURE_ACCESS', True, True)
        arcpy.StageService_server(sddraft, sd)
        search_result = gis.content.search("{} AND owner: {}".format(sd_fs_name,user), item_type="Service Definition")
        print(search_result)
        if len(search_result) > 0:
            for item in search_result:
                item.delete()
                print("Deleted existing " + ": ", item)
        item_properties = {"type": "Service Definition", "title" : str(lyr.name)}
        # Find the SD, update it, publish /w overwrite and set sharing and metadata
        print("Publishing feature service…")
        sdItem=gis.content.add(item_properties,sd)
        fs = sdItem.publish(overwrite=True)
        print("Finished publishing: {} – ID: {}".format(fs.title, fs.id))
        fs.move("Samuel")
#if shrOrg or shrEveryone or shrGroups:
        print("Setting sharing options…")
        fs.share(org=True, groups="21aa2f0052aa4f78ab2ac98153cc324a")
        print("Shared with " + str(fs.shared_with))
        update_dict={'capabilities':'Query,Extract'}
        from arcgis.features import FeatureLayerCollection
        flc=FeatureLayerCollection.fromitem(fs)
        flc.manager.update_definition(update_dict)
        print(lyr.name +" enabled for export")