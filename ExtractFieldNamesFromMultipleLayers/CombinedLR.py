import arcpy

class CombinedTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "CombinedLRTool"
        self.description = "CombinedTool"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        in_tables = arcpy.Parameter(
            displayName="Input Layers",
            name="InputLayers",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        in_seg = arcpy.Parameter(
            displayName="Seg Layers",
            name="in_seg",
            datatype="GPValueTable",
            # parameterType="Optional",
            direction="Input")
        in_seg.columns = [["GPTableView", "Table"]]
        # in_seg.filters[1].type='ValueList'
        # in_seg.filters[1].list=["<test list>"]

        testvalue = arcpy.Parameter(
            displayName="Test Field",
            name="testvalue",
            datatype="GPString",
            parameterType="Derived",
            direction="Output")

        # testvalue.parameterDependencies = [in_seg.name]
        # testvalue.columns = [['Field', 'Field'], ['String', 'Statistic Type']]
        # testvalue.filters[1].type = 'ValueList'
        params = [in_tables,in_seg,testvalue]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[1].value and parameters[1].altered:
            all_tables_list = parameters[1].value
            number_of_tables = len(all_tables_list)
            i = 0
            fields_list_tmp = []
            for in_table in all_tables_list:
                fields_list_tmp.append([field.name for field in arcpy.Describe(parameters[1].value[i][0]).fields])
                i += 1
            fields_list = list(set([item for sublist in fields_list_tmp for item in sublist]))
            parameters[2].value=str(len(fields_list))
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):


        return

