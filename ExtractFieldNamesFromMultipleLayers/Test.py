from CombinedLR import CombinedTool

a = CombinedTool()
parameters = a.getParameterInfo()
parameters[0].value = [[r"C:\projects\turbo-py\Test.gdb\Transmission\PipeSegment"]]
a.execute(parameters,None)