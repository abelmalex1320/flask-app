from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key

# Configure MySQL connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql",
        database="aircraft_db"
    )

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    db.close()
    if user:
        return User(user['id'], user['username'])
    return None

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        db.close()

        if user:
            user_obj = User(user['id'], user['username'])
            login_user(user_obj)
            return redirect(url_for('aircraft_list'))
        else:
            return "Invalid username or password"

    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Aircraft List (Protected Page)
@app.route('/aircraft-list')
@login_required
def aircraft_list():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT AC_ID, AC_NAME, FAULT_STATUS FROM aircraft")
    aircrafts = cursor.fetchall()
    db.close()
    return render_template("aircraft_list.html", aircrafts=aircrafts)

# Aircraft Detail Page (Protected)
@app.route('/aircraft/<int:aircraft_id>')
@login_required
def aircraft_detail(aircraft_id):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM aircraft WHERE AC_ID = %s", (aircraft_id,))
    aircraft = cursor.fetchone()
    db.close()
    return render_template("aircraft_detail.html", aircraft=aircraft)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
