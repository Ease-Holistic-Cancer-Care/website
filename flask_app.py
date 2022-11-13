from flask import Flask, render_template, redirect, url_for, session, request
import sqlite3
from mail import *
import random
import string
from locations import *
import json
import numpy as np

#Initialize Flask App
app = Flask(__name__)
app.secret_key = 'super secret key'

#social media links
database_connection = sqlite3.connect(database_location)
database_cursor = database_connection.cursor()
social_links = database_cursor.execute("SELECT * FROM social_links")
social_links = social_links.fetchall()

# specialties
navbar_specialties = database_cursor.execute("SELECT id,name FROM specialty")
navbar_specialties = navbar_specialties.fetchall()

# diseases
navbar_diseases = database_cursor.execute("SELECT id,title FROM diseases")
navbar_diseases = navbar_diseases.fetchall()

database_connection.commit()
database_connection.close()

#frontend
@app.route('/')
def index():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    slides = database_cursor.execute("SELECT * FROM home_carousel")
    slides = slides.fetchall()
    about = database_cursor.execute("SELECT * FROM home_page")
    about = about.fetchone()
    specialties = database_cursor.execute("SELECT * FROM specialty")
    specialties = specialties.fetchmany(6)
    statistics = database_cursor.execute("SELECT * FROM home_statistics")
    statistics = statistics.fetchall()
    doctor_data = database_cursor.execute("SELECT * FROM doctors")
    doctor_data = doctor_data.fetchall()
    testimonials = database_cursor.execute("SELECT * FROM testimonials")
    testimonials = testimonials.fetchall()
    faqs = database_cursor.execute("SELECT * FROM home_faq")
    faqs = faqs.fetchall()
    database_connection.commit()
    database_connection.close()
    return render_template('index.html',slides=slides, about=about, specialties=specialties, statistics=statistics, social_links=social_links, doctor_data=doctor_data, testimonials=testimonials, faqs=faqs, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/about/')
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
    return render_template('about.html', data=data,social_links=social_links,navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/doctors/')
def doctors():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    data = database_cursor.execute("SELECT * FROM doctors")
    data = data.fetchall()
    database_connection.commit()
    return render_template('doctors.html',social_links=social_links, data=data, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/doctorInfo/<string:id>/')
def doctorsInfo(id):
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    doctor_data = database_cursor.execute("SELECT * FROM doctors WHERE id = ?",(int(id),))
    doctor_data = doctor_data.fetchone()
    if doctor_data == None:
        return redirect(url_for('index'))
    doctor_profile = database_cursor.execute("SELECT * FROM doctor_profile WHERE id = ?",(int(id),))
    doctor_profile = doctor_profile.fetchone()
    doctor_degree = database_cursor.execute("SELECT * FROM doctor_degree WHERE id = ?",(int(id),))
    doctor_degree = doctor_degree.fetchall()
    doctor_experience = database_cursor.execute("SELECT * FROM doctor_experience WHERE id = ?",(int(id),))
    doctor_experience = doctor_experience.fetchall()
    database_connection.commit()
    database_connection.close()
    return render_template('doctorInfo.html',social_links=social_links, doctor_data=doctor_data, doctor_profile=doctor_profile, doctor_degree=doctor_degree, doctor_experience=doctor_experience,navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/specialty/')
def specialty():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    specialties = database_cursor.execute("SELECT * FROM specialty")
    specialties = specialties.fetchall()
    database_connection.commit()
    database_connection.close()
    return render_template('specialty.html',social_links=social_links, specialties=specialties,navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/diseases/<string:id>/')
def diseases(id):
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    diseases = database_cursor.execute("SELECT * FROM diseases WHERE specialty_id = ?",(int(id),))
    diseases = diseases.fetchall()
    if len(diseases) == 0:
        database_connection.commit()
        database_connection.close()
        return redirect(url_for('index'))
    specialty_name = database_cursor.execute("SELECT name FROM specialty WHERE id = ?",(int(id),))
    specialty_name = specialty_name.fetchone()[0]
    database_connection.commit()
    database_connection.close()
    return render_template('diseases.html',social_links=social_links, specialty_name=specialty_name, diseases=diseases,navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/disease/<string:id>/')
def disease(id):
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    disease_data = database_cursor.execute("SELECT * FROM diseases WHERE id = ?",(int(id),))
    disease_data = disease_data.fetchone()
    if disease_data == None:
        database_connection.commit()
        database_connection.close()
        return redirect(url_for('index'))
    specialty_name = database_cursor.execute("SELECT name FROM specialty WHERE id = ?",(disease_data[2],))
    specialty_name = specialty_name.fetchone()[0]
    disease_profile = database_cursor.execute("SELECT * FROM disease_profile WHERE disease_id = ?",(int(id),))
    disease_profile = disease_profile.fetchall()
    disease_types = database_cursor.execute("SELECT * FROM disease_types WHERE disease_id = ?",(int(id),))
    disease_types = disease_types.fetchall()
    disease_causes = database_cursor.execute("SELECT * FROM disease_causes WHERE disease_id = ?",(int(id),))
    disease_causes = disease_causes.fetchall()
    disease_symptoms = database_cursor.execute("SELECT * FROM disease_symptoms WHERE disease_id = ?",(int(id),))
    disease_symptoms = disease_symptoms.fetchall()
    disease_diagnosis = database_cursor.execute("SELECT * FROM disease_diagnosis WHERE disease_id = ?",(int(id),))
    disease_diagnosis = disease_diagnosis.fetchall()
    disease_treatment = database_cursor.execute("SELECT * FROM disease_treatment WHERE disease_id = ?",(int(id),))
    disease_treatment = disease_treatment.fetchall()
    disease_severity = database_cursor.execute("SELECT * FROM disease_severity WHERE disease_id = ?",(int(id),))
    disease_severity = disease_severity.fetchall()
    disease_faq = database_cursor.execute("SELECT * FROM disease_faq WHERE disease_id = ?",(int(id),))
    disease_faq = disease_faq.fetchall()
    doctors = disease_data[5].split(';')
    doctors_data = []
    for doctor in doctors:
        doctor_data = database_cursor.execute("SELECT * FROM doctors WHERE id = ?",(int(doctor),))
        doctor_data = doctor_data.fetchone()
        doctors_data.append(doctor_data)
    database_connection.commit()
    database_connection.close()
    return render_template('disease.html',social_links=social_links, disease_data=disease_data, specialty_name=specialty_name,
                           disease_profile=disease_profile, disease_types=disease_types, disease_causes=disease_causes,
                           doctors_data=doctors_data, disease_symptoms=disease_symptoms, disease_diagnosis=disease_diagnosis,
                           disease_severity=disease_severity, disease_treatment=disease_treatment, disease_faq=disease_faq,
                           navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/awards/')
def awards():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    data = database_cursor.execute("SELECT * FROM awards")
    data = data.fetchall()
    return render_template('awards.html', data=data,social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['lname']
        email = request.form['email']
        phone = request.form['number']
        message = request.form['message']
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        database_cursor.execute("INSERT INTO contact VALUES (?,?,?,?,?)", (first_name, last_name, email, phone, message))
        send_contact_mail(first_name+" "+last_name,email,message)
        database_connection.commit()
        database_connection.close()
        return render_template('contact.html',social_links=social_links, message="Your message has been sent successfully. We will contact you soon.", navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return render_template('contact.html',social_links=social_links, message=None, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/appointment/', methods=['GET', 'POST'])
def appointment():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        gender = request.form['gender']
        phone_number = request.form['number']
        appointment_type = request.form['appointment_type']
        message = request.form['message']
        # id = date(without -)+time(without :)+random
        #check if patient already exists
        patient = database_cursor.execute("SELECT * FROM patient WHERE email = ?", (email,))
        patient = patient.fetchone()
        if patient is None:
            #fetch last patient id
            exists = False
            last_patient_id = database_cursor.execute("SELECT id FROM patient ORDER BY id DESC LIMIT 1")
            last_patient_id = last_patient_id.fetchone()
            if last_patient_id is None:
                last_patient_id = 10000
                new_patient_id = last_patient_id + 1
            else:
                new_patient_id = int(last_patient_id[0]) + 1
            password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            database_cursor.execute("INSERT INTO patient VALUES (?,?,?,?,?,?,?)", (new_patient_id, first_name, last_name, phone_number, email, password, gender))
            database_connection.commit()
        else:
            exists = True
            new_patient_id = patient[0]
        #fetch last entered appointment id in database
        last_appointment_id = database_cursor.execute("SELECT * FROM appointment")
        last_appointment_id = last_appointment_id.fetchall()
        if len(last_appointment_id) == 0:
            new_appointment_id = str(new_patient_id) + "0001"
        else:
            #remove first 5 characters from last_appointment_id
            last_appointment_id = str(last_appointment_id[len(last_appointment_id)-1][8])[5:]
            new_appointment_id = str(new_patient_id) + str('{:0>4}'.format(int(last_appointment_id) + 1))
        database_cursor.execute("INSERT INTO appointment VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (first_name, last_name, gender, phone_number, email, appointment_type, message, 'pending',new_appointment_id,None, None, None, None, None))
        database_connection.commit()
        if exists:
            send_appointment_mail(first_name+" "+last_name,new_appointment_id,appointment_type, email, "")
        else:
            send_appointment_mail(first_name+" "+last_name,new_appointment_id,appointment_type, email, "Please login through your email ID: "+email+" and password. Your set password is: "+password)
        if 'patient_email' in session:
            patient_data = database_cursor.execute("SELECT first_name,last_name,mobile,email,gender FROM patient WHERE email=?", (session['patient_email'],))
            patient_data = patient_data.fetchone()
            database_connection.commit()
            database_connection.close()
            return render_template('appointment.html',social_links=social_links, message="Your appointment has been booked successfully. We will contact you soon. Your appointment ID is "+new_appointment_id, patient_data=patient_data, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        return render_template('appointment.html',social_links=social_links, message="Your appointment has been sent successfully. We will contact you soon. Your appointment ID is "+new_appointment_id, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    if 'patient_email' in session:
        patient_data = database_cursor.execute("SELECT first_name,last_name,mobile,email,gender FROM patient WHERE email=?", (session['patient_email'],))
        patient_data = patient_data.fetchone()
        return render_template('appointment.html',social_links=social_links, message=None, patient_data=patient_data, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return render_template('appointment.html',social_links=social_links, message=None, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

#bmr, calorie, exercise, break examination
@app.route('/bmi/', methods=['GET','POST'])
def bmi(): 
    if request.method == 'POST':
        age = request.form["age"]
        height = request.form["height"]
        weight = request.form["weight"]
        name = request.form["name"]
        email = request.form["email"]
        contact = request.form["contact"]
        bmi = float(weight) / (float(height)*0.01 * float(height)*0.01)
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        database_cursor.execute("INSERT INTO bmi VALUES (?,?,?,?,?,?,?)", (name, contact,email,age,height,weight,bmi))
        database_connection.commit()
        database_connection.close()
        return render_template('bmi.html', bmi = bmi, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return render_template('bmi.html', bmi = None, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/bmr/', methods=['GET','POST'])
def bmr():
    if request.method == 'POST':
        age = request.form["age"]
        height = request.form["height"]
        weight = request.form["weight"]
        name = request.form["name"]
        email = request.form["email"]
        contact = request.form["contact"]
        gender = request.form["gender"]
        if gender =="male":
            bmr = 10 * float(weight) + 6.25 * float(height) - 5 * float(age) + 5
        else:
            bmr = 10 * float(weight) + 6.25 * float(height) - 5 * float(age) - 161
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        database_cursor.execute("INSERT INTO bmr VALUES (?,?,?,?,?,?,?,?)", (name, contact,email,age,height,weight,gender,bmr))
        database_connection.commit()
        database_connection.close()
        return render_template('bmr.html', bmr = bmr, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return render_template('bmr.html', bmr = None, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

# @app.route('/calorie/', methods=['GET','POST'])
# def calorie():
#     if request.method == 'POST':
#         age = request.form["age"]
#         height = request.form["height"]
#         weight = request.form["weight"]
#         name = request.form["name"]
#         email = request.form["email"]
#         contact = request.form["contact"]
#         gender = request.form["gender"]
#         activity = request.form["activity"]
        

@app.route('/virtualTour/')
def virtualTour():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    data = database_cursor.execute("SELECT * FROM virtual_tour")
    data = data.fetchall()
    return render_template('virtualTour.html', data=data,social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/blogs/')
def blogs(): 
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    data = database_cursor.execute("SELECT image,title,description,id FROM blogs")
    data = data.fetchall()
    return render_template('blogs.html', data=data,social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/blog/<string:id>/')
def blog(id):
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    data = database_cursor.execute("SELECT * FROM blogs WHERE id=?", (id,))
    data = data.fetchone()
    if data is None:
        database_connection.commit()
        database_connection.close()
        return redirect(url_for('index'))
    data = list(data)
    data[4] = data[4].replace("\r","\n")
    data[4] = data[4].split('\n\n')
    return render_template('blog.html', data=data,social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/news/')
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
    return render_template('news.html', data=data, latest_news=latest_news,social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

#backend

@app.route('/admin/')
def adminHome():
    if 'user' in session:
        return render_template('adminHome.html', social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('login'))

@app.route('/manageAppointments/')
def manageAppointments():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        pending_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'pending'")
        pending_appointments = pending_appointments.fetchmany(3)
        approved_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'approved'")
        approved_appointments = approved_appointments.fetchmany(3)
        completed_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'completed'")
        completed_appointments = completed_appointments.fetchmany(3)
        declined_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'declined'")
        declined_appointments = declined_appointments.fetchmany(3)
        database_connection.commit()
        database_connection.close()
        return render_template('manageAppointments.html', social_links=social_links, pending_appointments=pending_appointments, approved_appointments=approved_appointments, completed_appointments=completed_appointments, declined_appointments=declined_appointments, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    elif 'patient_email' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        pending_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'pending' AND email_ID = ?", (session["patient_email"],))
        pending_appointments = pending_appointments.fetchall()
        approved_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'approved' AND email_ID = ?", (session["patient_email"],))
        approved_appointments = approved_appointments.fetchall()
        completed_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'completed' AND email_ID = ?", (session["patient_email"],))
        completed_appointments = completed_appointments.fetchall()
        declined_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'declined' AND email_ID = ?", (session["patient_email"],))
        declined_appointments = declined_appointments.fetchall()
        database_connection.commit()
        database_connection.close()
        return render_template('manageAppointments.html', social_links=social_links, pending_appointments=pending_appointments, approved_appointments=approved_appointments, completed_appointments=completed_appointments, declined_appointments=declined_appointments, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    else:
        return redirect(url_for('patientLogin'))

@app.route('/manageAppointments/<string:status>/')
def manageStatusAppointments(status):
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        if status == 'pending':
            pending_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'pending'")
            pending_appointments = pending_appointments.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template('manageStatusAppointments.html', social_links=social_links, appointments=pending_appointments, status=status, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        elif status == 'approved':
            approved_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'approved'")
            approved_appointments = approved_appointments.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template('manageStatusAppointments.html', social_links=social_links, appointments=approved_appointments, status=status, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        elif status == 'completed':
            completed_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'completed'")
            completed_appointments = completed_appointments.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template('manageStatusAppointments.html', social_links=social_links, appointments=completed_appointments, status=status, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        elif status == 'declined':
            declined_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'declined'")
            declined_appointments = declined_appointments.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template('manageStatusAppointments.html', social_links=social_links, appointments=declined_appointments, status=status, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    elif 'patient_email' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        if status == 'pending':
            pending_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'pending' AND email_ID = ?", (session["patient_email"],))
            pending_appointments = pending_appointments.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template('manageStatusAppointments.html', social_links=social_links, appointments=pending_appointments, status=status, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        elif status == 'approved':
            approved_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'approved' AND email_ID = ?", (session["patient_email"],))
            approved_appointments = approved_appointments.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template('manageStatusAppointments.html', social_links=social_links, appointments=approved_appointments, status=status, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        elif status == 'completed':
            completed_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'completed' AND email_ID = ?", (session["patient_email"],))
            completed_appointments = completed_appointments.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template('manageStatusAppointments.html', social_links=social_links, appointments=completed_appointments, status=status, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        elif status == 'declined':
            declined_appointments = database_cursor.execute("SELECT * FROM appointment WHERE status = 'declined' AND email_ID = ?", (session["patient_email"],))
            declined_appointments = declined_appointments.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template('manageStatusAppointments.html', social_links=social_links, appointments=declined_appointments, status=status, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route('/viewAppointment/<string:appointment_id>/')
def viewAppointment(appointment_id):
    if 'user' in session or 'patient_email' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        appointment = database_cursor.execute("SELECT * FROM appointment WHERE id = ?", (appointment_id,))
        appointment = appointment.fetchone()
        doctor_name = None
        if appointment[13] is not None:
            doctor_name = database_cursor.execute("SELECT name FROM doctors WHERE id = ?", (appointment[13],))
            doctor_name = doctor_name.fetchone()
            doctor_name = doctor_name[0]
        if appointment[7] == 'pending':
            doctors = database_cursor.execute("SELECT id, name FROM doctors")
            doctors = doctors.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template('viewAppointment.html', social_links=social_links, appointment=appointment, doctor_name=doctor_name, doctors=doctors, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        return render_template('viewAppointment.html', social_links=social_links, appointment=appointment, doctor_name=doctor_name, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route('/deleteAppointment/<string:appointment_id>/')
def deleteAppointment(appointment_id):
    if 'patient_email' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        database_cursor.execute("DELETE FROM appointment WHERE id = ?", (int(appointment_id),))
        database_connection.commit()
        database_connection.close()
        return redirect(url_for('manageAppointments'))
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        database_cursor.execute("DELETE FROM appointment WHERE id = ?", (int(appointment_id),))
        database_connection.commit()
        database_connection.close()
        return redirect(url_for('manageStatusAppointments', status='pending'))
    return redirect(url_for('patientLogin'))

@app.route('/approveAppointment/<string:appointment_id>/', methods=['POST'])
def approveAppointment(appointment_id):
    if 'user' in session and request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        doctor = request.form['doctor']
        message = request.form['message']
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        database_cursor.execute("UPDATE appointment SET status = 'approved', doctor_id = ?, date = ?, time = ? WHERE id = ?", (int(doctor),str(date),str(time),int(appointment_id)))
        if message != '':
            database_cursor.execute("UPDATE appointment SET hospital_message = ? WHERE id = ?", (message, int(appointment_id)))
        appointment_details = database_cursor.execute("SELECT * FROM appointment WHERE id = ?", (int(appointment_id),))
        appointment_details = appointment_details.fetchone()
        send_approval_mail(appointment_details[4],appointment_details[0]+" "+appointment_details[1],appointment_id,appointment_details[5],date,time,message)
        database_connection.commit()
        database_connection.close()
        return redirect(url_for('viewAppointment', appointment_id=appointment_id))
    return redirect(url_for('patientLogin'))

@app.route('/completeAppointment/<string:appointment_id>/')
def completeAppointment(appointment_id):
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        database_cursor.execute("UPDATE appointment SET status = 'completed' WHERE id = ?", (int(appointment_id),))
        appointment_details = database_cursor.execute("SELECT * FROM appointment WHERE id = ?", (int(appointment_id),))
        appointment_details = appointment_details.fetchone()
        database_connection.commit()
        database_connection.close()
        send_completed_mail(appointment_details[4],appointment_details[0]+" "+appointment_details[1],appointment_id,"https://www.ehcchospital.in/viewAppointment/"+appointment_id)
        return redirect(url_for('viewAppointment', appointment_id=appointment_id))
    return redirect(url_for('patientLogin'))

@app.route('/declineAppointment/<string:appointment_id>/', methods=['POST'])
def declineAppointment(appointment_id):
    if 'user' in session and request.method == 'POST':
        message = request.form['message']
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        database_cursor.execute("UPDATE appointment SET status = 'declined', hospital_message = ? WHERE id = ?", (message, int(appointment_id),))
        appointment_details = database_cursor.execute("SELECT * FROM appointment WHERE id = ?", (int(appointment_id),))
        appointment_details = appointment_details.fetchone()
        database_connection.commit()
        database_connection.close()
        send_declined_mail(appointment_details[4],appointment_details[0]+" "+appointment_details[1],appointment_id,message)
        return redirect(url_for('viewAppointment', appointment_id=appointment_id))
    return redirect(url_for('patientLogin'))

@app.route('/uploadDocument/<string:appointment_id>/', methods=['POST'])
def uploadDocument(appointment_id):
    if 'user' in session and request.method == 'POST':
        file = request.files['document']
        # set the file name to the appointment id
        new_file_name = appointment_id +"."+ file.filename.split('.')[1]
        file.save(os.path.join(UPLOAD_FOLDER,new_file_name))
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        database_cursor.execute("UPDATE appointment SET documents = ? WHERE id = ?", (new_file_name, int(appointment_id),))
        # get email from appointment
        email = database_cursor.execute("SELECT email_ID FROM appointment WHERE id = ?", (int(appointment_id),))
        email = email.fetchone()[0]
        #get patient name
        name = database_cursor.execute("SELECT first_name, last_name FROM patient WHERE email = ?", (email,))
        name = name.fetchone()
        name = name[0] + " " + name[1]
        send_document_upload_mail(name,email,appointment_id,"https://www.ehcchospital.in/viewAppointment/"+appointment_id)
        database_connection.commit()
        database_connection.close()
        return redirect(url_for('viewAppointment', appointment_id=appointment_id))
    return redirect(url_for('patientLogin'))

@app.route('/deleteDocument/<string:appointment_id>/')
def deleteDocument(appointment_id):
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        filename = database_cursor.execute("SELECT documents FROM appointment WHERE id = ?", (int(appointment_id),))
        filename = filename.fetchone()[0]
        os.remove(os.path.join(UPLOAD_FOLDER,filename))
        database_cursor.execute("UPDATE appointment SET documents = ? WHERE id = ?", (None,int(appointment_id),))
        database_connection.commit()
        database_connection.close()
        return redirect(url_for('viewAppointment', appointment_id=appointment_id))
    return redirect(url_for('patientLogin'))
                  
@app.route('/modifyPages/')
def modifyPages():
    if 'user' in session:
        return render_template('modifyPages.html', social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route('/addPages/')
def addPages():
    if 'user' in session:
        return render_template('addPages.html', social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route('/addDoctor/', methods=['POST', 'GET'])
def addDoctor():
    if 'user' in session:
        if request.method == 'POST':
            doctor_name = request.form['doctor_name']
            doctor_current_appointment = request.form['doctor_current_appointment']
            doctor_image = request.files['doctor_image']
            doctor_qualification = request.form['doctor_qualification']
            doctor_post_qualification = request.form['doctor_post_qualification']
            doctor_overseas_qualification = request.form['doctor_overseas_qualification']
            doctor_about = request.form['doctor_about']
            doctor_degree = []
            for i in range(3):
                temp = []
                temp.append(request.form['doctor_degree'+str(i+1)])
                temp.append(request.form['doctor_institute'+str(i+1)])
                temp.append(request.form['doctor_year'+str(i+1)])
                doctor_degree.append(temp)
            doctor_experience = []
            for i in range(3):
                temp = []
                temp.append(request.form['doctor_organization'+str(i+1)])
                temp.append(request.form['doctor_experience_from_year'+str(i+1)])
                temp.append(request.form['doctor_experience_to_year'+str(i+1)])
                doctor_experience.append(temp)
            #fetch last id
            database_connection = sqlite3.connect(database_location)
            database_cursor = database_connection.cursor()
            last_id = database_cursor.execute("SELECT id FROM doctors ORDER BY id DESC LIMIT 1")
            last_id = last_id.fetchone()
            if last_id is None:
                last_id = 0
            else:
                last_id = last_id[0]
            doctor_image_filename = "doctor_"+str(last_id+1)+"."+doctor_image.filename.split('.')[1]
            doctor_image.save(os.path.join(DOCTOR_FOLDER,doctor_image_filename))
            database_cursor.execute("INSERT INTO doctors VALUES (?,?,?,?)", (last_id+1,doctor_name,doctor_current_appointment,"../../static/images/doctors/"+doctor_image_filename))
            database_cursor.execute("INSERT INTO doctor_profile VALUES (?,?,?,?,?,?)", (last_id+1,doctor_qualification,doctor_post_qualification, doctor_overseas_qualification, doctor_current_appointment, doctor_about))
            for i in range(3):
                database_cursor.execute("INSERT INTO doctor_degree VALUES (?,?,?,?)", (last_id+1,doctor_degree[i][0],doctor_degree[i][1],doctor_degree[i][2]))
                database_cursor.execute("INSERT INTO doctor_experience VALUES (?,?,?,?)", (last_id+1,doctor_experience[i][0],doctor_experience[i][1],doctor_experience[i][2]))
            database_connection.commit()
            return render_template('addDoctor.html', social_links=social_links, message="Doctor Added Successfully", navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        return render_template('addDoctor.html', social_links=social_links, message=None, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route('/addSpecialty/', methods=['POST', 'GET'])
def addSpecialty():
    if 'user' in session:
        if request.method == "POST":
            name = request.form['specialty_name']
            description = request.form['specialty_description']
            illustration = request.files['specialty_illustration']
            #fetch last id
            database_connection = sqlite3.connect(database_location)
            database_cursor = database_connection.cursor()
            last_id = database_cursor.execute("SELECT id FROM specialty ORDER BY id DESC LIMIT 1")
            last_id = last_id.fetchone()
            if last_id is None:
                last_id = 0
            else:
                last_id = last_id[0]
            illustration_filename = "specialty_"+str(last_id+1)+"."+illustration.filename.split('.')[1]
            illustration.save(os.path.join(SPECIALTY_FOLDER,illustration_filename))
            database_cursor.execute("INSERT INTO specialty VALUES (?,?,?,?)", (last_id+1,name,description,"../../static/images/illustrations/specialty/"+illustration_filename))
            database_connection.commit()
            database_connection.close()
            return render_template('addSpecialty.html', social_links=social_links, message="Specialty Added Successfully", navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        return render_template('addSpecialty.html', social_links=social_links, message=None, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route('/addDisease/', methods=['POST', 'GET'])
def addDisease():
    if 'user' in session:
        # fetch all specialties
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        specialties = database_cursor.execute("SELECT id,name FROM specialty")
        specialties = specialties.fetchall()
        doctors = database_cursor.execute("SELECT id,name FROM doctors")
        doctors = doctors.fetchall()
        if request.method == "POST":
            specialty_id = request.form['specialty_name']
            disease_title = request.form['disease_title']
            disease_description = request.form['disease_description']
            disease_illustration = request.files['disease_illustration']
            doctors_disease = request.form.getlist('doctors')
            main_image = request.files['main_image']
            disease_profile_title1 = request.form['disease_profile_title1']
            disease_profile_content1 = request.form['disease_profile_content1']
            disease_profile_title2 = request.form['disease_profile_title2']
            disease_content2 = request.form['disease_profile_content1']
            disease_type_title1 = request.form['disease_type_title1']
            disease_type_description1 = request.form['disease_type_description1']
            disease_type_image1 = request.files['disease_type_image1']
            disease_type_title2 = request.form['disease_type_title2']
            disease_type_description2 = request.form['disease_type_description2']
            disease_type_image2 = request.files['disease_type_image2']
            causes = request.form['disease_causes']
            symptoms = request.form['disease_symptoms']
            disease_diagnosis_type1 = request.form['disease_diagnosis_type1']
            disease_diagnosis_description1 = request.form['disease_diagnosis_description1']
            disease_diagnosis_type2 = request.form['disease_diagnosis_type2']
            disease_description2 = request.form['disease_diagnosis_description1']
            disease_severity_type1 = request.form['disease_severity_type1']
            disease_severity_description1 = request.form['disease_severity_description1']
            disease_severity_type2 = request.form['disease_severity_type2']
            disease_severity_description2 = request.form['disease_severity_description2']
            disease_treatment_type1 = request.form['disease_treatment_type1']
            disease_treatment_description1 = request.form['disease_treatment_description1']
            disease_treatment_type2 = request.form['disease_treatment_type2']
            disease_treatment_description2 = request.form['disease_treatment_description2']
            # fetch last id
            last_id = database_cursor.execute("SELECT id FROM diseases ORDER BY id DESC LIMIT 1")
            last_id = last_id.fetchone()
            if last_id is None:
                last_id = 0
            else:
                last_id = last_id[0]
            disease_illustration_filename = "disease_"+str(last_id+1)+"."+disease_illustration.filename.split('.')[1]
            disease_illustration.save(os.path.join(DISEASES_ILLUSTRATION_FOLDER,disease_illustration_filename))
            main_image_filename = "disease_img"+str(last_id+1)+"."+main_image.filename.split('.')[1]
            main_image.save(os.path.join(DISEASES_FOLDER,main_image_filename))
            disease_type_image1_filename = "disease_type_img1_"+str(last_id+1)+"."+disease_type_image1.filename.split('.')[1]
            disease_type_image1.save(os.path.join(DISEASES_FOLDER,disease_type_image1_filename))
            disease_type_image2_filename = "disease_type_img2_"+str(last_id+1)+"."+disease_type_image2.filename.split('.')[1]
            disease_type_image2.save(os.path.join(DISEASES_FOLDER,disease_type_image2_filename))
            database_cursor.execute("INSERT INTO diseases VALUES (?,?,?,?,?,?,?)", (last_id+1,disease_title,specialty_id,disease_description,"../../static/images/illustrations/diseases/"+disease_illustration_filename,';'.join(doctors_disease),"../../static/images/disease/"+main_image_filename))
            database_cursor.execute("INSERT INTO disease_profile VALUES (?,?,?)", (last_id+1,disease_profile_title1,disease_profile_content1))
            database_cursor.execute("INSERT INTO disease_profile VALUES (?,?,?)", (last_id+1,disease_profile_title2,disease_content2))
            database_cursor.execute("INSERT INTO disease_types VALUES (?,?,?,?)", (last_id+1,disease_type_title1,disease_type_description1,"../../static/images/disease/"+disease_type_image1_filename))
            database_cursor.execute("INSERT INTO disease_types VALUES (?,?,?,?)", (last_id+1,disease_type_title2,disease_type_description2,"../../static/images/disease/"+disease_type_image2_filename))
            causes = causes.split(';')
            for cause in causes:
                database_cursor.execute("INSERT INTO disease_causes VALUES (?,?)", (last_id+1,cause))
            symptoms = symptoms.split(';')
            for symptom in symptoms:
                database_cursor.execute("INSERT INTO disease_symptoms VALUES (?,?)", (last_id+1,symptom))
            database_cursor.execute("INSERT INTO disease_diagnosis VALUES (?,?,?)", (last_id+1,disease_diagnosis_type1,disease_diagnosis_description1))
            database_cursor.execute("INSERT INTO disease_diagnosis VALUES (?,?,?)", (last_id+1,disease_diagnosis_type2,disease_description2))
            database_cursor.execute("INSERT INTO disease_severity VALUES (?,?,?)", (last_id+1,disease_severity_type1,disease_severity_description1))
            database_cursor.execute("INSERT INTO disease_severity VALUES (?,?,?)", (last_id+1,disease_severity_type2,disease_severity_description2))
            database_cursor.execute("INSERT INTO disease_treatment VALUES (?,?,?)", (last_id+1,disease_treatment_type1,disease_treatment_description1))
            database_cursor.execute("INSERT INTO disease_treatment VALUES (?,?,?)", (last_id+1,disease_treatment_type2,disease_treatment_description2))
            database_connection.commit()
            database_connection.close()
            return render_template('addDisease.html', social_links=social_links, specialties=specialties, doctors=doctors, message="Disease Added Successfully",navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        database_connection.close()
        return render_template('addDisease.html', social_links=social_links, doctors=doctors, specialties=specialties, message=None,navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))
  
@app.route('/addVirtualTour/', methods=['POST', 'GET'])
def addVirtualTour():
    if 'user' in session:
        if request.method == "POST":
            title = request.form['vt_title']
            description = request.form['vt_description']
            image = request.files['vt_image']
            #fetch last id
            database_connection = sqlite3.connect(database_location)
            database_cursor = database_connection.cursor()
            last_id = database_cursor.execute("SELECT id FROM virtual_tour ORDER BY id DESC LIMIT 1")
            last_id = last_id.fetchone()
            if last_id is None:
                last_id = 0
            else:
                last_id = last_id[0]
            image_filename = "vt_"+str(last_id+1)+"."+image.filename.split('.')[1]
            image.save(os.path.join(VIRTUAL_TOUR_FOLDER,image_filename))
            database_cursor.execute("INSERT INTO virtual_tour VALUES (?,?,?,?)", ("../../static/images/virtual_tour/"+image_filename,title,description,last_id+1))
            database_connection.commit()
            database_connection.close()
            return render_template('addVirtualTour.html', social_links=social_links, message="Specialty Added Successfully", navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        return render_template('addVirtualTour.html', social_links=social_links, message=None, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route('/addAward/', methods=['POST', 'GET'])
def addAward():
    if 'user' in session:
        if request.method == "POST":
            award_type = request.form['award_type']
            title = request.form['award_title']
            description = request.form['award_description']
            image = request.files['award_image']
            #fetch last id
            database_connection = sqlite3.connect(database_location)
            database_cursor = database_connection.cursor()
            last_id = database_cursor.execute("SELECT id FROM awards ORDER BY id DESC LIMIT 1")
            last_id = last_id.fetchone()
            if last_id is None:
                last_id = 0
            else:
                last_id = last_id[0]
            image_filename = "award_"+str(last_id+1)+"."+image.filename.split('.')[1]
            image.save(os.path.join(AWARDS_FOLDER,image_filename))
            database_cursor.execute("INSERT INTO awards VALUES (?,?,?,?,?)", (award_type,title,description,"../../static/images/awards/"+image_filename,last_id+1))
            database_connection.commit()
            database_connection.close()
            return render_template('addAward.html', social_links=social_links, message="Award Added Successfully",navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        return render_template('addAward.html', social_links=social_links, message=None,navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))
      
@app.route('/addNews/', methods=['POST', 'GET'])
def addNews():
    if 'user' in session:
        if request.method == "POST":
            title = request.form['news_title']
            # check if is_head is checked
            if 'is_head' in request.form:
                is_head = "yes"
                news_heading = request.form['news_heading']
            else:
                is_head = "no"
            news_description = request.form['news_description']
            news_image = request.files['news_image']
            #fetch last id
            database_connection = sqlite3.connect(database_location)
            database_cursor = database_connection.cursor()
            last_id = database_cursor.execute("SELECT id FROM news ORDER BY id DESC LIMIT 1")
            last_id = last_id.fetchone()
            if last_id is None:
                last_id = 0
            else:
                last_id = last_id[0]
            if is_head == "yes":
                image_filename = "head_news_"+str(last_id+1)+"."+news_image.filename.split('.')[1]
                news_image.save(os.path.join(HEAD_NEWS_FOLDER,image_filename))
                database_cursor.execute("INSERT INTO news VALUES (?,?,?,?,?,?)", ("../../static/images/news/head_news/"+image_filename,title,news_heading,news_description,is_head,last_id+1))
            else:
                image_filename = "news_"+str(last_id+1)+"."+news_image.filename.split('.')[1]
                news_image.save(os.path.join(NEWS_FOLDER,image_filename))
                database_cursor.execute("INSERT INTO news VALUES (?,?,?,?,?,?)", ("../../static/images/news/"+image_filename,title,None,news_description,is_head,last_id+1))
            database_connection.commit()
            database_connection.close()
            return render_template('addNews.html', social_links=social_links, message="News Added Successfully",navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        return render_template('addNews.html', social_links=social_links, message=None,navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/addBlog/', methods=['POST', 'GET'])
def addBlog():
    if 'user' in session:
        if request.method == "POST":
            title = request.form['blog_title']
            description = request.form['blog_description']
            blog_image = request.files['blog_image']
            blog_content = request.form['blog_content']
            #fetch last id
            database_connection = sqlite3.connect(database_location)
            database_cursor = database_connection.cursor()
            last_id = database_cursor.execute("SELECT id FROM blogs ORDER BY id DESC LIMIT 1")
            last_id = last_id.fetchone()
            if last_id is None:
                last_id = 0
            else:
                last_id = last_id[0]
            image_filename = "blog_"+str(last_id+1)+"."+blog_image.filename.split('.')[1]
            blog_image.save(os.path.join(BLOGS_FOLDER,image_filename))
            database_cursor.execute("INSERT INTO blogs VALUES (?,?,?,?,?)", ("../../static/images/blogs/"+image_filename,title,description,last_id+1,blog_content))
            database_connection.commit()
            database_connection.close()
            return render_template('addBlog.html', social_links=social_links, message="Blog Added Successfully",navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        return render_template('addBlog.html', social_links=social_links, message=None,navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/addTestimonial/', methods=['POST', 'GET'])
def addTestimonial():
    if 'user' in session:
        if request.method == "POST":
            name = request.form["person_name"]
            designation = request.form["person_designation"]
            testimonial = request.form["person_testimonial"]
            image = request.files["person_image"]
            #fetch last id
            database_connection = sqlite3.connect(database_location)
            database_cursor = database_connection.cursor()
            last_id = database_cursor.execute("SELECT id FROM testimonials ORDER BY id DESC LIMIT 1")
            last_id = last_id.fetchone()
            if last_id is None:
                last_id = 0
            else:
                last_id = last_id[0]
            image_filename = "testimonial_"+str(last_id+1)+"."+image.filename.split('.')[1]
            image.save(os.path.join(TESTIMONIALS_FOLDER,image_filename))
            database_cursor.execute("INSERT INTO testimonials VALUES (?,?,?,?,?)", (last_id+1, name, designation, "\""+testimonial+"\"", "../../static/images/testimonial/"+image_filename))
            database_connection.commit()
            database_connection.close()
            return render_template('addTestimonial.html', social_links=social_links, message="Testimonial Added Successfully",navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        return render_template('addTestimonial.html', social_links=social_links, message=None,navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/addFAQ/', methods=["POST","GET"])
def addFAQs():
    if 'user' in session:
        if request.method == "POST":
            question = request.form["faq_question"]
            answer = request.form["faq_answer"]
            database_connection = sqlite3.connect(database_location)
            database_cursor = database_connection.cursor()
            database_cursor.execute("INSERT INTO home_faq VALUES (?,?)", (question,answer))
            database_connection.commit()
            database_connection.close()
            return render_template('addFAQ.html', social_links=social_links, message="FAQ Added Successfully",navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        return render_template('addFAQ.html', social_links=social_links, message=None,navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        
@app.route('/adminLogin/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        data = database_cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        data = data.fetchone()
        if data is None:
             return render_template('adminLogin.html', social_links=social_links, message="Invalid Credentials", navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        else:
            session['user'] = data[0]
            session['user_type'] = data[2]
            return redirect(url_for('adminHome'))
    if 'user' in session:
        return redirect(url_for('adminHome'))
    return render_template('adminLogin.html', social_links=social_links, message=None, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/logoutAdmin/')
def logout():
    session.pop('user', None)
    session.pop('user_type', None)
    return redirect(url_for('login'))

@app.route('/modifyHome/', methods=['GET', 'POST'])
def modifyHome():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        if request.method == 'POST':
            #carousel
            carousel_items = database_cursor.execute("SELECT id FROM home_carousel")
            carousel_items = carousel_items.fetchone()
            carousel = []
            for i in range(len(carousel_items)):
                temp = []
                carousel_heading = request.form['carousel_heading_'+str(carousel_items[i])]
                carousel_description = request.form['carousel_description_'+str(carousel_items[i])]
                carousel_image = request.files['carousel_image_'+str(carousel_items[i])]
                temp.append(carousel_heading)
                temp.append(carousel_description)
                if carousel_image.filename != '':
                    image_filename = "carousel_"+str(carousel_items[i])+"."+carousel_image.filename.split('.')[1]
                    carousel_image.save(os.path.join(HOME_CAROUSEL_FOLDER,image_filename))
                    temp.append("../../static/images/Homepage/"+image_filename)
                carousel.append(temp)
            for i in range(len(carousel_items)):
                if len(carousel[i]) == 3:
                    database_cursor.execute("UPDATE home_carousel SET heading=?, description=?, image = ? WHERE id=?;", (carousel[i][0], carousel[i][1], carousel[i][2], carousel_items[i]))
                else:
                    database_cursor.execute("UPDATE home_carousel SET heading=?, description=? WHERE id=?;", (carousel[i][0], carousel[i][1], carousel_items[i]))
            #about
            about_heading = request.form['about_heading']
            about_description = request.form['about_description']
            about_image_new = request.files['about_image']
            about_image_old = database_cursor.execute("SELECT about_image FROM home_page;")
            about_image_old = about_image_old.fetchone()[0]
            database_cursor.execute("UPDATE home_page SET about_heading=?, about_description=? WHERE about_image=?;", (about_heading, about_description, about_image_old))
            database_connection.commit()
            if about_image_new.filename != '':
                about_image_new.save(os.path.join(HOME_CAROUSEL_FOLDER,about_image_new.filename))
                about_image_new = "../../static/images/Homepage/"+about_image_new.filename
                database_cursor.execute("UPDATE home_page SET about_image=? WHERE about_image = ?", (about_image_new,about_image_old))
            database_connection.commit()
            
            #statistics
            statistics_items = database_cursor.execute("SELECT id FROM home_statistics;")
            statistics_items = statistics_items.fetchone()
            statistics = []
            for i in range(len(statistics_items)):
                temp = []
                statistics_heading = request.form['statistics_heading_'+str(statistics_items[i])]
                statistics_description = request.form['statistics_description_'+str(statistics_items[i])]
                temp.append(statistics_heading)
                temp.append(statistics_description)
                statistics.append(temp)
            for i in range(len(statistics_items)):
                database_cursor.execute("UPDATE home_statistics SET title=?, count=? WHERE id=?;", (statistics[i][0], statistics[i][1], statistics_items[i]))
            database_connection.commit()
            
            #faqs
            faq_items = database_cursor.execute("SELECT id FROM home_faq;")
            faq_items = faq_items.fetchall()
            faqs = []
            for i in range(len(faq_items)):
                temp = []
                faq_question = request.form['faq_question_'+str(faq_items[i][0])]
                faq_answer = request.form['faq_answer_'+str(faq_items[i][0])]
                temp.append(faq_question)
                temp.append(faq_answer)
                faqs.append(temp)
            for i in range(len(faq_items)):
                database_cursor.execute("UPDATE home_faq SET question=?, answer=? WHERE id=?;", (faqs[i][0], faqs[i][1], faq_items[i][0]))
            database_connection.commit()   
            
            carousel_data = database_cursor.execute("SELECT * FROM home_carousel")
            carousel_data = carousel_data.fetchall()
            about = database_cursor.execute("SELECT * FROM home_page")
            about = about.fetchone()
            statistics = database_cursor.execute("SELECT * FROM home_statistics")
            statistics = statistics.fetchall()
            faqs = database_cursor.execute("SELECT * FROM home_faq")
            faqs = faqs.fetchall()
            database_connection.close()
            return render_template('modifyHome.html', social_links = social_links, faqs=faqs, about=about, carousel_data = carousel_data, message = "Details updated successfully.", navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        else:
            carousel_data = database_cursor.execute("SELECT * FROM home_carousel")
            carousel_data = carousel_data.fetchall()
            about = database_cursor.execute("SELECT * FROM home_page")
            about = about.fetchone()
            statistics = database_cursor.execute("SELECT * FROM home_statistics")
            statistics = statistics.fetchall()
            faqs = database_cursor.execute("SELECT * FROM home_faq")
            faqs = faqs.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template('modifyHome.html', social_links = social_links, faqs=faqs, about=about, carousel_data = carousel_data, statistics=statistics, message = None, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route('/modifySpecialty/', methods=['GET', 'POST'])
def modifySpecialty():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        if request.method == "POST":
            specialty_id = request.form['specialty_id']
            specialty_name = request.form["specialty_name"]
            specialty_description = request.form["specialty_description"]
            specialty_illustration = request.files["specialty_illustration"]
            if specialty_illustration.filename != '':
                illustration_filename = "specialty_"+str(specialty_id)+"."+specialty_illustration.filename.split('.')[1]
                specialty_illustration.save(os.path.join(SPECIALTY_FOLDER,illustration_filename))
                specialty_illustration = "../../static/images/illustrations/specialty/"+illustration_filename
                database_cursor.execute("UPDATE specialty SET name=?, description=?, illustration=? WHERE id=?;", (specialty_name, specialty_description, specialty_illustration, specialty_id))
            else:
                specialty_illustration = database_cursor.execute("SELECT illustration FROM specialty WHERE id=?;", (specialty_id,))
                specialty_illustration = specialty_illustration.fetchone()[0]
                database_cursor.execute("UPDATE specialty SET name=?, description=? WHERE id=?;", (specialty_name, specialty_description, specialty_id))
            specialty_main = database_cursor.execute("SELECT * FROM specialty")
            specialty_main = specialty_main.fetchall() 
            database_connection.commit()
            database_connection.close()
            return render_template('modifySpecialty.html', specialty_main=specialty_main, message = "Specialty updated successfully.", navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        specialty_main = database_cursor.execute("SELECT * FROM specialty")
        specialty_main = specialty_main.fetchall() 
        database_connection.commit()
        database_connection.close()
        return render_template('modifySpecialty.html', specialty_main=specialty_main, message = None, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))
        

@app.route("/modifyTestimonial/", methods=['GET', 'POST'])
def modifyTestimonial():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        if request.method == "POST":
            testimonial_id = request.form["testimonial_id"]
            testimonial_name = request.form["testimonial_name"]
            testimonial_designation = request.form["testimonial_designation"]
            testimonial_content = request.form["testimonial_content"]
            testimonial_image = request.files["testimonial_image"]
            if testimonial_image.filename != "" and testimonial_image.filename is not None:
                previous_image = database_cursor.execute("SELECT image FROM testimonials WHERE id = ?", (int(testimonial_id),)).fetchone()[0]
                os.remove(os.path.join(THIS_FOLDER,previous_image.replace("../","")))
                testimonial_image_filepath = "testimonial_"+ testimonial_id+ "."  + testimonial_image.filename.split(".")[1]
                testimonial_image.save(os.path.join(TESTIMONIALS_FOLDER,"testimonial_"+ testimonial_id + "." + testimonial_image.filename.split(".")[1]))
                database_cursor.execute("UPDATE testimonials SET name=?, designation=?, content = ?, image=? WHERE id=?;", (testimonial_name, testimonial_designation,testimonial_content, "../static/images/testimonial/"+testimonial_image_filepath, testimonial_id))
            else:
                database_cursor.execute("UPDATE testimonials SET name = ?, designation = ?, content = ? WHERE id = ?", (testimonial_name, testimonial_designation,testimonial_content, int(testimonial_id)))
            testimonials_main = database_cursor.execute("SELECT id, name FROM testimonials")
            testimonials_main = testimonials_main.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template('modifyTestimonial.html', testimonials_main = testimonials_main, message = "Testimonial updated successfully.",social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        testimonials_main = database_cursor.execute("SELECT id, name FROM testimonials")
        testimonials_main = testimonials_main.fetchall() 
        database_connection.commit()
        database_connection.close()  
        return render_template("modifyTestimonial.html",testimonials_main=testimonials_main, message=None, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route("/getTestimonial/<string:id>/")
def getTestimonial(id):
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    testimonial = database_cursor.execute("SELECT * FROM testimonials WHERE id = ?", (int(id),))
    testimonial = testimonial.fetchone()
    if testimonial is not None:
        testimonial = list(testimonial)
        json_data = json.dumps(testimonial)
        database_connection.commit()
        database_connection.close()
        return json_data
    return "No data found"

@app.route("/deleteTestimonial/",methods=["POST","GET"])
def deleteTestimonial():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        if request.method == "POST":
            testimonial_id = request.form["testimonial_id"]
            previous_image = database_cursor.execute("SELECT image FROM testimonials WHERE id = ?", (int(testimonial_id),)).fetchone()[0]
            os.remove(os.path.join(THIS_FOLDER,previous_image.replace("../","")))
            database_cursor.execute("DELETE FROM testimonials WHERE id = ?", (int(testimonial_id),))
            testimonials_main = database_cursor.execute("SELECT * FROM testimonials")
            testimonials_main = testimonials_main.fetchall() 
            database_connection.commit()
            database_connection.close()
            return render_template("deleteTestimonial.html", testimonials_main = testimonials_main, message = "Testimonial Deleted successfully", social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        testimonials_main = database_cursor.execute("SELECT * FROM testimonials")
        testimonials_main = testimonials_main.fetchall() 
        database_connection.commit()
        database_connection.close()
        return render_template("deleteTestimonial.html", testimonials_main = testimonials_main, message = None, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route("/deleteCarousel/<string:carousel_id>/")
def deleteCarousel(carousel_id):
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        filename = database_cursor.execute("SELECT image FROM home_carousel WHERE id = ?", (int(carousel_id),))
        filename = filename.fetchone()[0]
        os.remove(os.path.join(THIS_FOLDER,filename.replace("../../","")))
        database_cursor.execute("DELETE FROM home_carousel WHERE id = ?", (int(carousel_id),))
        database_connection.commit()
        database_connection.close()
        return redirect(url_for('modifyHome'))
    return redirect(url_for('patientLogin'))

@app.route("/deleteStatistic/<string:statistic_id>/")
def deleteStatistic(statistic_id):
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        database_cursor.execute("DELETE FROM home_statistics WHERE id = ?", (int(statistic_id),))
        database_connection.commit()
        database_connection.close()
        return redirect(url_for('modifyHome'))
    return redirect(url_for('patientLogin'))


@app.route("/deleteFAQ/<string:faq_id>/")
def deleteFAQ(faq_id):
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        database_cursor.execute("DELETE FROM home_faq WHERE id = ?", (int(faq_id),))
        database_connection.commit()
        database_connection.close()
        return redirect(url_for('modifyHome'))
    return redirect(url_for('patientLogin'))

@app.route('/modifyAbout/', methods=['GET', 'POST'])
def modifyAbout():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        if request.method == 'POST':
            hero_title = request.form['hero_title']
            hero_description = request.form['hero_description']
            vision = request.form['vision']
            mission = request.form['mission']
            values = request.form['values']
            database_cursor.execute("UPDATE about SET hero_title = ?, hero_description = ?, vision = ?, mission = ?, core_values = ? WHERE id = 1", (hero_title, hero_description, vision, mission, values))
            data = database_cursor.execute("SELECT * FROM about")
            data = data.fetchone()
            database_connection.commit()
            database_connection.close()
            return render_template('modifyAbout.html', social_links = social_links, data=data, message='Data Updated Successfully', navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        else:
            data = database_cursor.execute("SELECT * FROM about")
            data = data.fetchone()
            database_connection.commit()
            database_connection.close()
            return render_template('modifyAbout.html', social_links = social_links, data=data, message=None, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route('/patientLogin/', methods=['GET', 'POST'])
def patientLogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        data = database_cursor.execute("SELECT * FROM patient WHERE email = ? AND password = ?", (email, password))
        data = data.fetchone()
        if data is None:
             return render_template('patientLogin.html', social_links=social_links, message="Invalid Credentials", navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        else:
            session['patient_email'] = data[4]
            return redirect(url_for('patientHome'))
    if 'patient_email' in session:
        return redirect(url_for('patientHome'))
    return render_template('patientLogin.html', social_links=social_links, message=None, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route('/logoutPatient/')
def logoutPatient():
    session.pop('patient_email', None)
    return redirect(url_for('patientLogin'))

@app.route('/patient/')
def patientHome():
    if 'patient_email' in session:
        return render_template('patientHome.html', social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route('/editProfile/',methods=["POST","GET"])
def editProfile():
    if 'patient_email' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        data = database_cursor.execute("SELECT first_name, last_name, mobile, email, gender FROM patient WHERE email = ?", (session['patient_email'],))
        data = data.fetchone()
        if request.method == "POST":
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            phone = request.form["phone"]
            gender = request.form["gender"]
            old_password = request.form["old_password"]
            new_password1 = request.form["new_password1"]
            new_password2 = request.form["new_password2"]
            if old_password != "":
                password = database_cursor.execute("SELECT password FROM patient WHERE email = ?", (session['patient_email'],))
                password = password.fetchone()[0]
                if old_password != password:
                    return render_template("editProfile.html", message="Old password entered incorrectly", data=data, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
                if new_password1 == new_password2 and new_password1!= "":
                    database_cursor.execute("UPDATE patient SET first_name = ?, last_name = ?, mobile = ?, email = ?, gender = ?, password = ? WHERE email = ?", (first_name, last_name, phone, email, gender, new_password1, session['patient_email']))
                    session["patient_email"] = email
                else:
                    return render_template("editProfile.html", message="Passwords do not match/Enter a proper password", data=data, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
            else:
                database_cursor.execute("UPDATE patient SET first_name = ?, last_name = ?, mobile = ?, email = ?, gender = ? WHERE email = ?", (first_name, last_name, phone, email, gender, session['patient_email']))
            session["patient_email"] = email
            database_connection.commit()
            database_connection.close()
            return render_template('editProfile.html', message="Profile Updated Successfully", data=data, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        database_connection.commit()
        database_connection.close()
        return render_template('editProfile.html', message=None, data=data, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route('/manageAdmins/')
def manageAdmins():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        admins = database_cursor.execute("SELECT email, type FROM users")
        admins = admins.fetchall()
        return render_template('manageAdmins.html', social_links=social_links, admins=admins, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route("/addAdmin/<string:email>/<string:password>/<int:userType>/")
def addAdmin(email,password,userType):
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        if userType == 1:
            userType = 'admin'
        elif userType == 2:
            userType = 'reception'
        database_cursor.execute("INSERT INTO users VALUES (?,?,?)",(email,password,userType))
        database_connection.commit()
        database_connection.close()
        return redirect(url_for('manageAdmins'))
    return redirect(url_for('patientLogin'))

@app.route("/deleteAdmin/<string:email>/")
def deleteAdmin(email):
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        database_cursor.execute("DELETE FROM users WHERE email = ?", (email,))
        database_connection.commit()
        database_connection.close()
        return redirect(url_for('manageAdmins'))
    return redirect(url_for('patientLogin'))

@app.route('/managePatients/')
def managePatients():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        patients = database_cursor.execute("SELECT id,first_name,last_name,mobile,email,gender FROM patient")
        patients = patients.fetchall()
        return render_template('managePatients.html', social_links=social_links, patients=patients, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route("/deletePatient/<int:id>/")
def deletePatients(id):
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        database_cursor.execute("DELETE FROM patient WHERE id = ?", (id,))
        database_connection.commit()
        database_connection.close()
        return redirect(url_for('managePatients'))
    return redirect(url_for('patientLogin'))

@app.route("/recentAppointments/", methods=["POST", "GET"])
def recentAppointments():
    if 'user' in session:
        if request.method == "POST":
            from_date = request.form["from_date"]
            to_date = request.form["to_date"]
            database_connection = sqlite3.connect(database_location)
            database_cursor = database_connection.cursor()
            appointments_final = database_cursor.execute("SELECT id, first_name,last_name,type,status FROM appointment WHERE date>= ? AND date <= ?",(from_date,to_date))
            appointments_final = appointments_final.fetchall()
            appointments = [["ID","First Name","Last Name","Appointment Type","Appointment Status"]]
            for i in appointments_final:
                appointments.append(list(i))
            fileName = from_date + to_date + ".csv"
            for file_name in os.listdir(APPOINTMENT_REPORTS):
                os.remove(APPOINTMENT_REPORTS + "/" + file_name)
            np.savetxt(os.path.join(APPOINTMENT_REPORTS,fileName),appointments,delimiter =", ", fmt ='% s')
            appointments.pop(0)
            return render_template("recentAppointments.html",from_date=from_date,to_date=to_date,fileName=fileName, appointments=appointments, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        return render_template("recentAppointments.html", appointments=None, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route("/deleteVirtualTour/", methods=["POST", "GET"])
def deleteVirtualTour():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        if request.method == "POST":
            vt_id = request.form["virtual_tour_id"]
            previous_image = database_cursor.execute("SELECT image FROM virtual_tour WHERE id = ?",(vt_id,))
            previous_image = previous_image.fetchone()[0]
            os.remove(os.path.join(THIS_FOLDER,previous_image.replace("../","")))
            database_cursor.execute("DELETE FROM virtual_tour WHERE id = ?", (vt_id,))
            virtual_tours = database_cursor.execute("SELECT id, title FROM virtual_tour")
            virtual_tours = virtual_tours.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template("deleteVirtualTour.html", virtual_tours=virtual_tours, message="Virtual Tour deleted successfully!", social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        virtual_tours = database_cursor.execute("SELECT id, title FROM virtual_tour")
        virtual_tours = virtual_tours.fetchall()
        database_connection.commit()
        database_connection.close()
        return render_template("deleteVirtualTour.html", virtual_tours=virtual_tours, message=None, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route("/getVirtualTour/<string:id>/")
def getVirtualTour(id):
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    virtual_tours = database_cursor.execute("SELECT title,description,image FROM virtual_tour WHERE id = ?", (int(id),))
    virtual_tours = virtual_tours.fetchone()
    if virtual_tours is not None:
        virtual_tours = list(virtual_tours)
        json_data = json.dumps(virtual_tours)
        database_connection.commit()
        database_connection.close()
        return json_data
    return "No data found"

@app.route("/deleteBlog/", methods=["POST","GET"])
def deleteBlog():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        if request.method == "POST":
            blog_id = request.form["blog_id"]
            previous_image = database_cursor.execute("SELECT image FROM blogs WHERE id = ?",(blog_id,))
            previous_image = previous_image.fetchone()[0]
            os.remove(os.path.join(THIS_FOLDER,previous_image.replace("../../","")))
            database_cursor.execute("DELETE FROM blogs WHERE id = ?", (blog_id,))
            blogs = database_cursor.execute("SELECT id, title FROM blogs")
            blogs = blogs.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template("deleteBlog.html", blogs=blogs, message="Blog deleted successfully!", social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        blogs = database_cursor.execute("SELECT id, title FROM blogs")
        blogs = blogs.fetchall()
        database_connection.commit()
        database_connection.close()
        return render_template("deleteBlog.html", blogs=blogs, message=None, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route("/getBlog/<string:id>/")
def getBlog(id):
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    blogs = database_cursor.execute("SELECT title,description,image FROM blogs WHERE id = ?", (int(id),))
    blogs = blogs.fetchone()
    if blogs is not None:
        blogs = list(blogs)
        json_data = json.dumps(blogs)
        database_connection.commit()
        database_connection.close()
        return json_data
    return "No data found"

@app.route("/deleteNews/",methods=["POST","GET"])
def deleteNews():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        if request.method == "POST":
            news_id = request.form["news_id"]
            previous_image = database_cursor.execute("SELECT image FROM news WHERE id = ?",(news_id,))
            previous_image = previous_image.fetchone()[0]
            os.remove(os.path.join(THIS_FOLDER,previous_image.replace("../","")))
            database_cursor.execute("DELETE FROM news WHERE id = ?", (news_id,))
            news = database_cursor.execute("SELECT id, title FROM news")
            news = news.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template("deleteNews.html",news=news,message="News deleted successfully!", social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        news = database_cursor.execute("SELECT id, title FROM news")
        news = news.fetchall()
        database_connection.commit()
        database_connection.close()
        return render_template("deleteNews.html",news=news, message=None, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route("/getNews/<string:id>/")
def getNews(id):
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    news = database_cursor.execute("SELECT title,description,image FROM news WHERE id = ?", (int(id),))
    news = news.fetchone()
    if news is not None:
        news = list(news)
        json_data = json.dumps(news)
        database_connection.commit()
        database_connection.close()
        return json_data
    return "No data found"

@app.route("/deleteAward/",methods=["POST","GET"])
def deleteAward():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        if request.method == "POST":
            award_id = request.form["award_id"]
            previous_image = database_cursor.execute("SELECT image FROM awards WHERE id = ?",(award_id,))
            previous_image = previous_image.fetchone()[0]
            os.remove(os.path.join(THIS_FOLDER,previous_image.replace("../","")))
            database_cursor.execute("DELETE FROM awards WHERE id = ?",(award_id,))
            awards = database_cursor.execute("SELECT id, title FROM awards")
            awards = awards.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template("deleteAward.html",awards=awards, message = "Award deleted successfully!", social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        awards = database_cursor.execute("SELECT id, title FROM awards")
        awards = awards.fetchall()
        return render_template("deleteAward.html",awards=awards, message = None, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)

@app.route("/getAward/<string:id>/")
def getAward(id):
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    awards = database_cursor.execute("SELECT title,type,description,image FROM awards WHERE id = ?", (int(id),))
    awards = awards.fetchone()
    if awards is not None:
        awards = list(awards)
        json_data = json.dumps(awards)
        database_connection.commit()
        database_connection.close()
        return json_data
    return "No data found"

@app.route("/deleteDoctor/", methods=["POST","GET"])
def deleteDoctor():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        if request.method == "POST":
            doctor_id = request.form["doctor_id"]
            doctor_image = database_cursor.execute("SELECT profile_image FROM doctors WHERE id = ? ",(doctor_id,))
            doctor_image = doctor_image.fetchone()[0]
            os.remove(os.path.join(THIS_FOLDER,doctor_image.replace("../../","")))
            database_cursor.execute("DELETE FROM doctors WHERE id = ?",(doctor_id,))
            database_cursor.execute("DELETE FROM doctor_profile WHERE id = ?",(doctor_id,))
            database_cursor.execute("DELETE FROM doctor_degree WHERE id = ?",(doctor_id,))
            database_cursor.execute("DELETE FROM doctor_experience WHERE id = ?",(doctor_id,))
            doctors = database_cursor.execute("SELECT id, name FROM doctors")
            doctors = doctors.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template("deleteDoctor.html", doctors=doctors, message = "Doctor deleted successfully!", social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        doctors = database_cursor.execute("SELECT id, name FROM doctors")
        doctors = doctors.fetchall()
        database_connection.commit()
        database_connection.close()
        return render_template("deleteDoctor.html", doctors=doctors, message = None, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route("/getDoctor/<string:id>/")
def getDoctor(id):
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    doctors = database_cursor.execute("SELECT name, current_appointment, profile_image FROM doctors WHERE id = ?", (int(id),))
    doctors = doctors.fetchone()
    if doctors is not None:
        doctors = list(doctors)
        json_data = json.dumps(doctors)
        database_connection.commit()
        database_connection.close()
        return json_data
    return "No data found"

@app.route("/deleteDisease/",methods=["POST","GET"])
def deleteDisease():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        if request.method == "POST":
            disease_id = request.form["disease_id"]
            database_cursor.execute("DELETE FROM disease_profile WHERE disease_id = ?", (disease_id,))
            database_cursor.execute("DELETE FROM disease_symptoms WHERE disease_id = ?", (disease_id,))
            database_cursor.execute("DELETE FROM disease_treatment WHERE disease_id = ?", (disease_id,))
            database_cursor.execute("DELETE FROM disease_severity WHERE disease_id = ?", (disease_id,))
            database_cursor.execute("DELETE FROM disease_diagnosis WHERE disease_id = ?", (disease_id,))
            database_cursor.execute("DELETE FROM disease_causes WHERE disease_id = ?", (disease_id,))
            types_images = database_cursor.execute("SELECT image FROM disease_types WHERE disease_id = ?", (disease_id,)).fetchall()
            for i in types_images:
                os.remove(os.path.join(THIS_FOLDER,i[0].replace("../../","")))
            database_cursor.execute("DELETE FROM disease_types WHERE disease_id = ?", (disease_id,))
            disease_images = database_cursor.execute("SELECT illustration, main_image FROM diseases WHERE id = ?", (int(disease_id),))
            for i in disease_images:
                os.remove(os.path.join(THIS_FOLDER,i[0].replace("../../","")))
                os.remove(os.path.join(THIS_FOLDER,i[1].replace("../../","")))
            database_cursor.execute("DELETE FROM diseases WHERE id = ?", (int(disease_id),))
            diseases = database_cursor.execute("SELECT id, title FROM diseases")
            diseases = diseases.fetchall()
            navbar_diseases = database_cursor.execute("SELECT id,title FROM diseases")
            navbar_diseases = navbar_diseases.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template("deleteDisease.html", diseases=diseases, message = "Disease deleted successfully!", social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        diseases = database_cursor.execute("SELECT id, title FROM diseases")
        diseases = diseases.fetchall()
        navbar_diseases = database_cursor.execute("SELECT id,title FROM diseases")
        navbar_diseases = navbar_diseases.fetchall()
        database_connection.commit()
        database_connection.close()
        return render_template("deleteDisease.html", diseases=diseases, message = None, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.route("/getDisease/<string:id>/")
def getDisease(id):
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    disease = database_cursor.execute("SELECT title,specialty_id,description,illustration FROM diseases WHERE id = ?", (int(id),))
    disease = disease.fetchone()
    specialty = database_cursor.execute("SELECT name FROM specialty WHERE id = ?", (disease[1],))
    specialty = specialty.fetchone()[0]
    disease = list(disease)
    disease[1] = specialty
    if disease is not None:
        disease = list(disease)
        json_data = json.dumps(disease)
        database_connection.commit()
        database_connection.close()
        return json_data
    return "No data found"

@app.route("/deleteSpecialty/",methods=["POST","GET"])
def deleteSpecialty():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        if request.method == "POST":
            specialty_id = request.form["specialty_id"]
            previous_illustration = database_cursor.execute("SELECT illustration FROM specialty WHERE id = ?", (int(specialty_id),)).fetchone()[0]
            os.remove(os.path.join(THIS_FOLDER,previous_illustration.replace("../../","")))
            database_cursor.execute("DELETE FROM specialty WHERE id = ?", (int(specialty_id),))
            diseases = database_cursor.execute("SELECT id FROM diseases WHERE specialty_id = ?", (int(specialty_id),)).fetchall()
            for i in diseases:
                database_cursor.execute("DELETE FROM disease_profile WHERE disease_id = ?", (i[0],))
                database_cursor.execute("DELETE FROM disease_symptoms WHERE disease_id = ?", (i[0],))
                database_cursor.execute("DELETE FROM disease_treatment WHERE disease_id = ?", (i[0],))
                database_cursor.execute("DELETE FROM disease_severity WHERE disease_id = ?", (i[0],))
                database_cursor.execute("DELETE FROM disease_diagnosis WHERE disease_id = ?", (i[0],))
                database_cursor.execute("DELETE FROM disease_causes WHERE disease_id = ?", (i[0],))
                types_images = database_cursor.execute("SELECT image FROM disease_types WHERE disease_id = ?", (i[0],)).fetchall()
                for i in types_images:
                    os.remove(os.path.join(THIS_FOLDER,i[0].replace("../../","")))
                database_cursor.execute("DELETE FROM disease_types WHERE disease_id = ?", (i[0],))
            disease_images = database_cursor.execute("SELECT illustration, main_image FROM diseases WHERE specialty_id = ?", (int(specialty_id),))
            for i in disease_images:
                os.remove(os.path.join(THIS_FOLDER,i[0].replace("../../","")))
                os.remove(os.path.join(THIS_FOLDER,i[1].replace("../../","")))
            database_cursor.execute("DELETE FROM diseases WHERE specialty_id = ?", (int(specialty_id),))
            specialty_main = database_cursor.execute("SELECT * FROM specialty")
            specialty_main = specialty_main.fetchall() 
            navbar_specialties = database_cursor.execute("SELECT id,name FROM specialty")
            navbar_specialties = navbar_specialties.fetchall()
            database_connection.commit()
            database_connection.close()
            return render_template("deleteTestimonial.html", specialty_main = specialty_main, message = "Specialty and its diseases Deleted successfully", social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        specialty_main = database_cursor.execute("SELECT * FROM specialty")
        specialty_main = specialty_main.fetchall()
        navbar_specialties = database_cursor.execute("SELECT id,name FROM specialty")
        navbar_specialties = navbar_specialties.fetchall()
        database_connection.commit()
        database_connection.close()
        return render_template("deleteSpecialty.html", specialty_main = specialty_main, message = None, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)    
    
@app.route("/getSpecialty/<string:id>/")
def getSpecialty(id):
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    specialty = database_cursor.execute("SELECT * FROM specialty WHERE id = ?", (int(id),))
    specialty = specialty.fetchone()
    if specialty is not None:
        specialty = list(specialty)
        json_data = json.dumps(specialty)
        database_connection.commit()
        database_connection.close()
        return json_data
    return "No data found"

@app.route("/addDiseaseFAQ/", methods = ["POST","GET"])
def addDiseaseFAQ():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        diseases = database_cursor.execute("SELECT id, title FROM diseases")
        diseases = diseases.fetchall()
        if request.method == "POST":
            disease_id = request.form["disease_id"]
            question = request.form["faq_question"]
            answer = request.form["faq_answer"]
            database_cursor.execute("INSERT INTO disease_faq VALUES (?,?,?)",(disease_id,question,answer))
            database_connection.commit()
            database_connection.close()
            return render_template("addDiseaseFAQ.html",diseases=diseases, message = "FAQ Added Successfully", social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
        database_connection.commit()
        database_connection.close()
        return render_template("addDiseaseFAQ.html",diseases=diseases, message = None, social_links=social_links, navbar_specialties=navbar_specialties, navbar_diseases=navbar_diseases)
    return redirect(url_for('patientLogin'))

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True,port=5000)