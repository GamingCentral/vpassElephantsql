import psycopg2.pool
import time
import urllib.parse as up

class ConnectionPool:
    def __init__(self, db_url):
        parsed_url = up.urlparse(db_url)
        self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            database=parsed_url.path[1:],
            user=parsed_url.username,
            password=parsed_url.password,
            host=parsed_url.hostname,
            port=parsed_url.port
        )

    def get_connection(self):
        return self.connection_pool.getconn()

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
                        self.recover_connection(conn)
            time.sleep(60)  # Check every minute

    def recover_connection(self, conn):
        self.connection_pool.putconn(conn)
        new_conn = self.connection_pool.getconn()
        if new_conn is not None:
            print("Recovered connection:", conn)
        else:
            print("Could not recover connection:", conn)

# Usage
if __name__ == "__main__":
    db_url = "postgres://your_user:your_password@your_host:your_port/your_database"
    pool = ConnectionPool(db_url)
    
    # Start a thread to monitor and recover connections
    import threading
    monitor_thread = threading.Thread(target=pool.monitor_pool)
    monitor_thread.start()

    try:
        # Perform your database operations using 'conn'
        pass
    finally:
        pool.close_pool()
