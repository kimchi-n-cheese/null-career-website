from flask import Flask, render_template, Blueprint, request, redirect,flash, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User

app = Flask(__name__)

TOUR_PACKAGE = [
  {
    'id': 1,
    'title': 'Vietnam',
    'duration': '7 days',
    'price': 'Starting at $600'
  },
  {
    'id': 2,
    'title': 'Laos',
    'duration': '4 days',
    'price': 'Starting at $350'
  },
  {
    'id': 3,
    'title': 'Cambodia',
    'duration': '4 days',
    'price': 'Starting at $360'
  },
  {
    'id': 4,
    'title': 'Thailand',
    'duration': '5 days',
    'price': 'Starting at $600'
  }
]

auth = Blueprint('auth', __name__)

@app.route("/")
def home():
  return render_template('home.html', deals=TOUR_PACKAGE)

@app.route("/base")
def base():
  return render_template("base.html")

@app.route("/api/tours")
def list_tours():
  return jsonify(TOUR_PACKAGE)

@app.route("/aboutus")
def aboutus():
  return render_template("aboutus.html", user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
      email = request.form.get('email')
      password = request.form.get('password')
      user = User.query.filter_by(email=email).first()
      if user:
          if check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
          else:
            flash('Incorrect password. Please try again.', category='error')
      else:
        flash('There is no account registered under this email.', category='error')
  return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@app.route("/signup", methods=['GET', 'POST'])
def sign_up():
  if request.method == 'POST':
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    password1 = request.form.get('password1')
    confirm_password = request.form.get('password2')
    
    user = User.query.filter_by(email=email).first()
    if user:
      flash('This email is already registered.', category='error')
    if len(email) < 4:
        flash('Email must contain a minimum of 4 characters.', category='error')
    elif len(first_name) < 2:
        flash('First name must contain a minimum of 2 characters.', category='error')
    elif password1 != confirm_password:
        flash('Password does not match', category='error')
    elif all(c.isalpha() for c in password1):
        flash('Password must contain at least one digit.', category='error')
    else:
        new_user = User(email=email,first_name = first_name, password=generate_password_hash(password1, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('Your account has been created.', category='success')
        return redirect(url_for('app.home'))
            #data is valid. Add user to database
  return render_template("sign_up.html", user=current_user)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)