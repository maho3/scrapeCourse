# scrapeCourse
Python script to probe class availabilities in the University of Illinois system.

## How to Run
#### Open scrape.py in a standard text editor. In the definition of the alert() function, change the values of ADDR and passw to the email account information you want to forward notifications from.
```
def alert(row): # send email with information in row
    ADDR = "EMAIL_HERE@EMAIL.com" # don't steal my dummy account
    passw = "PASSWORD_HERE"
    ...
```
 - If you are using a Gmail account. You will need to allow access for less secure apps. You can do that at [here](https://www.google.com/settings/security/lesssecureapps). 

#### Open courses.csv in Excel or an equivalent spreadsheet editor. Adjust row values to reflect the courses you want to check. This should be self-explanatory.
 - MAKE SURE TO SAVE AS A CSV FILE.

#### Run scrape.py in terminal with the command:
```
python scrape.py
```

#### Allow it to run indefinitely.
