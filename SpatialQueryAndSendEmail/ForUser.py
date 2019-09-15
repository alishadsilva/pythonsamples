# for python 3.5 onwards and for all layers in the feature service
import requests, json, urllib, datetime, time, smtplib, urllib3,os
from datetime import timedelta

# Set the parameters:
base_URL = 'https://services.arcgis.com/Wl7Y1m92PbjtJs5n/arcgis/rest/services/ThaneMap/FeatureServer/replace'
layer_list=[0,1,2,3,4]
for x in layer_list:
    URL= urllib.parse.urljoin(base_URL,str(x)+'/query')
    uniqueID = 'OBJECTID'           # i.e. OBJECTID
    dateField = 'CreationDate' 
    Email='Email'     # Date field to query
    hoursValue = 3                  # Number of hours to check when a feature was added
    # Set the email ID:
    fromEmail = 'abc@gmail.com' # Email sender 
    #toEmail = 'alishadsilva98@gmail.com'   # Email receiver
    smtpServer = 'smtp.gmail.com'    # SMPT Server Name
    portNumber = 465                 # SMTP Server port
    # Create empty list for uniqueIDs
    oidList = []
    # Send the POST request:
    payload = {'f': 'pjson', 'where': "1=1", 'outfields' : '{0}, {1},{2}'.format(uniqueID, dateField, Email), 'returnGeometry' : 'false'}
    r=requests.post(URL,params=payload)
    data=r.json()
    print(data)
    # Loop through the features in the extracted JSON:
    for feat in data['features']:
        createDate = feat['attributes'][dateField]
        email=feat['attributes'][Email]
        createDate = int(str(createDate)[0:-3])
        t = datetime.datetime.now() - timedelta(hours=hoursValue)
        t = time.mktime(t.timetuple())
        if createDate > t:
            oidList.append(feat['attributes'][uniqueID])
            print(oidList)
        # Email Info to send the email
        #for e in email:
            #print(e)
        FROM = fromEmail
        TO = [email]        
        SUBJECT = 'New Features Added'
        TEXT = "Features with {0}s {1} were added.".format(uniqueID, oidList)
        message = """From: %s
        To: %s
        Subject: %s

        %s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        gmail_user='abc@gmail.com' #Your emailid
        gmail_password='XXXX' #your password
        # # If new features exist, send email
        if len(oidList) > 0:
            smtpObj = smtplib.SMTP_SSL(host=smtpServer, port=portNumber)
            smtpObj.login(gmail_user, gmail_password)
            smtpObj.sendmail(FROM, TO, message)
            print("Successfully sent email" )
            smtpObj.quit()




