import psycopg2.pool
import threading
import time
import urllib.parse as up

class ConnectionPool:
    def __init__(self, db_url, minconn, maxconn):
        parsed_url = up.urlparse(db_url)
        db_params = {
            "database": parsed_url.path[1:],
            "user": parsed_url.username,
            "password": parsed_url.password,
            "host": parsed_url.hostname,
            "port": parsed_url.port
        }

        self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=minconn,
            maxconn=maxconn,
            **db_params
        )

        self.monitor_thread = threading.Thread(target=self.monitor_pool, daemon=True)
        self.monitor_thread_started = False  # Flag to ensure one monitor thread per pool

    def get_connection(self):
        try:
            if not self.monitor_thread_started:
                self.monitor_thread.start()
                self.monitor_thread_started = True
            return self.connection_pool.getconn()
        except psycopg2.OperationalError as e:
            print(e)
            return str(e)

    def return_connection(self, conn):
        self.connection_pool.putconn(conn)

    def close_pool(self):
        self.connection_pool.closeall()

    def monitor_pool(self):
        while True:
            for conn in self.connection_pool._pool:
                if not conn.closed:
                    try:
                        conn.isolation_level = None
                        conn.rollback()
                    except psycopg2.Error:
                        res=self.recover_connection(conn)
            time.sleep(60)  # Check every minute

    def recover_connection(self, conn):
        try:
            self.connection_pool.putconn(conn)
            new_conn = self.connection_pool.getconn()
            if new_conn is not None:
                print("Recovered connection:", conn)
                return 1
            else:
                print("Could not recover connection:", conn)
                return 0
        except Exception as e:
            print(e)
            return 0

# Usage
def poolcreate(dburl):
    db_url = dburl
    pool = ConnectionPool(db_url, minconn=1, maxconn=10)
    return pool
