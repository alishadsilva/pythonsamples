#!/usr/bin/env python
# coding: utf-8

# In[59]:


import arcpy
import arcgis
from arcgis.gis import GIS
from IPython.display import display
import numpy as np


# In[60]:


gis = GIS("https://www.arcgis.com", "username", "P@ssword")


# In[61]:


from arcgis.mapping import WebMap
targetMapItem = gis.content.get('61450cd256654cf8bd145960376f0923')
targetMapItem


# In[62]:


cities_flayer = targetMapItem.layers[0]


# In[63]:


cities_fset = cities_flayer.query() #querying without any conditions returns all the features


# In[74]:


features_for_update = [] #list containing corrected features
all_features = cities_fset.features


# In[66]:


test=r"D:\Data\Alisha\TemplateData (1)\TemplateData\TemplateData.gdb\USA\cities"


# In[72]:


with arcpy.da.SearchCursor(test, ['OID@','POP1990']) as scursor:
    for row in scursor:
        values=row[1]
        for x in all_features:
            if row[0]==x.attributes['FID']:
                x.attributes['Zip']=int(values)
                features_for_update.append(x)
                print(str(x))
                print("========================================================================")


# In[73]:


cities_flayer.edit_features(updates= features_for_update)


# In[ ]:




