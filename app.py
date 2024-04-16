from flask import Flask, render_template, redirect, url_for, g, request, send_file
import os
import sqlite3
import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__)

# SQL Lite DB for login information.
def connect_db():
    conn = sqlite3.connect('dashboard.db')
    cursor = conn.cursor()

    cursor.executescript('''
        create table if not exists user (
            id integer primary key autoincrement,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL
        );
     ''')

    conn.commit()
    return conn

# Initial Route
@app.route('/', methods=['GET'])
def loadRegister():
    return render_template('register.html')

@app.route('/dashboard', methods=['GET'])
def loadDashboard():
    # TEST CODE

    # Students data available in a list of list
    students = [['Akash', 34, 'Sydney', 'Australia'],
                ['Rithika', 30, 'Coimbatore', 'India'],
                ['Priya', 31, 'Coimbatore', 'India'],
                ['Sandy', 32, 'Tokyo', 'Japan'],
                ['Praneeth', 16, 'New York', 'US'],
                ['Praveen', 17, 'Toronto', 'Canada']]
     
    # Convert list to dataframe and assign column values
    df = pd.DataFrame(students,
                      columns=['Name', 'Age', 'City', 'Country'],
                      index=['a', 'b', 'c', 'd', 'e', 'f'])
     
    # Create Bar chart
    fig = px.bar(df, x='Name', y='Age', color='City', barmode='group')
     
    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
     
    # Use render_template to pass graphJSON to html
    return render_template('dashboard.html', bar=graphJSON)

@app.route('/login', methods=['GET'])
def loadLogin():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    g.db = connect_db()
    cursor = g.db.execute('SELECT * FROM user where username = ? and password = ?', (username, password))
    user = cursor.fetchone()
    if (user == None):
        g.db.close()
        return None
    g.db.close()
    return redirect(url_for('loadDashboard'))

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        g.db = connect_db()
        cursor = g.db.execute('SELECT * FROM user where username = ? and email = ?', (username, email))
        users = cursor.fetchall()

        if len(users) != 0:
            g.db.close()
            return render_template('register.html', error='username and email is already in use.')
        
        g.db.execute('INSERT INTO user (username, password, email) VALUES (?, ?, ?)', (username, password, email))

        cursor = g.db.execute('SELECT * FROM user where username = ?', (username,))
        newUser = cursor.fetchone()

        g.db.commit()
        g.db.close()
        return redirect(url_for('loadDashboard'))

    

    
if __name__ == '__main__':
    app.run(debug=True)