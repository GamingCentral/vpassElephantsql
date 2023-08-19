import datetime
import mysql.connector
import os.path
import os
import mailto as mt
import threading as th
import barscan_cloud
import csv
import Installation_files.databaseConnect as dc
#from Installation_files import create_cloud_tables

def cursorcreate():
    dbp=dc.extractinfo()
    u,p=dbp[0],dbp[1]
    try:
        mydb = mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            user=str(u),
            password=str(p),
            database=str(u)
        )
        return mydb
    except Exception as e:
        print(e)

def check_database_table_exist(table_name):
    '''cursor = mydb.cursor()

    # Check if the table exists
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND LOWER(table_name) = %s",(table_name,))
    table_exists = cursor.fetchone() is not None #fetches next row until the row turns out to be none(end of rows)
    # Check if the table has the correct schema
    if table_exists:
        pass
    else:
        create_cloud_tables.execute_main()
        mydb.commit()
    cursor.close()
    mydb.close()'''
    return 1

def run_once_per_day(table_use1,table_use2,table_use3):
    # Check if the file exists and read the last run timestamp
    filename = 'lastrun.txt'
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            last_run_str = f.read().strip()
            last_run = datetime.datetime.strptime(last_run_str, '%Y-%m-%d').date()
    else:
        last_run = datetime.date.min #first time execution

    today = datetime.date.today()
    if last_run < today:
        f1=check_database_table_exist(table_use1)
        f2=check_database_table_exist(table_use2)
        f3=check_database_table_exist(table_use3)
        if(f1==1 and f2==1 and f3==1):
            # Update the last run timestamp in the file
            with open(filename, 'w') as f:
                f.write(str(today))
            f.close()
            return f1
        else:
            return 0
    else:
        return 1

class rdbms:
    def fetch_last_vid(self, table_name):
        mydb=cursorcreate()
        cursor = mydb.cursor()
        '''strcmd = "SELECT vid FROM " + str(table_name) + " ORDER BY rowid DESC LIMIT 1"'''
        strcmd="SELECT vid FROM {} ORDER BY {} DESC LIMIT 1".format(table_name, 'vid')
        cursor.execute(strcmd)
        result = cursor.fetchone()
        last_vid = result[0] if result else None
        cursor.close()
        mydb.close()
        return last_vid
    



class addvisitorinfo:
    def __init__(self,n,p,e,c,r):
        self.Name=n
        self.Phno=p
        self.Ptm=c
        self.email=e
        self.reason=r
        self.qrid='NULL'
        self.intime='NULL'
        self.outime='NULL'
    
    def generatevid(self,need):
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        new_date = datetime.datetime.strptime(current_date, '%Y-%m-%d').strftime('%y%d%m')
        #if(new_date==)
        if(need==True):
            return int(new_date)*1000+1
        else:
            return int(new_date)
    
    def insert_into_table(self,table_name,vid):
        mydb=cursorcreate()
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO "+str(table_name)+" VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"+";",(str(vid),str(self.qrid),self.Name,str(self.Phno),self.email,self.Ptm,self.reason,str(self.intime),str(self.outime)))
        mydb.commit()
        cursor.close()
        mydb.close()

    
    def qrid_link(self,vid,qrid):
        mydb=cursorcreate()
        cur = mydb.cursor()
        cur.execute(f"UPDATE Records SET qrid = "+str(qrid)+" WHERE vid = "+str(vid))
        mydb.commit()
        cur.close()
        mydb.close()
        mydb=cursorcreate()
        cur = mydb.cursor()
        cur.execute(f"UPDATE QRavailable SET availability = 0 WHERE qrid = "+str(qrid))
        mydb.commit()
        cur.close()
        mydb.close()

class Execute:

    def __init__(self,n,p,e,pt,r,b):
        self.Name=n
        self.Phno=int(p)
        self.Email=e
        self.ptm=pt
        self.reasonofvisit=r
        self.barcode=b

    def process_main(self):
        f1=run_once_per_day('Records','InVisitors','QRavailable') #first check for table existance and creation
        if(f1==1):
            #process continues if both table and schema are matched
            vid=self.addnewvisitor()
            return vid
            #now we need to query for last used vid if same day or create new if different day
            #process 1: new user with unique vid is registered(insertion),
            #process 1.5: qid is fetched from available list whose availabitlity is set as 1 and assigned to vid
            #process 2: intime is taken(by using qid) for user in records whose IT is null(fetching user) then copy data to invisitors
            #process 3: now fetch by qid from invisitors and note the ot and then push it to records also then remove it from invisitors   
        else:
            print("process terminated because of wrong schema")   #---------->prompt
        
    def addnewvisitor(self):
        #if==1
        #2:
        v=addvisitorinfo(self.Name,self.Phno,self.Email,self.ptm,self.reasonofvisit)
        ord=rdbms()
        last_vid=ord.fetch_last_vid('Records')
        vid_today=v.generatevid(False)
        if(last_vid==None):
            vid=v.generatevid(True)
        elif(last_vid!=None):
            if(vid_today!=last_vid//1000): # type: ignore
                vid=v.generatevid(True)
            else:
                vid=last_vid+1 # type: ignore
        #3:
        v.insert_into_table('Records',vid)
        return vid
        #mailto faculty...
        
        #--------------------------------------------------------------

class mailtofac():
    def __init__(self,ptm,Name,Phno,reasonofvisit):
        mt.mail_run(ptm,Name,Phno,reasonofvisit)

class download_db(): #-----------------------------------------------
    def download_Records(self):
        mydb=cursorcreate()
        cur = mydb.cursor()
        cur.execute("select * from Records")
        rows=cur.fetchall()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        subfolder = 'database_downloaded/Records'
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)
        filename = os.path.join(subfolder, f'Records@{timestamp}.csv')
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([col[0] for col in cur.description])
            for row in rows:
                writer.writerow(row)
        cur.close()
        mydb.close()

    def download_InVistors(self):
        mydb=cursorcreate()
        cur=mydb.cursor()
        cur.execute("select * from InVisitors")
        rows=cur.fetchall()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        subfolder = 'database_downloaded/InVisitors'
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)
        filename = os.path.join(subfolder, f'InVisitors@{timestamp}.csv')
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([col[0] for col in cur.description])
            for row in rows:
                writer.writerow(row)
        cur.close()
        mydb.close()

def database_download():
    d=download_db()
    d.download_Records()
    d.download_InVistors()



def exit(b):
    print("in exit")
    barscan_cloud.barcode_execute_out(b)

def main_run(n,p,em,pt,r,b):
    e=Execute(n,p,em,pt,r,b)
    vid=e.process_main()
    barscan_cloud.barcode_execute_assign(b,vid,n,p,em,pt,r)


def mailtooperation(ptm,Name,Phno,reasonofvisit):
    mtf=mailtofac(ptm,Name,Phno,reasonofvisit)

def allthreadrun(n,p,em,pt,r,b):
    th.Thread(target=main_run(n,p,em,pt,r,b)).start()
    th.Thread(target=mailtooperation(pt,n,p,r)).start()
