class creds:
    def __init__(self,username,password,conn):
        self.username=username
        self.password=password
        self.conn=conn

    def checkcreds(self):
        #check if credentials are valid or not
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT LOWER(username), password,Admin FROM creds")
                rows=cursor.fetchall()
                for row in rows:
                    if str(self.username)
