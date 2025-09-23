# wine.py is a Python script that creates a web application using Flask to 
# predict the type of wine based on the user's input of wine characteristics. 
# The script loads a pre-trained machine learning model from a pickle file 
# and uses it to make predictions. The web application allows users to input 
# values for various wine characteristics, such as alcohol content and color 
# intensity, and then displays the predicted wine type based on the input values. 
# The script also includes a signal handler to shut down the server gracefully 
# on shutdown. The web application can be accessed by running the script and 
# navigating to the appropriate URL in a web browser.

from flask import Flask, render_template, request, redirect, url_for, session
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
import sqlite3
import pickle
import signal
import re
from user_activity_logger import activity_logger

# Create a signal handler to shut down the server gracefully on shutdown
def shutdown(signal_number, frame):
    print("Shutting down server")
    exit(0)

signal.signal(signal.SIGINT, shutdown)

# Load the model from the pickle file
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
app.secret_key = 'your_secret_key'

# # Configure MySQL service
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'MySQL@#1234'
# app.config['MYSQL_DB'] = 'wineruserdb'

# mysql = MySQL(app)

# Turn debugging mode off for production
app.debug = True 

# create a routine to notify test scipts that the server is up and running
@app.route("/health")
def health_check():
    return "Server is healthy!", 200  # Return 200 OK when ready

# this decorator tells Flask what URL should trigger our function
@app.route("/")
def wine_predict():
    if 'username' in session:
        return render_template('wine.html')
    else:
        return render_template('login.html')

# login provides a simple login form for users to enter their username and password
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = sqlite3.connect('wineusers.db').cursor()
        if cursor:
            cursor.execute('SELECT * FROM accounts WHERE username = ? AND password = ?', (username, password))
            account = cursor.fetchone()
            cursor.close()
            if account:
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['email'] = account[3]
                
                # Log successful login
                activity_logger.log_login_attempt(username, success=True)
                
                msg = 'Logged in successfully!'
                return render_template('wine.html', prediction_text = msg)
            else:
                # Log failed login attempt
                activity_logger.log_login_attempt(username, success=False, details={'reason': 'invalid_credentials'})
                msg = 'Incorrect username/password!'
        else:
            # Log database connection error
            activity_logger.log_login_attempt(username, success=False, details={'reason': 'database_error'})
            msg = 'Database connection error!'

    return render_template('login.html', login_text='Incorrect username/password!')

# logout removes the user's session data and redirects them to the login page
@app.route("/logout")
def logout():
    # Log logout before clearing session
    username = session.get('username')
    activity_logger.log_logout(username=username)
    
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))

# profile displays the user's profile information if they are logged in
@app.route("/profile")
def profile():
    if 'username' in session:
        # Log profile access
        activity_logger.log_profile_access()
        return render_template('profile.html', username_text='Username: {}'.format(session['username']), email_text='Email: {}'.format(session['email']))
    else:
        return render_template('login.html')

# register provides a simple registration form for users to create a new account
@app.route("/register", methods=['POST', 'GET'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = sqlite3.connect('wineusers.db').cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = ?', (username, ))
        account = cursor.fetchone()
        # cursor = mysql.connection.cursor()
        # cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        # account = cursor.fetchone()
        if account:
            activity_logger.log_registration(username, success=False, details={'reason': 'username_exists'})
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            activity_logger.log_registration(username, success=False, details={'reason': 'invalid_email'})
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            activity_logger.log_registration(username, success=False, details={'reason': 'invalid_username'})
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            activity_logger.log_registration(username, success=False, details={'reason': 'incomplete_form'})
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, ?, ?, ?)', (username, password, email, ))
            cursor.connection.commit()
            cursor.close()
            # cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            # mysql.connection.commit()
            activity_logger.log_registration(username, success=True)
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        activity_logger.log_registration('', success=False, details={'reason': 'incomplete_form'})
        msg = 'Please fill out the form!'
    return render_template('register.html', register_text=msg)

# about provides information about the web application       
@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')

# contact provides a simple contact form for users to send a message to the webmaster
@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        # Log contact form submission
        activity_logger.log_contact_form()
        return render_template('contact.html', contact_text='Your meessage has been sent!')
    else:
        return render_template('contact.html', contact_text='')

# predict uses the machine learning model to predict the wine type based on the user's input
@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('wine.html')
    else:
        alcohol = request.form['alcohol']
        malic_acid = request.form['malic_acid']
        ash = request.form['ash']
        alcalinity_of_ash = request.form['alcalinity_of_ash']
        magnesium = request.form['magnesium']
        total_phenols = request.form['total_phenols']
        flavanoids = request.form['flavanoids']
        nonflavanoid_phenols = request.form['nonflavanoid_phenols']
        proanthocyanins = request.form['proanthocyanins']
        color_intensity = request.form['color_intensity']
        hue = request.form['hue']
        od280_od315_of_diluted_wines = request.form['od280_od315_of_diluted_wines']
        proline = request.form['proline']

        prediction = model.predict([[alcohol, malic_acid, ash, alcalinity_of_ash, magnesium, total_phenols, flavanoids, nonflavanoid_phenols, proanthocyanins, color_intensity, hue, od280_od315_of_diluted_wines, proline]])
        prediction = prediction[0]

        # Log wine classification with input data and prediction
        wine_data = {
            'alcohol': alcohol,
            'malic_acid': malic_acid,
            'ash': ash,
            'alcalinity_of_ash': alcalinity_of_ash,
            'magnesium': magnesium,
            'total_phenols': total_phenols,
            'flavanoids': flavanoids,
            'nonflavanoid_phenols': nonflavanoid_phenols,
            'proanthocyanins': proanthocyanins,
            'color_intensity': color_intensity,
            'hue': hue,
            'od280_od315_of_diluted_wines': od280_od315_of_diluted_wines,
            'proline': proline
        }
        activity_logger.log_wine_classification(wine_data, int(prediction))

        return render_template('wine.html', prediction_text='The wine type is variety #{}'.format(prediction))

# change_password allows users to change their password if they are logged in
@app.route("/change_password", methods=['POST'])
def change_password():
    if 'username' in session:
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            activity_logger.log_password_change(success=False, details={'reason': 'password_mismatch'})
            return render_template('profile.html', username_text='Username: {}'.format(session['username']), email_text='Email: {}'.format(session['email']), profile_text='New passwords do not match!')
        
        cursor = sqlite3.connect('wineusers.db').cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = ? AND password = ?', (session['username'], current_password))
        account = cursor.fetchone()
        # cursor = mysql.connection.cursor()
        # cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (session['username'], current_password))
        # account = cursor.fetchone()
        
        if account:
            cursor.execute('UPDATE accounts SET password = ? WHERE username = ?', (new_password, session['username']))
            cursor.connection.commit()
            cursor.close()
            # cursor.execute('UPDATE accounts SET password = %s WHERE username = %s', (new_password, session['username']))
            # mysql.connection.commit()
            activity_logger.log_password_change(success=True)
            return render_template('profile.html', username_text='Username: {}'.format(session['username']), email_text='Email: {}'.format(session['email']), profile_text='Password changed successfully!')
        else:
            cursor.close()
            activity_logger.log_password_change(success=False, details={'reason': 'incorrect_current_password'})
            return render_template('profile.html', username_text='Username: {}'.format(session['username']), email_text='Email: {}'.format(session['email']), current_password=current_password, profile_text='Current password is incorrect!')
    else:
        return redirect(url_for('login'))

# main runs the Flask web application
if __name__ == "__main__":
#    app.debug = True
    app.run()

