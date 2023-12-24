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
        self.username = username
        self.password = password
        self.pool:cp.ConnectionPool = pool
    def checkUser(self):
        try:
            self.connection = self.pool.get_connection()
            if not isinstance(self.connection, str):
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT admin FROM LoginCredentials WHERE username = %s AND password = %s",(self.username,self.password,))
                    self.admin = cursor.fetchone()
                    if self.admin is not None:
                        return int(self.admin)
                    else:
                        return None
        except Exception as e:
            print(e)