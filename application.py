from flask import Flask, render_template, redirect, url_for, flash
from wtforms_fields import *
from models import *
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit

# Configue app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lrpzmxykmzcbsu:2f135748bbc1c3a35f0377e465eb4cdfdf58678df1105d43b62d49c0d0b5f2c9@ec2-23-20-70-32.compute-1.amazonaws.com:5432/dfakdbh4li0103'
db = SQLAlchemy(app)

# Initialise Flask-Socketio
socketio = SocketIO(app)

# Configure login session
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Hasing the password
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add user to database
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        flash('Registered Successfully. Please Login', 'success')
        return redirect(url_for('login'))

    return render_template("index.html", form = reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # Allow login after validation
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))
    
    return render_template("login.html", form=login_form)


@app.route("/chat", methods=['GET', 'POST'])
def chat():
    # if not current_user.is_authenticated:
    #     flash("Please login before joining the chatroom.", "danger")
    #     return redirect(url_for('login'))


    
    return render_template('chat.html')


@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))


@socketio.on('message')
def message(data):
    print(f"\n{data}\n")
    send(data)


if __name__ == "__main__":
    socketio.run(app, debug=True)