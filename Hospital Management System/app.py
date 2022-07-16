from email import message
from logging import root
from select import select
from unicodedata import name
from flask import Flask, render_template, request

import pymysql
db_connection = None
tb_cursor = None

app = Flask(__name__)

# function to connect to database
def connectToDb():
    global db_connection, tb_cursor
    db_connection=pymysql.connect(host="localhost",user="root", passwd="",database="hospital",port=3306)
    if(db_connection):
        print("done!!!")
        tb_cursor=db_connection.cursor()
    else:
        print("not done")

# function to disconnect from database
def disconnectDb():
    db_connection.close()
    tb_cursor.close()

# function to get data from database
def getAllPatientsData():
    connectToDb()
    selectQuery= "select * from patient;"
    tb_cursor.execute(selectQuery)
    allData = tb_cursor.fetchall()
    disconnectDb()
    print(allData)
    return allData

def insertIntoTable(name,phone,city,date):
    connectToDb()
    inserQuery = "INSERT INTO patient(name,phone,city,date) VALUES(%s, %s, %s, %s);"
    tb_cursor.execute(inserQuery,(name,phone,city,date))
    db_connection.commit()
    disconnectDb()
    return True


@app.route("/")
def  index():
    allPatients = getAllPatientsData()
    return render_template("index.html",data = allPatients)

@app.route("/add",methods=["GET","POST"])
def addPatient():
    if request.method == "POST":
        data = request.form
        isiInserted = insertIntoTable(data['txtName'],data['txtPhone'],data['txtCity'],data['txtDate'])
        if(isiInserted):
            msg= "Patient Data Inserted"
        else:
            msg="Not Inserted"
        return render_template("add.html",message=msg)
    return render_template("add.html")


if __name__=='__main__':
    app.run(debug=True)