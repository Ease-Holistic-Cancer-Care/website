from email import message
from flask import Flask, render_template, redirect, url_for, session, request
import sqlite3
import os

#Initialize Flask App
app = Flask(__name__)
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
database_location = os.path.join(THIS_FOLDER, 'database.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    data = database_cursor.execute("SELECT * FROM about")
    data = data.fetchone()
    database_connection.commit()
    database_connection.close()
    # convert data to list
    data = list(data)
    data[4] = data[4].split(';')
    data[6] = data[6].split(';')
    
    return render_template('about.html', data=data)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginConfirm', methods=['POST'])
def loginConfirm():
    email = request.form['email']
    password = request.form['password']
    if email == 'abc@gmail.com' and password == 'abc':
        return redirect(url_for('index'))
    else:
        return redirect(url_for('doctors'))

@app.route('/doctors')
def doctors():
    return render_template('doctors.html')

@app.route('/doctorInfo')
def doctorsInfo():
    return render_template('doctor_info.html')

@app.route('/specialty')
def specialty():
    return render_template('specialty.html')

@app.route('/awards')
def awards():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    data = database_cursor.execute("SELECT * FROM awards")
    data = data.fetchall()
    return render_template('awards.html', data=data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

@app.route('/appointmentSubmit', methods=['POST'])
def appointmentSubmit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    gender = request.form['gender']
    phone_number = request.form['number']
    appointment_type = request.form['appointment_type']
    message = request.form['message']
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    database_cursor.execute("INSERT INTO appointment VALUES (?,?,?,?,?,?,?,?)", (first_name, last_name, email, gender, phone_number, appointment_type, message, 'pending'))
    database_connection.commit()
    database_connection.close()
    return redirect(url_for('appointment'))

@app.route('/patient')
def patient(): 
    return render_template('patient.html')

@app.route('/virtualTour')
def virtualTour():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    data = database_cursor.execute("SELECT * FROM virtual_tour")
    data = data.fetchall()
    return render_template('virtualTour.html', data=data)

@app.route('/blogs')
def blogs(): 
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    data = database_cursor.execute("SELECT * FROM blogs")
    data = data.fetchall()
    return render_template('blogs.html', data=data)

@app.route('/news')
def news(): 
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    data = database_cursor.execute("SELECT * FROM news")
    data = list(data.fetchall())
    latest_news = []
    for i in range(len(data)):
        if data[i][4] == 'yes':
            latest_news.append(data[i])
    #remove latest news from data
    for i in range(len(latest_news)):
        data.remove(latest_news[i])
    print(len(data))
    return render_template('news.html', data=data, latest_news=latest_news)

if __name__ == '__main__':
    app.run(debug=True,port=5001)