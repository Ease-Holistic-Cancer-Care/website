from crypt import methods
from email import message
from flask import Flask, render_template, redirect, url_for, session, request
import sqlite3
import os

#Initialize Flask App
app = Flask(__name__)
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
database_location = os.path.join(THIS_FOLDER, 'database.db')
app.secret_key = 'super secret key'

#social media links
database_connection = sqlite3.connect(database_location)
database_cursor = database_connection.cursor()
social_links = database_cursor.execute("SELECT * FROM social_links")
social_links = social_links.fetchall()
database_connection.commit()
database_connection.close()

@app.route('/')
def index():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    slides = database_cursor.execute("SELECT * FROM home_carousel")
    slides = slides.fetchall()
    about = database_cursor.execute("SELECT * FROM home_page")
    about = about.fetchone()
    specialties = database_cursor.execute("SELECT * FROM specialty")
    specialties = specialties.fetchmany(3)
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
    return render_template('index.html',slides=slides, about=about, specialties=specialties, statistics=statistics, social_links=social_links, doctor_data=doctor_data, testimonials=testimonials, faqs=faqs)

@app.route('/admin/')
def adminHome():
    if 'user' in session:
        return render_template('adminHome.html', social_links=social_links)
    return redirect(url_for('login'))

@app.route('/modifyPages/')
def modifyPages():
    if 'user' in session:
        return render_template('modifyPages.html', social_links=social_links)
    return redirect(url_for('login'))

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
    return render_template('about.html', data=data,social_links=social_links)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        data = database_cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        data = data.fetchone()
        if data is None:
             return render_template('login.html', social_links=social_links, message="Invalid Credentials")
        else:
            session['user'] = data[0]
            session['user_type'] = data[2]
            return redirect(url_for('adminHome'))
    if 'user' in session:
        return redirect(url_for('adminHome'))
    return render_template('login.html', social_links=social_links, message=None)

@app.route('/logout/')
def logout():
    session.pop('user', None)
    session.pop('user_type', None)
    return redirect(url_for('login'))

@app.route('/doctors/')
def doctors():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    data = database_cursor.execute("SELECT * FROM doctors")
    data = data.fetchall()
    database_connection.commit()
    return render_template('doctors.html',social_links=social_links, data=data)

@app.route('/doctorInfo/')
def doctorsInfo():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    doctor_data = database_cursor.execute("SELECT * FROM doctors")
    doctor_data = doctor_data.fetchone()
    doctor_profile = database_cursor.execute("SELECT * FROM doctor_profile")
    doctor_profile = doctor_profile.fetchone()
    doctor_degree = database_cursor.execute("SELECT * FROM doctor_degree")
    doctor_degree = doctor_degree.fetchall()
    doctor_experience = database_cursor.execute("SELECT * FROM doctor_experience")
    doctor_experience = doctor_experience.fetchall()
    database_connection.commit()
    database_connection.close()
    return render_template('doctorInfo.html',social_links=social_links, doctor_data=doctor_data, doctor_profile=doctor_profile, doctor_degree=doctor_degree, doctor_experience=doctor_experience)

@app.route('/specialty/')
def specialty():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    specialties = database_cursor.execute("SELECT * FROM specialty")
    specialties = specialties.fetchall()
    database_connection.commit()
    database_connection.close()
    return render_template('specialty.html',social_links=social_links, specialties=specialties)

@app.route('/diseases/')
def diseases():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    diseases = database_cursor.execute("SELECT * FROM diseases")
    diseases = diseases.fetchall()
    database_connection.commit()
    database_connection.close()
    return render_template('diseases.html',social_links=social_links, diseases=diseases)

@app.route('/disease/')
def disease():
    return render_template('disease.html',social_links=social_links)

@app.route('/awards/')
def awards():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    data = database_cursor.execute("SELECT * FROM awards")
    data = data.fetchall()
    return render_template('awards.html', data=data,social_links=social_links)

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
        database_connection.commit()
        database_connection.close()
        return render_template('contact.html',social_links=social_links, message="Your message has been sent successfully. We will contact you soon.")
    return render_template('contact.html',social_links=social_links, message=None)

