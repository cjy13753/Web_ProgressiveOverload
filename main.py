from flask import render_template, Blueprint
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/home')
@login_required
def home():
    return render_template('home.html', user_name=current_user.username, user_id=current_user.id)