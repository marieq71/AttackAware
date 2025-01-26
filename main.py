# Main Flask application file

from flask import Flask, render_template, request, redirect, url_for, flash, current_app, session
from flask_sqlalchemy import SQLAlchemy
from signup import Signup, SignupForm
from flask_login import current_user, LoginManager, login_required, logout_user
from login import Login, LoginForm
from admin import Admin
from create_admin import create_initial_admin
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
import os
from profile import UpdateProfile, ProfileForm, changePasswordForm, changePassword
from flask import send_from_directory
from utils import commitUserInteraction, topicImage, topicGraph, ALL_TOPICS
from models import db, User, CyberAttack, Scenario, Video, user_interaction

def create_app():
    app = Flask(__name__)  # Initializes the application
    app.secret_key = 'attackaware'  # Needed for flashing messages
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_profile.db'  # The database that will be created
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '123456'
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit to files to avoid overloads
    app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # Set the expiration time to 1 hour (in seconds)
    app.config['WTF_CSRF_SECRET_KEY'] = 'another-random-key'
    app.config['WTF_CSRF_ENABLED'] = True

    # Check if the uploads folder exists, create it if it does not
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Initialize the database
    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()  # Creates the tables if they don't exist
        create_initial_admin()  # Call the function to create the admin

    return app

#create the app by calling the function
app = create_app()

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize the database and login manager
login_manager = LoginManager()

#  # Redirect to the home route for login
login_manager.login_view = 'home'

# Initialize the login manager with the app
login_manager.init_app(app)

# Define ALLOWED_EXTENSIONS globally
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

#customisable domain list for email in signup form
allowed_domains = os.getenv('ALLOWED_DOMAINS', 'gmail.com,yahoo.com,outlook.com').split(',')

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    login_form = LoginForm()
    signup_form = SignupForm()

    # Handle the signup form
    if signup_form.validate_on_submit():
        signup_instance = Signup()  # Create an instance of Signup
        return signup_instance.post()

    # Handle the login form
    if login_form.validate_on_submit():
        login_instance = Login()  # Create an instance of Login
        return login_instance.post()

    # Render both forms in the home template
    return render_template('home.html', login_form=login_form, signup_form=signup_form)

@app.route('/make_admin/<int:user_id>', methods=['POST'])
@login_required
def make_admin(user_id):
    if not current_user.is_admin:
        flash("You do not have permission to perform this action.", 'admin')
        return redirect(url_for('home'))

    result = Admin.promote_to_admin(user_id) # Fixed a typo in the function name
    flash(result)
    return redirect(url_for('home'))

@app.route('/threats')
def threats():
    login_form = LoginForm()
    signup_form = SignupForm()

    is_admin = getattr(current_user, 'is_admin', False) if current_user.is_authenticated else False

    return render_template('threats.html', is_admin=is_admin, login_form=login_form, signup_form=signup_form)  #app needs to check if user is admin to allow certain privileges to page


# Route to render the ransomware page
@app.route('/ransomware')
def ransomware():

    commitUserInteraction('Ransomware') #call the function from utils.py with the topic

    return render_template('ransomware.html')  # Renders ransomware HTML file from templates

@app.route('/social_engineering')
def social_engineering():

    commitUserInteraction('Social Engineering') #call the function from utils.py with the topic

    return render_template('social_engineering.html')  # Renders social engineering HTML file from templates

@app.route('/cyber_hygiene')
def cyber_hygiene():

    commitUserInteraction('Cyber Hygiene')

    return render_template('cyber_hygiene.html')  # Renders cyber hygiene HTML file from templates

@app.route('/IoT')
def IoT():

    commitUserInteraction('IoT')

    return render_template('IoT.html')  # Renders IoT HTML file from templates

@app.route('/phishing_scams')
def phishing_scams():

    commitUserInteraction('Phishing Scams') 

    return render_template('phishing_scams.html')       # Renders phishing scams HTML file from templates


@app.route('/contact_us',  methods=['GET', 'POST'])
def contact_us():
    login_form = LoginForm()   # Passes login form to contact page
    signup_form = SignupForm()  # Passes signup form to contact page
    return render_template('contact_us.html', login_form=login_form, signup_form=signup_form)  # Renders contact us HTML file from templates

@app.route('/admin/attacks', methods=['GET', 'POST'])
def manage_attacks():
    if request.method == 'POST':
        if 'new_attack' in request.form:
            # Add a new attack
            name = request.form['new_attack']
            description = request.form['description']
            prevention = request.form['prevention']
            warning_message = request.form.get('warning_message', '')
            template_name = request.form['template_name']

            # Create and add the new attack to the database
            new_attack = CyberAttack(
                name=name,
                description=description,
                prevention=prevention,
                warning_message=warning_message,
                template_name=template_name
            )
            db.session.add(new_attack)
            db.session.commit()

            flash(f"Attack '{name}' added successfully!", "success")
            session['attack_created'] = True  # Store flag in session

        elif 'scenario-type' in request.form:
            # Add a new scenario
            scenario_type = request.form['scenario-type']
            correct_answer = request.form['correct-answer']
            incorrect_answer = request.form.get('incorrect-answer', '')
            extra_notes = request.form.get('extra-notes', '')

            # Create and add the new scenario to the database
            new_scenario = Scenario(
                type=scenario_type,
                correct_answer=correct_answer,
                incorrect_answer=incorrect_answer,
                extra_notes=extra_notes
            )
            db.session.add(new_scenario)
            db.session.commit()

            flash(f"Scenario '{scenario_type}' added successfully!", "success")
            session['scenario_created'] = True  # Store flag in session

        return redirect(url_for('manage_attacks'))

    # Get all attacks and scenarios from the database
    attacks = CyberAttack.query.all()
    scenarios = Scenario.query.all()

    # Retrieve flags from session and clear them after use
    attack_created = session.pop('attack_created', False)
    scenario_created = session.pop('scenario_created', False)

    # Render the template and pass the flags
    return render_template(
        'manage_attacks.html',
        attacks=attacks,
        scenarios=scenarios,
        attack_created=attack_created,
        scenario_created=scenario_created
    )

