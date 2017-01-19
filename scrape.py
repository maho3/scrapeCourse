import requests
import smtplib
from time import sleep
from numpy import random
import pandas as pd


def alert(row):
    ADDR = "dummymattho@gmail.com"
    passw = "dummyaccount"

    content = (row['Dept']+ ' ' + row['Course'] + ', CRN: ' + row['CRN'] + ', is available \n\nIt may not be immediately apparent on Course Explorer, as that site only refreshes every 20 min.')
    
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(ADDR,passw)
    mail.sendmail(ADDR, row['Email'],content) 
    mail.close()
    print("Sent update to:")
    print row

while True:
    courses = pd.read_csv('courses.csv', dtype={'Course': str,'CRN': str})

    for index, row in courses.iterrows():

        a = requests.get('http://courses.illinois.edu/cisapp/explorer/schedule/2017/spring/'
                         + row['Dept'] +'/' + row['Course'] + '/' + row['CRN']+'.xml', 
                         auth=()).text

        if u'Closed' in a:
            print(row['Dept'] +' ' + row['Course'] + ': closed')
            courses.loc[row.name,'Open'] = 0
        elif (u'null' in a) or (u'Error' in a):
            print(row['Dept'] +' ' + row['Course'] + ': XML RETRIEVAL ERROR')
        else:
            print(row['Dept'] +' ' + row['Course'] + ': OPEN')
            
            if row['Open'] == 0:
                alert(row)
            courses.loc[row.name,'Open'] = 1
    
    
    courses.to_csv('courses.csv',index=False)
    sleep(15*random.poisson(20))
