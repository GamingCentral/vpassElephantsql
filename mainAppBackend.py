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
                return self.pool
        except Exception as e:
            print(e)
            return 0