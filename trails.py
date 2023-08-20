import urllib.parse as up
import psycopg2

connection_url = "postgres://piciqucz:oD0UWQowMN4O3Jasjd32c-7qX-hetspn@bubble.db.elephantsql.com/piciqucz"

if connection_url:
    url = up.urlparse(connection_url)
    
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    
    print("Connected to the database!")
    try:

        with conn.cursor() as cursor:
            cursor.execute("drop table test")
            conn.commit()
    
    # Perform database operations here
    except Exception as e:
        print(e)
    finally:
        conn.close()
        print("Connection closed.")
else:
    print("ELEPHANTSQL_URL environment variable not set.")
