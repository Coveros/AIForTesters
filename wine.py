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
from datetime import datetime

# Create a signal handler to shut down the server gracefully on shutdown
def shutdown(signal_number, frame):
    print("Shutting down server")
    exit(0)

signal.signal(signal.SIGINT, shutdown)

# Load the model from the pickle file
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
app.secret_key = 'your_secret_key'

DB_FILE = 'wineusers.db'

# # Configure MySQL service
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'MySQL@#1234'
# app.config['MYSQL_DB'] = 'wineruserdb'

# mysql = MySQL(app)

# Turn debugging mode off for production
app.debug = True 

# initialize the database and create the activity_log table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        action TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

# log_activity records a user action into the activity_log table
def log_activity(user_id, username, action):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO activity_log (user_id, username, action, timestamp) VALUES (?, ?, ?, ?)',
                   (user_id, username, action, timestamp))
    conn.commit()
    conn.close()

# get_user_activity_logs retrieves all activity log entries for a given user
def get_user_activity_logs(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT action, timestamp FROM activity_log WHERE user_id = ? ORDER BY id DESC', (user_id,))
    logs = cursor.fetchall()
    conn.close()
    return logs

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
        cursor = sqlite3.connect(DB_FILE).cursor()
        if cursor:
            cursor.execute('SELECT * FROM accounts WHERE username = ? AND password = ?', (username, password))
            account = cursor.fetchone()
            cursor.close()
            if account:
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['email'] = account[3]
                log_activity(account[0], account[1], 'login')
                msg = 'Logged in successfully!'
                return render_template('wine.html', prediction_text = msg)
            else:
                msg = 'Incorrect username/password!'
        else:
            msg = 'Database connection error!'

    return render_template('login.html', login_text='Incorrect username/password!')

# logout removes the user's session data and redirects them to the login page
@app.route("/logout")
def logout():
    if 'id' in session and 'username' in session:
        log_activity(session['id'], session['username'], 'logout')
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))

# profile displays the user's profile information if they are logged in
@app.route("/profile")
def profile():
    if 'username' in session:
        return render_template('profile.html', username_text='Username: {}'.format(session['username']), email_text='Email: {}'.format(session['email']), activity_logs=get_user_activity_logs(session['id']))
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
        cursor = sqlite3.connect(DB_FILE).cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = ?', (username, ))
        account = cursor.fetchone()
        # cursor = mysql.connection.cursor()
        # cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        # account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, ?, ?, ?)', (username, password, email, ))
            cursor.connection.commit()
            # retrieve the new account id for logging
            cursor.execute('SELECT id FROM accounts WHERE username = ?', (username,))
            new_account = cursor.fetchone()
            cursor.close()
            # cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            # mysql.connection.commit()
            if new_account:
                log_activity(new_account[0], username, 'register')
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
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

        return render_template('wine.html', prediction_text='The wine type is variety #{}'.format(prediction))

# change_password allows users to change their password if they are logged in
@app.route("/change_password", methods=['POST'])
def change_password():
    if 'username' in session:
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            return render_template('profile.html', username_text='Username: {}'.format(session['username']), email_text='Email: {}'.format(session['email']), profile_text='New passwords do not match!', activity_logs=get_user_activity_logs(session['id']))
        
        cursor = sqlite3.connect(DB_FILE).cursor()
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
            log_activity(session['id'], session['username'], 'change_password')
            return render_template('profile.html', username_text='Username: {}'.format(session['username']), email_text='Email: {}'.format(session['email']), profile_text='Password changed successfully!', activity_logs=get_user_activity_logs(session['id']))
        else:
            cursor.close()
            return render_template('profile.html', username_text='Username: {}'.format(session['username']), email_text='Email: {}'.format(session['email']), current_password=current_password, profile_text='Current password is incorrect!', activity_logs=get_user_activity_logs(session['id']))
    else:
        return redirect(url_for('login'))

# main runs the Flask web application
if __name__ == "__main__":
#    app.debug = True
    app.run()

