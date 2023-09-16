import os
import json 
import mysql.connector
from flask import Flask
from mysql.connector import Error

app = Flask(__name__)

dbsecret = "/vault/secrets/credentials.txt"
# make sure that the file name under /vault/secrets/credentials.txt match the
# one you put on the the annotation vault.hashicorp.com/agent-inject-secret-credentials.txt on pod


if os.path.exists(dbsecret):
    # Open the secret file in read mode
    with open(dbsecret, 'r') as file:
        # Read the content of the file, which should contain your credentials
        dbcredentials = file.read()
else:
    print("File dbsecret does not exist")
       
       
db = json.loads(dbcredentials)
# Database connection
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '3306')
db_database = os.getenv('DB_DATABASE', 'demo')
db_user = db["username"]
db_password = db["password"]


try:
    connection = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_database
    )
    if connection.is_connected():
        print('Connected to MySQL database!')
except Error as e:
    print('Failed to connect to MySQL database:', e)
    raise e


@app.route('/')
def hello():
    return 'Hello World!'
    


if __name__ == '__main__':
    app.run(debug=True ,  host='0.0.0.0')
