from flask import Flask, render_template, redirect, url_for
from wtforms_fields import *
from models import *
from passlib.hash import pbkdf2_sha256

# Configue app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lrpzmxykmzcbsu:2f135748bbc1c3a35f0377e465eb4cdfdf58678df1105d43b62d49c0d0b5f2c9@ec2-23-20-70-32.compute-1.amazonaws.com:5432/dfakdbh4li0103'
db = SQLAlchemy(app)

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
        return redirect(url_for('login'))

    return render_template("index.html", form = reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # Check for login validation
    if login_form.validate_on_submit():
        return "Logged In"
    
    return render_template("login.html", form=login_form)


if __name__ == "__main__":
    app.run(debug=True)