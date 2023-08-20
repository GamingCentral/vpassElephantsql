import mysql.connector
import databaseConnect as dc

#-------------->CHECKED! UP AND RUNNING

dbp=dc.extractinfo()
u,p=dbp[0],dbp[1]
try:
    mydb = mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user=str(u),
        password=str(p),
        database=str(u)
    )
except Exception as e:
    print(e)

create_table_query = """
CREATE TABLE Records (
    vid INT PRIMARY KEY,
    qrid VARCHAR(50),
    name VARCHAR(25),
    phno BIGINT,
    email VARCHAR(40),
    ptm VARCHAR(25),
    reasonofvisit VARCHAR(75),
    IT varchar(20),
    OT varchar(20) default NULL
)
"""
create_invisitors_query = """
CREATE TABLE InVisitors (
    vid INT,
    qrid VARCHAR(50),
    name VARCHAR(25),
    phno BIGINT,
    email VARCHAR(40),
    ptm VARCHAR(25),
    reasonofvisit VARCHAR(75),
    IT varchar(20)
)
"""
# Create the QRavailable and faculty tables if they don't exist
create_qravailable_query = """
CREATE TABLE IF NOT EXISTS QRavailable (
    qrid VARCHAR(50) PRIMARY KEY,
    availability integer default 1 not null
)
"""
create_table_credentails= """
CREATE TABLE IF NOT EXISTS credentails (
    username varchar(30) primary key not null unique, 
    password varchar(30), 
    Admin Integer not null default 0
)
"""

create_faculty_query = """
CREATE TABLE IF NOT EXISTS faculty (
    name VARCHAR(25) PRIMARY KEY,
    email varchar(40) not null, 
    department varchar(10), 
    contact bigint not null
)
"""
def execute_main():
    cursor = mydb.cursor()
    try:
        cursor.execute(create_qravailable_query)
    except Exception as e:
        pass
    try:
        cursor.execute(create_faculty_query)
    except Exception as e:
        pass
    try:
        cursor.execute(create_table_credentails)
        cursor.execute("insert into credentails values('Admin','123456','1')")
    except Exception as e:
        pass
    try:
        cursor.execute(create_table_query)
    except Exception as e:
        pass
    try:
        cursor.execute(create_invisitors_query)
    except Exception as e:
        pass
    mydb.commit()
    cursor.close()
    mydb.close()

execute_main()