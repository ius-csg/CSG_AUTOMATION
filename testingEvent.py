import mysql.connector
import os
import dotenv
def insertData(): #this calls collecting
    try:
        conn = mysql.connector.connect(host="192.168.1.101",port=3306, 
                        user=os.getenv("SQL_USERNAME"), 
                        passwd=os.getenv("SQL_PW"), 
                        database="EVENT")
        c = conn.cursor()
        c.execute('''
        INSERT INTO EVENTS (id,name,description,start_datetime, end_datetime, location, type, created_at, updated_at)
        VALUES
        (id,"Game Night","Our first automatic game night","2019-09-25 08:20","2019-09-25 09:20:00","NS 111A","game night",CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())
        ''')                  
        conn.commit()
        print("Successfully sent data")
        conn.close()
    except Exception as e:
        print(e)          


insertData()