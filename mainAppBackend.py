import connectionpool as cp
import json
from datetime import datetime

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
                    cursor.execute("SELECT vid FROM Records ORDER BY vid DESC LIMIT 1")
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
                        cursor.execute("INSERT INTO Records VALUES(%s,%s,%s,%s,%s,%s,%s,%s,NULL)",(self.vid,self.qrid,self.name,self.phone,self.email,self.person,self.reason,self.intime,))
                        cursor.execute("INSERT INTO InVisitors VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(self.vid,self.qrid,self.name,self.phone,self.email,self.person,self.reason,self.intime,))
                        cursor.execute("UPDATE qravailable SET availability = 0 WHERE qrid = %s",(self.qrid,))
                        self.connection.commit()
                        self.pool.return_connection(self.connection)
                        return 1
                else:
                    return 'Check Internet Connection'
            except Exception as e:
                return str(e)