@app.route('/appointment/', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
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
        return render_template('appointment.html',social_links=social_links, message="Your appointment has been sent successfully. We will contact you soon.")
    return render_template('appointment.html',social_links=social_links, message=None)

@app.route('/patient/')
def patient(): 
    return render_template('patient.html')

@app.route('/virtualTour/')
def virtualTour():
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    data = database_cursor.execute("SELECT * FROM virtual_tour")
    data = data.fetchall()
    return render_template('virtualTour.html', data=data,social_links=social_links)

@app.route('/blogs/')
def blogs(): 
    database_connection = sqlite3.connect(database_location)
    database_cursor = database_connection.cursor()
    data = database_cursor.execute("SELECT * FROM blogs")
    data = data.fetchall()
    return render_template('blogs.html', data=data,social_links=social_links)

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
    print(len(data))
    return render_template('news.html', data=data, latest_news=latest_news,social_links=social_links)

@app.route('/modifyHome/', methods=['GET', 'POST'])
def modifyHome():
    if 'user' in session:
        database_connection = sqlite3.connect(database_location)
        database_cursor = database_connection.cursor()
        carousel_data = database_cursor.execute("SELECT * FROM home_carousel")
        carousel_data = carousel_data.fetchall()
        about = database_cursor.execute("SELECT * FROM home_page")
        about = about.fetchone()
        if request.method == 'POST':
            #carousel
            carousel_items = database_cursor.execute("SELECT COUNT(*) FROM home_carousel;")
            carousel_items = carousel_items.fetchone()[0]
            carousel = []
            for i in range(carousel_items):
                temp = []
                carousel_heading = request.form['carousel_heading_'+str(i+1)]
                carousel_description = request.form['carousel_description_'+str(i+1)]
                temp.append(carousel_heading)
                temp.append(carousel_description)
                carousel.append(temp)
            for i in range(carousel_items):
                database_cursor.execute("UPDATE home_carousel SET heading=?, description=? WHERE id=?;", (carousel[i][0], carousel[i][1], i+1))
            #about
            about_heading = request.form['about_heading']
            about_description = request.form['about_description']
            about_image = database_cursor.execute("SELECT about_image FROM home_page;")
            about_image = about_image.fetchone()[0]
            database_cursor.execute("UPDATE home_page SET about_heading=?, about_description=? WHERE about_image=?;", (about_heading, about_description, about_image))
            database_connection.commit()
            database_connection.close()
            return render_template('modifyHome.html', social_links = social_links, about=about, carousel_data = carousel_data, message = "Details updated successfully.")
        else:
            database_connection.commit()
            database_connection.close()
            return render_template('modifyHome.html', social_links = social_links, about=about, carousel_data = carousel_data, message = None)
    return redirect(url_for('login'))

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
            return render_template('modifyAbout.html', social_links = social_links, data=data, message='Data Updated Successfully')
        else:
            data = database_cursor.execute("SELECT * FROM about")
            data = data.fetchone()
            database_connection.commit()
            database_connection.close()
            return render_template('modifyAbout.html', social_links = social_links, data=data, message=None)
    return redirect(url_for('login'))

@app.route('/modifyDoctors/')
def modifyDoctors():
    if 'user' in session:
        return render_template('modifyDoctors.html', social_links = social_links)
    return redirect(url_for('login'))

@app.route('/modifySpecialties/')
def modifySpecialties():
    if 'user' in session:
        return render_template('modifySpecialties.html', social_links = social_links)
    return redirect(url_for('login'))

@app.route('/modifyNews/')
def modifyNews():
    if 'user' in session:
        return render_template('modifyNews.html', social_links = social_links)
    return redirect(url_for('login'))

@app.route('/modifyAwards/')
def modifyAwards():
    if 'user' in session:
        return render_template('modifyAwards.html', social_links = social_links)
    return redirect(url_for('login'))

@app.route('/modifyBlogs/')
def modifyBlogs():
    if 'user' in session:
        return render_template('modifyBlogs.html', social_links = social_links)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True,port=5000)