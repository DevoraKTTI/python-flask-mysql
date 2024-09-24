# Author: Clinton Daniel, University of South Florida
# Date: 4/4/2023
# Description: This is a Flask App that uses SQLite3 to
# execute (C)reate, (R)ead, (U)pdate, (D)elete operations
# to run "python -m flask run "
from flask import Flask
from flask import render_template
from flask import request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
def get_db_connection():
    try:
        con = mysql.connector.connect(
            host= 'localhost',
            user= 'root',
            password= 'Mysql68!',
            database= 'database1'
        )
        if con.is_connected():
            return con
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# Home Page route
@app.route("/")
def home():
    return render_template("home.html")

# Route to form used to add a new student to the database
@app.route("/enternew")
def enternew():
    return render_template("student.html")

# Route to add a new record (INSERT) student data to the database
@app.route("/addrec", methods = ['POST', 'GET'])
def addrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            zip = request.form['zip']

            con = get_db_connection()
            if con:
                cur = con.cursor()
                cur.execute("INSERT INTO students ( name, addr, city, zip) VALUES (%s, %s, %s, %s)", (nm, addr, city, zip))
                con.commit()
                msg = "Record successfully added to database"
            else:
                msg = "Database connection failed"
        except Exception as e:
            msg = f"Error in the INSERT: {e}"
        finally:
            if con and con.is_connected():
                con.close()
            return render_template('result.html', msg=msg)

# Route to SELECT all data from the database and display in a table      
@app.route('/list')
def list():
    print("got to list")
    con = get_db_connection()
    if con:
        cur = con.cursor(dictionary=True)
        #  cur.execute("SELECT id, name, addr, city, zip FROM students")
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()
        #next 2
        con.close()
        return render_template("list.html", rows=rows)


# Route that will SELECT a specific row in the database then load an Edit form 
@app.route("/edit", methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            id = request.form['id']
            # Connect to the database and SELECT a specific rowid
            con = get_db_connection()
            if con:
                cur = con.cursor(dictionary=True)
                cur.execute("SELECT id, name, addr, city, zip FROM students WHERE id = %s", (id,))
                rows = cur.fetchall()
        except Exception as e:
            rows = []
        finally:
            if con and con.is_connected():
                con.close()
            return render_template("edit.html", rows=rows)


# Route used to execute the UPDATE statement on a specific record in the database
@app.route("/editrec", methods=['POST','GET'])
def editrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            rowid = request.form['id']
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            zip = request.form['zip']

            con = get_db_connection()
            if con:
                cur = con.cursor()
                cur.execute("UPDATE students SET name=%s, addr=%s, city=%s, zip=%s WHERE id=%s", (nm, addr, city, zip, rowid))
                con.commit()
                msg = "Record successfully edited in the database"
            else:
                msg = "Database connection failed"
        except Exception as e:
            msg = f"Error in the Edit: {e}"
        finally:
            if con and con.is_connected():
                con.close()
            return render_template('result.html', msg=msg)



# Route used to DELETE a specific record in the database    
@app.route("/delete", methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['id']
            con = get_db_connection()
            #if con:
            cur = con.cursor()
            cur.execute("DELETE FROM students WHERE ID=%s", (rowid,))
            con.commit()
            msg = "Record successfully deleted from the database"
            #else:
                #msg = "Database connection failed"
        except Exception as e:
            msg = f"Error in the DELETE: {e}"
        finally:
            if con and con.is_connected():
                con.close()
            return render_template('result.html', msg=msg)
