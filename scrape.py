import requests # for pulling XML
import smtplib # for sending emails
from time import sleep
from numpy import random
import pandas as pd


def alert(row): # send email with information in row
    ADDR = "dummymattho@gmail.com" # don't steal my dummy account
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
    courses = pd.read_csv('courses.csv', dtype={'Course': str,'CRN': str}) # read from csv

    for index, row in courses.iterrows():

        a = requests.get('http://courses.illinois.edu/cisapp/explorer/schedule/2017/spring/'
                         + row['Dept'] +'/' + row['Course'] + '/' + row['CRN']+'.xml', 
                         auth=()).text # pull XML

        if u'Closed' in a: # check XML for 'Closed' status
            print(row['Dept'] +' ' + row['Course'] + ': closed')
            courses.loc[row.name,'Open'] = 0
        elif (u'null' in a) or (u'Error' in a):
            print(row['Dept'] +' ' + row['Course'] + ': XML RETRIEVAL ERROR')
        else:
            print(row['Dept'] +' ' + row['Course'] + ': OPEN')
            
            if row['Open'] == 0: # if class was already open, don't send another email
                alert(row)
            courses.loc[row.name,'Open'] = 1
    
    
    courses.to_csv('courses.csv',index=False) # update 'Open' status in csv
    
    sleep(15*random.poisson(20)) # wait a random amount of time; approx 5 min