@app.route('/attack/<int:attack_id>')
def attack(attack_id):
    attack = CyberAttack.query.get_or_404(attack_id)
    return render_template('ransomware.html', attack=attack)

@app.route('/admin/remove_attack/<int:attack_id>', methods=['POST'])
def remove_attack(attack_id):
    attack = CyberAttack.query.get_or_404(attack_id)  # Fetch the attack by ID
    db.session.delete(attack)  # Delete the attack from the database
    db.session.commit()  # Commit the changes to the database

    flash(f"Attack '{attack.name}' removed successfully!", "success")  # Flash success message
    return redirect(url_for('manage_attacks'))  # Redirect back to the manage attacks page

@app.route('/remove_scenario/<int:scenario_id>', methods=['POST'])
def remove_scenario(scenario_id):
    scenario = Scenario.query.get(scenario_id)
    if scenario:
        db.session.delete(scenario)
        db.session.commit()
        flash(f"Scenario '{scenario.type}' removed successfully.", "success")
    else:
        flash("Scenario not found.", "error")
    return redirect(url_for('manage_attacks'))

@app.route('/manage_videos', methods=['GET', 'POST'])
def manage_videos():
    if request.method == 'POST':
        # Add a new video
        video_link = request.form.get('video_link')
        if video_link:
            new_video = Video(link=video_link)
            db.session.add(new_video)
            db.session.commit()
        return redirect(url_for('manage_videos'))

    # For GET request, render the manage_attacks.html page with existing videos
    videos = Video.query.all()  # Fetch all videos from the database
    return render_template('manage_attacks.html', videos=videos)


@app.route('/remove_video/<int:video_id>', methods=['POST'])
def remove_video(video_id):
    video_to_remove = Video.query.get_or_404(video_id)
    db.session.delete(video_to_remove)
    db.session.commit()
    return redirect(url_for('manage_videos'))

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user is None:
        print("User not found")
    return user


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    user=current_user

    # Retrieve all interactions for the user
    userInteractions = user_interaction.query.filter_by(userId=user.id).all()
    interactedTopics = {interaction.topic for interaction in userInteractions}

    # Fetch the total number of topics from utils.py
    ALL_TOPICS
    totalTopics = len(ALL_TOPICS) 

    # Calculate the progress for the progress bar
    progressBar = (len(interactedTopics) / totalTopics) * 100 if totalTopics > 0 else 0

    form = ProfileForm()
    # Check if the form is submitted and validated
    if form.validate_on_submit():
        updateProfile_instance = UpdateProfile()
        return updateProfile_instance.post()
    
    changePassword_form = changePasswordForm()

    if changePassword_form.validate_on_submit():
        changePassword_instance = changePassword()
        return changePassword_instance.post()
    
    #Query top 3 topics for the current user
    favTopics = user_interaction.query \
    .filter_by(userId=current_user.id) \
    .order_by(user_interaction.clickCount.desc()) \
    .limit(3) \
    .all()
    
     # Instantiate the login and signup forms
    login_form = LoginForm()
    signup_form = SignupForm()
    
    return render_template('profile.html', form=form, 
                           changePassword_form=changePassword_form,
                           login_form=login_form,
                           signup_form=signup_form, 
                           user=user, progressBar = progressBar, 
                           favTopics=favTopics, topicImage=topicImage, 
                           topicGraph=topicGraph, totalTopics=totalTopics) 

@app.route('/uploads/<filename>')
def uploadedFile(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

from utils import get_total_topics

@app.route('/totalTopics')
def totalTopics():
    total_topics = get_total_topics()
    # Do something with total_topics
    return total_topics

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # Handles the login form
    if login_form.validate_on_submit():
        login_instance = Login()  # Create an instance of Login
        result = login_instance.post()

        if result:
            flash("Logged in successfully!", 'info')
            return redirect(url_for('profile'))  # Redirect to profile page
        else:
            flash("Invalid credentials. Please try again.", 'error')

    # Render the form in the home template
    return render_template('base.html', login_form=login_form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()


    # Handles the signup form
    if signup_form.validate_on_submit():
        signup_instance = Signup()  # Creates an instance of Signup
        success = signup_instance.post()

        # Redirects to login after successful signup
        if success:
            flash("Account created successfully! Please log in.", 'info')
            return redirect(url_for('home'))  # Redirects to home page after signup
        else:
            flash("There was an error with the signup. Please try again.", 'error')

    # Renders the form in the home template
    return render_template('home.html', signup_form=signup_form)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    app.logger.info("CSRF Token: %s", request.form.get('_csrf_token'))  # Log CSRF token for debugging

    try:
        logout_user()
        flash("You have successfully logged out.", 'info')
        return redirect(url_for('home'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        return redirect(url_for('home'))
    
#Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# Context processor to handle login and signup instances across all pages
@app.context_processor
def inject_forms():
    return {
        'login_form': LoginForm(),
        'signup_form': SignupForm()
    }

if __name__ == "__main__":
    app.run(debug=True)  # Enables debug mode to rerun the application when changes are made

