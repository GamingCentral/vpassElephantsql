class creds:
    def __init__(self,username,password,conn):
        self.username=username
        self.password=password
        self.conn=conn

    def checkcreds(self):
        #check if credentials are valid or not
        try:
            with self.conn.cursor() as cursor:
                cmd="select password,admin from creds where lower(username)=?"
                cursor.execute(cmd,str(self.username).lower(),)
                res=cursor.fetchone()
                if res:
                    password,admin=res
                    if str(password)==self.password:
                        return admin
                return None #password wrong or invalid credentials as a whole
        except Exception as e:
            print("Error in checking credentials!: ",e)
            return None
        
def credchecker(username,password,conn):
    c=creds(username,password,conn)
    res=c.checkcreds()
    return res