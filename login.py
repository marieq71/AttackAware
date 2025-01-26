from flask import request, session, flash, url_for, redirect
from models import db, User
from flask_login import login_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login', render_kw={"class": "button"}) #call the .button class in CSS to pass through spesification

class Login():
    def post(self):
        email=request.form.get('email') #request data from the login form
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #use email to search for user

        if user and user.check_password(password):  # Use the check_password method created in models.py
            
            login_user(user)
            session['userId'] = user.id  # Store the user ID in the session
            
            flash(f'Welcome {user.firstName}. You logged in successfully', 'update')

            return redirect(url_for('profile'))  # Redirect to the home page or dashboard
        else:
            flash('Invalid email or password', 'login') #spesify which form the flash message should show up on ('login')
            return redirect(url_for('home'))
 