import connectionpool as cp
import json
from datetime import datetime
from email.message import EmailMessage
import ssl
import smtplib
import logging
import threading

class dbUrlFunctions:
    def __init__(self,dburl):
        self.dburl = dburl
    def fetchPoolObject(self):
        try:
            self.pool=cp.poolcreate(self.dburl) #pool object
            self.connection = self.pool.get_connection()
            if not isinstance(self.connection,str):
                #valid connection fetched
                self.pool.return_connection(self.connection)
                return self.pool
        except Exception as e:
            print(e)
            return 0

class loginFunctions:
    def __init__(self,username,password,pool):
        self.username = str(username)
        self.password = password
        self.pool:cp.ConnectionPool = pool
    def checkUser(self):
        try:
            self.connection = self.pool.get_connection()
            if not isinstance(self.connection, str):
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT admin FROM LoginCredentials WHERE LOWER(username) = %s AND password = %s",(self.username.lower(),self.password,))
                    self.admin = cursor.fetchone()
                    self.pool.return_connection(self.connection)
                    if self.admin is not None:
                        return int(self.admin[0])
                    else:
                        return 'Incorrect Username or Password'
        except Exception as e:
            return str(e)

class facultyFunctions:
    def __init__(self,pool):
        self.pool:cp.ConnectionPool = pool
    def facultyRegister(self,name,phno,email,dept):
        self.name = name
        self.phno = phno
        self.email = email
        self.dept = dept
        try:
            self.connection = self.pool.get_connection()
            if not isinstance(self.connection, str):
                with self.connection.cursor() as cursor:
                    returned = self.checkAlreadyExist()
                    if returned == 0:
                        cursor.execute("INSERT INTO Faculty VALUES(%s,%s,%s,%s)",(self.name,self.email,self.phno,self.dept,))
                        self.connection.commit()
                        self.pool.return_connection(self.connection)
                        self.addToJson()
                        return 1
                    else:
                        return 'Faculty Already Registered'
            else:
                return 'Lost Internet Connection'
        except Exception as e:
            return str(e)
    def checkAlreadyExist(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from Faculty where PhoneNumber = %s",(self.phno,))
            self.result = cursor.fetchone()
            if self.result is not None:
                return 1 #return if already exists
            else:
                return 0 #return if not exists
    def initalCallToJson(self):
        try:
            self.connection = self.pool.get_connection()
            if not isinstance(self.connection, str):
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM Faculty")
                    self.result = cursor.fetchall()
                    self.pool.return_connection(self.connection)
                    self.json_data = []
                    for row in self.result:
                        data = {
                            "name": row[0],
                            "phno": row[1],
                            "dept": row[3]
                        }
                        self.json_data.append(data)
                    self.json_file_path = 'json_data.json'
                    with open(self.json_file_path, 'w') as json_file:
                        json.dump(self.json_data, json_file, indent=2)
                    return 1
            else:
                return 'Check Internet Connection'
        except Exception as e:
            return str(e)
    def addToJson(self):
        data = {
            "name": self.name,
            "phno": self.phno,
            "dept": self.dept
        }
        self.json_data.append(data)
        self.json_file_path = 'json_data.json'
        with open(self.json_file_path, 'w') as json_file:
            json.dump(self.json_data, json_file, indent=2)
    
class signUpFunctions:
    def __init__(self,pool):
        self.pool:cp.ConnectionPool = pool
    def signUp(self,username,password,admin):
        self.username = str(username)
        self.password = str(password)
        self.admin = admin
        try:
            self.connection = self.pool.get_connection()
            with self.connection.cursor() as cursor:
                response = self.userExists(self.connection)
                if not isinstance(response, str):
                    if response == 1:
                        self.pool.return_connection(self.connection)
                        return 'User Already Exists' #try reseting password? ###################################
                    else:
                        cursor.execute("INSERT INTO LoginCredentials VALUES(%s,%s,%s)",(self.username,self.password,self.admin,))
                        self.connection.commit()
                        self.pool.return_connection(self.connection)
                        return 1
                else:
                    return str(response)
        except Exception as e:
            return str(e)
    def userExists(self,connection):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM LoginCredentials WHERE LOWER(username) = %s",(self.username.lower(),))
                self.result = cursor.fetchone()
                if self.result is not None:
                    return 1 # user already exists
                else:
                    return 0
        except Exception as e:
            return str(e)

class newBarcodeRegistrationFuctions:
    def __init__(self,pool):
        self.pool:cp.ConnectionPool = pool
    def checkQrExists(self,connection, barcode):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM qravailable where qrid = %s",(barcode,))
                result = cursor.fetchone()
                if result is not None:
                    return 1 # qr already exists
                else:
                    return 0
        except Exception as e:
            return str(e)
    def registerQR(self,barcode):
        try:
            self.connection=self.pool.get_connection()
            if not isinstance(self.connection, str):
                with self.connection.cursor() as cursor:
                    returned = self.checkQrExists(self.connection,barcode)
                    if not isinstance(returned,str):
                        if returned == 0:
                            cursor.execute("INSERT INTO qravailable VALUES(%s,1)",(barcode,))
                            self.connection.commit()
                            self.pool.return_connection(self.connection)
                            return 1
                        else:
                            return 'QR already registered' #try reseting availability? #########################
            else:
                return 'Check Internet Connection'
        except Exception as e:
            return str(e)

class visitorEntryFunctions:
    def __init__(self,pool):
        self.pool:cp.ConnectionPool = pool
    def getVID(self):
        current_time = datetime.now()
        formatted_date = current_time.strftime("%d%m%Y")
        timestamp=int(formatted_date)
        try:
            self.connection=self.pool.get_connection()
            if not isinstance(self.connection, str):
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT vid from records order by intime limit 1")
                    self.result = cursor.fetchone()
                    self.pool.return_connection(self.connection)
                    if self.result is not None:
                        print(self.result[0],type(self.result[0]))
                        print(timestamp,type(timestamp))
                        print(self.result[0]%1000)
                        if timestamp == (self.result[0]//1000):
                            print('using result value that was fecthed: '+str(self.result[0]+1))
                            return int(self.result[0]+1)
                    print('using timestamp value')
                    return timestamp*1000+1
            else:
                return 'Check Internet Connection'
        except Exception as e:
            return str(e)
    '''def getQrid(self):
        try:
            self.connection=self.pool.get_connection()
            if not isinstance(self.connection, str):
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT qrid FROM qravailable WHERE availability = 1 LIMIT 1")
                    self.result = cursor.fetchone()
                    self.pool.return_connection(self.connection)
                    if self.result is not None:
                        return self.result[0]
                    else:
                        return 'No QR Available'
            else:
                return 'Check Internet Connection'
        except Exception as e:
            return str(e)'''
    def getIntime(self):
        current_date = datetime.now()
        current_time = current_date.strftime("%d/%m/%Y %H:%M:%S")
        return str(current_time)
    def registerVisitor(self,name,phone,email,person,reason,barcode):
        self.name = name
        self.phone = phone
        self.email = email
        self.person = person
        self.reason = reason
        self.vid = self.getVID()
        self.qrid = barcode
        self.intime = self.getIntime()
        if isinstance(self.vid,str):
            return self.vid
        else:
            print(self.vid)
            try:
                self.connection=self.pool.get_connection()
                if not isinstance(self.connection, str):
                    with self.connection.cursor() as cursor:
                        try:
                            cursor.execute("INSERT INTO Records VALUES(%s,%s,%s,%s,%s,%s,%s,%s,NULL)",(self.vid,self.qrid,self.name,self.phone,self.email,self.person,self.reason,self.intime,))
                            cursor.execute("INSERT INTO InVisitors VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(self.vid,self.qrid,self.name,self.phone,self.email,self.person,self.reason,self.intime,))
                            cursor.execute("UPDATE qravailable SET availability = 0 WHERE qrid = %s",(self.qrid,))
                            obj=mailtoFunctions(self.pool)
                            threading.Thread(target=obj.sendmail(self.name,self.phone,self.email,self.person,self.reason)).start()
                            self.connection.commit()
                        except Exception as e:
                            return str(e)
                        self.pool.return_connection(self.connection)
                        return 1
                else:
                    return 'Check Internet Connection'
            except Exception as e:
                return str(e)

class mailtoFunctions:
    def __init__(self,pool):
        self.pool:cp.ConnectionPool = pool
    def fetchEmail(self,person):
        try:
            self.connection = self.pool.get_connection()
            if not isinstance(self.connection, str):
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT Email FROM Faculty WHERE Name = %s",(person,))
                    self.result = cursor.fetchone()
                    self.pool.return_connection(self.connection)
                    if self.result is not None:
                        return self.result[0],1
            else:
                return 'Check Internet Connection',0
        except Exception as e:
            return str(e),0
    def sendmail(self, visitor_name, visitor_phone, visitorEmail, person_to_meet, reason_of_visit):
        email_sender = 'yourMail@gmail.com'
        email_password = 'passwordHere'
        email_recipient, flag = self.fetchEmail(person_to_meet)

        if flag == 1:
            subject = 'Visitor Management System'
            body = f"Mr./Ms. {visitor_name} is here to meet you.\n" \
                   f"He/She is at the gate and is expecting to meet you soon.\n" \
                   f"Contact: {visitor_phone}\nEmail: {visitorEmail}\nReason: {reason_of_visit}"

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_recipient  # Use the actual recipient here
            em['Subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_recipient, em.as_string())
            except Exception as e:
                logging.error(f"Error sending email: {str(e)}")
        else:
            logging.error(f"Unable to fetch recipient email for {person_to_meet}")

class visiotrExitFunctions:
    def __init__(self,pool):
        self.pool:cp.ConnectionPool = pool
    def outTimeFetch(self):
        current_date = datetime.now()
        current_time = current_date.strftime("%d/%m/%Y %H:%M:%S")
        return str(current_time)
    def visitorExit(self,barcode):
        self.barcode = barcode
        self.outime = self.outTimeFetch()
        try:
            self.connection = self.pool.get_connection()
            if not isinstance(self.connection, str):
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT vid FROM Records WHERE qrid = %s AND outtime IS NULL",(self.barcode,))
                    self.result = cursor.fetchone()
                    if self.result is not None:
                        self.vid = self.result[0]
                        cursor.execute("UPDATE Records SET outtime = %s WHERE vid = %s",(self.outime,self.vid,))
                        cursor.execute("UPDATE qravailable SET availability = 1 WHERE qrid = %s",(self.barcode,))
                        cursor.execute("DELETE FROM InVisitors WHERE vid = %s",(self.vid,))
                        self.connection.commit()
                        self.pool.return_connection(self.connection)
                        return 1
                    else:
                        return 'Invalid QR'
            else:
                return 'Check Internet Connection'
        except Exception as e:
            return str(e)
