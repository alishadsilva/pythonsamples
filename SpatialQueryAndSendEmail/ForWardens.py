import json
import arcpy
import arcgis
import urllib
from arcgis.gis import GIS
from arcgis.mapping import WebMap
import requests, datetime, time, smtplib, urllib3,os
from datetime import timedelta

gis = GIS("https://www.arcgis.com", "AlishaD_ess", "ESRI@1994")
targetMapItem = gis.content.get('ff87c91da4254455849500a72fa2dd2d')

polygon_fs = arcpy.FeatureSet()
polygon_fs.load("https://services.arcgis.com/Wl7Y1m92PbjtJs5n/arcgis/rest/services/Thane_Mapboun/FeatureServer/5/query?where=1%3D1&outFields=*&returnGeometry=true&f=json")


base_URL = "https://services.arcgis.com/Wl7Y1m92PbjtJs5n/arcgis/rest/services/Thane_Mapboun/FeatureServer/replace"
layer_list=[0,1,2,3,4]
for x in layer_list:
    point_url= urllib.parse.urljoin(base_URL,str(x)+'/query?where=1%3D1&outFields=*&returnGeometry=true&f=json')
    point_fs = arcpy.FeatureSet()
    point_fs.load(point_url)
    print(point_url)

    names=[]
    ward_nums=[]
    Email=[]
    with arcpy.da.SearchCursor(polygon_fs,['SHAPE@','Ward_Name','Ward_No','Email']) as cursor1:
        for row in cursor1:
            row1=row[0]
            name=row[1]
            num=row[2]
            Email.append(row[3])
            with arcpy.da.SearchCursor(point_fs,['SHAPE@']) as cursor2:
                for row in cursor2:
                    if row[0].within(row1):
                        names.append(name)
                        ward_nums.append(num)
                        break
    fs_animals= targetMapItem.layers[int(x)]
    test=[]
    fl_animals=fs_animals.query()
    all_features = fl_animals.features
    print(names)
    print(ward_nums)
    for a,b,c in zip(all_features,names,ward_nums):
        a.attributes['Ward_name']=b
        a.attributes['Ward_num']=c
        test.append(a)
    fs_animals.edit_features(updates= test)
    uniqueID = 'OBJECTID'           # i.e. OBJECTID
    dateField = 'CreationDate'      # Date field to query
    ward='Ward_name'
    #Email='Email'
    hoursValue = 3                  # Number of hours to check when a feature was added

    # Create empty list for uniqueIDs
    oidList = []
    for name1 in names:
        query= "Ward_name="+"\'"+str(name1)+"\'"
        # Send the POST request:
        URL= urllib.parse.urljoin(base_URL,str(x)+'/query')
        payload = {'f': 'pjson', 'where': query, 'outfields' : '{0},{1},{2}'.format(uniqueID, dateField,ward), 'returnGeometry' : 'false'}
        data=requests.get(URL,params=payload).json()
        # Loop through the features in the extracted JSON:
        for feat in data['features']:
            createDate = feat['attributes'][dateField]
            createDate = int(str(createDate)[0:-3])
            t = datetime.datetime.now() - timedelta(hours=hoursValue)
            t = time.mktime(t.timetuple())
            if createDate > t:
                oidList.append(feat['attributes'][uniqueID])
                print(oidList)
                continue
            # Email Info to send the email
                # Set the email ID:
    for email in Email:
        print(email)
        fromEmail = 'thanamunicipalcorp@gmail.com' # Email sender
        toEmail= email
        smtpServer = 'smtp.gmail.com'
        portNumber = 465                 # SMTP Server port
        FROM = fromEmail
        TO = [toEmail]
        SUBJECT = 'New Issue Reported'
        TEXT = "\n Hello, \n \n New issues with numbers {0} were reported for your department. \n \n Regrads, \n Muncipality Team".format(oidList)
        message = """From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
        gmail_user='abc@gmail.com' #Your emailid
        gmail_password='P@ssword' #your password
        # # If new features exist, send email
        if len(oidList) > 0:
            smtpObj = smtplib.SMTP_SSL(host=smtpServer, port=portNumber)
            smtpObj.login(gmail_user, gmail_password)
            smtpObj.sendmail(FROM, TO, message)
            print("Successfully sent email" )
            smtpObj.quit()
            break
        else:
            print("No email sent")
            break
    test.clear()
    names.clear()
    oidList.clear()
