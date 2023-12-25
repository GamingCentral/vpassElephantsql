import connectionpool as cp 
import json

pool = cp.ConnectionPool('postgres://piciqucz:oD0UWQowMN4O3Jasjd32c-7qX-hetspn@bubble.db.elephantsql.com/piciqucz',1,10)
connection = pool.get_connection()
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM Faculty")
    result = cursor.fetchall()
    pool.return_connection(connection)
pool.close_pool()
json_data = []

for row in result:
    data = {
        "name": row[0],
        "phno": row[1],
        "dept": row[3]
    }
    json_data.append(data)

# Specify the file path where you want to save the JSON file
json_file_path = 'json_data.json'

# Write the data to the JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(json_data, json_file, indent=2)

print(f'Data saved to {json_file_path}')
