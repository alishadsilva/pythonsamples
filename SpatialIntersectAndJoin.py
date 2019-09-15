import arcpy
count = 0
with arcpy.da.SearchCursor(r"D:\Data\Subho\ESRISUpport.gdb\light", ["wmMapPointName", 'SHAPE@', 'OBJECTID']) as cursor:
    for row in cursor:
        # if (count == 10):
        #     break
        with arcpy.da.SearchCursor(r"D:\Data\Subho\ESRISUpport.gdb\subArea", ["NAME", 'SHAPE@']) as cursor1:
            for row1 in cursor1:
                test=str(row1[0])
                # if (count == 10):
                #     break
                if(row[1].within(row1[1])):
                    # print(row1[0])
                    # print(row[0])
                    print(row[2])
                    count+=1
                    with arcpy.da.UpdateCursor(r"D:\Data\Subho\ESRISUpport.gdb\light", ['wmMapPointName', 'ttt1'],"OBJECTID ="+str(row[2])) as cursor2:
                        for row2 in cursor2:
                            print row2[0]
                            print row1[0]
                            row2[1]=str(row1[0])
                            cursor2.updateRow(row2)  
                        
