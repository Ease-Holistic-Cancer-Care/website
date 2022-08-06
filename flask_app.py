from flask import Flask, render_template, redirect, url_for, session, request

#Initialize Flask App
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

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

@app.route('/specialty')
def specialty():
    return render_template('specialty.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

@app.route('/patient')
def patient(): 
    return render_template('patient.html')

if __name__ == '__main__':
    app.run(debug=True)