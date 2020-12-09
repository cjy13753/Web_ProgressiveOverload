from flask import redirect, url_for, request, Blueprint, flash, render_template
from flask_login import login_user, logout_user, login_required

from werkzeug.security import generate_password_hash, check_password_hash
from models.user import UserModel

auth = Blueprint('auth', __name__)

@auth.route('/')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = UserModel.find_by_username(username=username)
    
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=remember)
    return redirect(url_for('main.home'))


@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = UserModel.find_by_username(username=username)

    if user:
        flash('Username already exists')
        return redirect(url_for('main.signup'))

    new_user = UserModel(username=username, password=generate_password_hash(password, method='sha256'))

    new_user.save_to_db()

    return redirect(url_for('auth.login'))