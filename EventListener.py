import mysql.connector
from datetime import datetime  
from datetime import timedelta 
from mysql.connector import Error
from dotenv import load_dotenv
import os
import smtplib
load_dotenv()
gmail_user = os.getenv("GMAIL_USERNAME")
gmail_password = os.getenv("GMAIL_PW")
def sendMail(eventName, eventStart, eventEnd, eventDescription="", eventLocation="", eventDays="1 day"): 
    print(eventName)
    print(eventStart)
    print(eventEnd)
    print(eventDescription)
    print(eventLocation)
    print(eventDays)       
    sent_from = gmail_user
    to = ['zbouvier@iu.edu'] #attendees
    subject = 'Automated Email Reminder for %s' % eventName #meeting name
    body = 'This is an automated reminder from the IUS Computer Security Group that the event ' + eventName + ' is happening between the times of ' + str(eventStart) + ' and ' + str(eventEnd) + '. as a reminder, the event\'s description is '+ eventDescription +'and it is located at ' +eventLocation+ '. This means it is '+eventDays+' away'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except Exception as e:
        print(e)
def getCurrentEvents():
    try:
        connection = mysql.connector.connect(host=os.getenv("SQL_IP"),port=3306, 
                                            database=os.getenv("SQL_DATABASE"),
                                            user=os.getenv("SQL_USERNAME"),
                                            password=os.getenv("SQL_PW"))

        sql_select_Query = "select name, start_datetime, end_datetime, description, location from EVENTS WHERE start_datetime >= DATE_ADD(CURRENT_TIMESTAMP(), INTERVAL -1 DAY)"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for row in records:
            startDateTime = row[1]
            twoWeeksBefore = startDateTime - timedelta(days=14)
            oneMonthBefore = startDateTime - timedelta(days=30)
            oneDayBefore = startDateTime - timedelta(days=1)
            #print(startDateTime)
            #print(datetime.now())
            if(twoWeeksBefore <= datetime.now() and twoWeeksBefore >= datetime.now() - timedelta(minutes=50)):
                sendMail(row[0], row[1], row[2], row[3], row[4], "14 days")
            elif(oneMonthBefore <= datetime.now() and oneMonthBefore >= datetime.now() - timedelta(minutes=50)):
                sendMail(row[0], row[1], row[2], row[3], row[4], "1 month")
            elif(oneDayBefore <= datetime.now() and oneDayBefore >= datetime.now() - timedelta(minutes=50)):
                sendMail(row[0], row[1], row[2], row[3], row[4])
                #send event warning email
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            #print("MySQL connection is closed")

getCurrentEvents()
#sendMail()