from datetime import datetime

def getIntime():
    current_date = datetime.now()
    current_time = current_date.strftime("%d/%m/%Y %H:%M:%S")
    return str(current_time)

print(getIntime())