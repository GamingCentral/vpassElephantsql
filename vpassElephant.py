import urllib.parse as up
import psycopg2

class checkconnection:
    def __init__(self,dburl):
        self.dburl=up.urlparse(dburl)
    def connect(self): #make a connection if connected save it in pool {a temporary array}
        try:
            conn = psycopg2.connect(
                database=self.dburl.path[1:],
                user=self.dburl.username,
                password=self.dburl.password,
                host=self.dburl.hostname,
                port=self.dburl.port
            )
            return conn   #pool of connections, REMEMBER THIS IS NOT CLOSED!!! NEED TO BE CLOSED IF WINDOW CLOSED    
        except Exception as e:
            return str(e)
        
def runcheckconnect(url):
    chc=checkconnection(url)
    res=chc.connect()
    return res