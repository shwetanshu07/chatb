from flask import Flask, render_template
from wtforms_fields import *
from models import *

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

        # Check if username exists
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            # there already exists a same username
            return "Someone else has taken this username"
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted into DB"
    return render_template("index.html", form = reg_form)


if __name__ == "__main__":
    app.run(debug=True)