from chatb import app, db, login_manager, socketio, ROOMS
from flask import render_template, url_for, flash, redirect
from chatb.forms import RegistrationForm, LoginForm
from chatb.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import send, emit, join_room, leave_room
from time import localtime, strftime
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_obj = User.query.filter_by(username = login_form.username.data).first()
        login_user(user_obj)
        return redirect(url_for('chat'))
    
    return render_template('index.html', lform = login_form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    
    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        uname = reg_form.username.data
        pswd = reg_form.password.data

        user = User(username=uname, password = pswd)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('chat'))
    
    return render_template('register.html', rform = reg_form)


@app.route("/chat")
@login_required
def chat():
    return render_template("chat.html", rooms=ROOMS)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

# Event handlers for SocketIO
@socketio.on('message')
def handle_message(data):
    print(data)
    t = strftime("%H:%M %p", localtime())
    msg = data['msg']
    uname = data['username']
    send({"username":uname, "msg":msg, "time":t}, room=data['room'])

@socketio.on('join')
def join(data):
    room = data['room']
    join_room(room)
    #sending notification that user X has joined this room
    msg = data['username'] + " has joined the " + data['room'] + " room."
    send({'msg':msg}, room = room)

@socketio.on('leave')
def leave(data):
    lroom = data['room']
    leave_room(lroom)
    #sending notification that user X has left this room
    msg = data['username'] + " has left the " + data['room'] + " room."
    send({'msg':msg}, room = lroom)
