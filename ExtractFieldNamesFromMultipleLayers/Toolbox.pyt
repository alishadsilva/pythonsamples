import arcpy
from CombinedLR import CombinedTool

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""
        self.category="Test123"
        # List of tool classes associated with this toolbox
        self.tools = [CombinedTool]



