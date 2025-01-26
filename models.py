from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
from flask_login import current_user

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

# Define the User class that maps to the 'User' table in the database
class User(UserMixin, db.Model):

    __tablename__ = 'user' #SQLAlchemy defualt table names to lowercase/
                           #Explicitly set the table name

    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    firstName = db.Column(db.String(20))  # First name, with a max length of 20 characters
    lastName = db.Column(db.String(30))  # Last name, with a max length of 30 characters
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email, must be unique and required
    password = db.Column(db.String, nullable=False)  # Password, required for every user
    birthday = db.Column(db.DateTime, nullable=True) 
    profilePic = db.Column(db.String(100), nullable=True)  # Store the file path as a string
    is_admin = db.Column(db.Boolean, default=False)  # Mark if user is admin

    # Define how to represent a User object when printed or logged
    def __repr__(self):
        # Return a string that includes the email of the user in a readable format
        return f'<User {self.email}>'
        # For example, if the user's email is 'user@example.com', it will return '<User user@example.com>'

#allows system to compare user password with password stored in hash
    def set_password(self, password): 
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class CyberAttack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    prevention = db.Column(db.Text, nullable=False)
    warning_message = db.Column(db.String(255), default='')
    template_name = db.Column(db.String(100), nullable=False)

class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)  # Scenario type
    correct_answer = db.Column(db.String(255), nullable=False)  # Correct answer
    incorrect_answer = db.Column(db.String(255), nullable=True)  # Optional incorrect answer
    extra_notes = db.Column(db.Text, nullable=True)  # Additional notes
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(255), nullable=False)  # Adjust max length as needed

#Create a class that wil save the interaction that the user has with the app
class user_interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each interaction
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ForeignKey for user
    topic = db.Column(db.String(100), nullable=False)  # Topic of the interaction
    clickCount = db.Column(db.Integer, default=0)  # Count of user clicks, with a default value

    # Relationship for ease of querying
    user = db.relationship('User', backref='interactions',  lazy=True)  # Establish relationship with User


