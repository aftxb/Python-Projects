from datetime import date
from email import message
from flask import Flask,render_template,request,redirect,url_for

import pymysql
db_connection = None
tb_cursor = None

app = Flask(__name__)

# function to connect to database
def connectToDb():
    global db_connection, tb_cursor
    db_connection=pymysql.connect(host="localhost",user="root", passwd="",database="agms",port=3306)
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
def getAllartData():
    connectToDb()
    selectQuery= "select * from art;"
    tb_cursor.execute(selectQuery)
    allData = tb_cursor.fetchall()
    disconnectDb()
    print(allData)
    return allData

def insertIntoTable(artwork,artist,genre,year):
    connectToDb()
    inserQuery = "INSERT INTO art(artwork,artist,genre,year) VALUES(%s, %s, %s, %s);"
    tb_cursor.execute(inserQuery,(artwork,artist,genre,year))
    db_connection.commit()
    disconnectDb()
    return True

# funtion for update-delete from database
def getartBasedOnID(id):
    connectToDb()
    selectQuery = "SELECT * FROM art WHERE ID=%s;"
    tb_cursor.execute(selectQuery,(id,))
    oneData = tb_cursor.fetchone()
    disconnectDb()
    return oneData
def updateartIntoTable(artwork,artist,genre,year,id):
    connectToDb()
    updateQuery = "UPDATE art SET artwork=%s,artist=%s,genre=%s,year=%s WHERE ID=%s;"
    tb_cursor.execute(updateQuery,(artwork,artist,genre,year,id))
    db_connection.commit()
    disconnectDb()
    return True
def deleteartFromTable(id):
    connectToDb()
    deleteQuery = "DELETE FROM art WHERE ID=%s;"
    tb_cursor.execute(deleteQuery,(id,))
    db_connection.commit()
    disconnectDb()
    return True

@app.route("/")
def  index():
    allart = getAllartData()
    return render_template("index.html",data = allart)

@app.route("/add",methods=["GET","POST"])
def addart():
    if request.method == "POST":
        data = request.form
        isiInserted = insertIntoTable(data['txtartwork'],data['txtartist'],data['txtgenre'],data['txtyear'])
        if(isiInserted):
            msg= "Art Data Inserted"
        else:
            msg="Not Inserted"
        return render_template("add.html",message=msg)
    return render_template("add.html")

@app.route("/update/",methods=["GET","POST"])
def updateart():
    id = request.args.get("ID",type=int,default=1)
    idData = getartBasedOnID(id)
    if request.method == "POST":
        data = request.form
        isUpdated = updateartIntoTable(data['txtartwork'],data['txtartist'],data['txtgenre'],data['txtyear'],id)
        if(isUpdated):
            
            message = "Updation Success"
        else:
            message = "Updation Error"
        return render_template("update.html",message = message)
    return render_template("update.html",data=idData)

@app.route("/delete/")
def deleteart():
    id = request.args.get("ID",type=int,default=1)
    deleteartFromTable(id)
    return redirect(url_for("index"))


if __name__=='__main__':
    app.run(debug=True)