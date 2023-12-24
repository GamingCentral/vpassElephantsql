import connectionpool as cp

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
    def __init__(self,name,phno,email,dept,pool):
        self.name = name
        self.phno = phno
        self.email = email
        self.dept = dept
        self.pool:cp.ConnectionPool = pool
    def facultyRegister(self):
        try:
            self.connection = self.pool.get_connection()
            if not isinstance(self.connection, str):
                with self.connection.cursor() as cursor:
                    returned = self.checkAlreadyExist()
                    if returned == 0:
                        cursor.execute("INSERT INTO Faculty VALUES(%s,%s,%s,%s)",(self.name,self.email,self.phno,self.dept,))
                        self.connection.commit()
                        self.pool.return_connection(self.connection)
                        return 'Faculty Registered Successfully'
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
