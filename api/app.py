# Import necessary modules and libraries
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField, TextAreaField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Email, DataRequired
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' # Add a secret key for CSRF protection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_board.db'
db = SQLAlchemy(app)

# Initialize Flask-Login for managing user sessions
login_manager = LoginManager(app)
# Add the user_loader decorator

# Define a user loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)
# Initialize CSRF protection
csrf = CSRFProtect(app) # Initialize CSRF protection

# Define Flask forms for various purposes
class EmployerForm(FlaskForm):
    # ... Field definitions and validators ...
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    website = StringField('Website')
    location = StringField('Location', validators=[DataRequired()])
    job_title = StringField('Job Title', validators=[DataRequired()])
    experience = StringField('Experience', validators=[DataRequired()])
    salary = StringField('Salary', validators=[DataRequired()])
    skills = StringField('Skills', validators=[DataRequired()])
    job_vacancy_details = TextAreaField('Job Vacancy Details', validators=[DataRequired()])
    submit = SubmitField('Submit')

class JobSeekerForm(FlaskForm):
    # ... Field definitions and validators ...
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    tel = StringField('Phone', validators=[DataRequired(), Length(min=12, max=12)])
    position = StringField('Position you are applying for', validators=[DataRequired()])
    resume = FileField('Resume Upload')
    website = StringField('Portfolio Website')
    salary = StringField('Salary Requirements')
    joining = StringField('When can you start?')
    relocation = SelectField('Are you willing to relocate?', choices=[('Yes', 'Yes'), ('No', 'No'), ('Not Sure', 'Not Sure')])
    last_employer = StringField('Last company you worked for?')
    address = TextAreaField('Comments')
    submit = SubmitField('Submit')

class AdminLoginForm(FlaskForm):
    # ... Field definitions and validators ...
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ContactForm(FlaskForm):
    # ... Field definitions and validators ...
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Your name"})
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "Your email address"})
    county = SelectField('County', choices=[('Nairobi', 'Nairobi'), ('Mombasa', 'Mombasa'), ('Kisumu', 'Kisumu')])
    subject = TextAreaField('Subject', validators=[DataRequired()], render_kw={"placeholder": "Write something..."})
    submit = SubmitField('Submit')

# Define SQLAlchemy models for database tables

class Employer(db.Model):
    # ... Table fields and relationships ...
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(100), nullable=False)
    job_vacancy_details = db.Column(db.String(255), nullable=False)
    job_listings = db.relationship('JobListing', backref='employer', lazy=True)

class JobSeeker(db.Model):
    # ... Table fields and relationships ...
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    tel = db.Column(db.String(12), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    resume = db.Column(db.String(100))  # You can adjust this based on your needs
    website = db.Column(db.String(100))
    salary = db.Column(db.String(100))
    joining = db.Column(db.String(100))
    relocation = db.Column(db.String(100))
    last_employer = db.Column(db.String(100))
    address = db.Column(db.String(255))

class JobListing(db.Model):
    # ... Table fields and relationships ...
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(100), nullable=False)
    job_vacancy_details = db.Column(db.String(255), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)

class Contact(db.Model):
    # ... Table fields and relationships ...
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    county = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(255), nullable=False)

class Admin(db.Model, UserMixin):
    # ... Table fields and methods ...
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class User(db.Model):
    # ... Table fields and methods ...
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Define route for the home page
@app.route('/')
def index():
    job_listings = JobListing.query.all()  # Query job listings from the database
    return render_template('index.html', job_listings=job_listings)

# Define route for the contact page with form handling
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()  # Create an instance of the form

    if form.validate_on_submit():
        # Use the form data from the validated form
        name = form.name.data
        email = form.email.data
        county = form.county.data
        subject = form.subject.data

        # Create a new Contact object and add it to the database
        new_contact = Contact(
            name=name,
            email=email,
            county=county,
            subject=subject
        )

        db.session.add(new_contact)
        db.session.commit()

        # Redirect to a success page or the contact page dashboard
        return redirect(url_for('contact'))
        
    return render_template('contact.html', form=form)  # Pass the form to the template

# Define route for displaying job listings
@app.route('/jobs')
def jobs():
    # Query job listings from the database
    job_listings = JobListing.query.all()  
    return render_template('jobs.html', job_listings=job_listings)

# Define route for the employer dashboard with form handling
@app.route('/employer', methods=['GET', 'POST'])
def employer_dashboard():
    form = EmployerForm()  # Create an instance of the form

    # Fetch job listings from the database
    # job_listings = JobListing.query.all()
    # print("Job Listings from Database:", job_listings)  
    # Add this line for debugging

    print("Before Querying Database")
    job_listings = JobListing.query.all()
    print("After Querying Database")
    print("Job Listings from Database:", job_listings)

    for listing in job_listings:
        print("Title:", listing.title)
        print("Company:", listing.company)
        print("Experience:", listing.experience)
        print("Salary:", listing.salary)
        print("Location:", listing.location)
        print("Job Vacancy Details:", listing.job_vacancy_details)

    if form.validate_on_submit():  # Check if the form has been submitted and is valid
        # Get form data from the form
        name = form.name.data
        email = form.email.data
        company = form.company.data
        website = form.website.data
        location = form.location.data
        job_title = form.job_title.data
        experience = form.experience.data
        salary = form.salary.data
        skills = form.skills.data
        job_vacancy_details = form.job_vacancy_details.data

        # Create a new Employer object and add it to the database
        new_employer = Employer(
            name=name,
            email=email,
            company=company,
            website=website,
            location=location,
            job_title=job_title,
            experience=experience,
            salary=salary,
            skills=skills,
            job_vacancy_details=job_vacancy_details
        )
        db.session.add(new_employer)
        db.session.commit()

        # Now, create a job listing associated with this employer using the same form data
        job_listing = JobListing(
            title=job_title,
            company=company,
            experience=experience,
            salary=salary,
            location=location,
            skills=skills,
            job_vacancy_details=job_vacancy_details,
            employer=new_employer  # Associate the job listing with the new employer
        )

        db.session.add(job_listing)
        db.session.commit()

        # Redirect to a success page or the employer dashboard
        return redirect(url_for('employer_dashboard'))

    return render_template('employer.html', form=form)

# Define route for the job seeker dashboard with form handling
@app.route('/job-seeker', methods=['GET', 'POST'])
def job_seeker_dashboard():
    form = JobSeekerForm()  # Create an instance of the form

    # Query job seekers from the database for debugging
    print("Before Querying Database")
    job_seekers = JobSeeker.query.all()
    print("After Querying Database")
    print("Job Seekers from Database:", job_seekers)

    for seeker in job_seekers:
        print("First Name:", seeker.fname)
        print("Last Name:", seeker.lname)
        print("Position Applied For:", seeker.position)
        print("Resume:", seeker.resume)
        print("Slary Expected:", seeker.salary)
        
    if request.method == 'POST' and form.validate_on_submit():
        # Use the form data from the validated form
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        tel = form.tel.data
        position = form.position.data
        resume = form.resume.data
        website = form.website.data
        salary = form.salary.data
        joining = form.joining.data
        relocation = form.relocation.data
        last_employer = form.last_employer.data
        address = form.address.data

        # Handle file upload if a file is selected
        if resume:
            # You can save the uploaded file to a specific folder
            # Make sure to secure the file uploads as per your needs
            resume.save('static/uploads/' + resume.filename)

        # Check if an entry with the same email already exists
        existing_job_seeker = JobSeeker.query.filter_by(email=email).first()
        if existing_job_seeker:
            # Update the existing entry with the new data
            existing_job_seeker.fname = fname
            existing_job_seeker.lname = lname
            # Update other fields as needed
            db.session.commit()
            flash("Your information has been updated.", "success")
            return redirect(url_for('job_seeker_dashboard'))
        else:
            # Create a new JobSeeker object and add it to the database
            new_job_seeker = JobSeeker(
                fname=fname,
                lname=lname,
                email=email,
                tel=tel,
                position=position,
                resume=resume.filename if resume else None,
                website=website,
                salary=salary,
                joining=joining,
                relocation=relocation,
                last_employer=last_employer,
                address=address
                )
        db.session.add(new_job_seeker)
        db.session.commit()

        # Redirect to a success page or the job seeker dashboard
        return redirect(url_for('job_seeker_dashboard'))

    return render_template('job-seeker.html', form=form)  # Pass the form to the template

# Define route for the admin dashboard with form handling
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():

    # Logout the user to start with a clean session
    logout_user()

    if current_user.is_authenticated:
        # Redirect to admin dashboard if already logged in
        return redirect(url_for('admin_dashboard'))

    print("Before Querying Database")
    admin_listings = Admin.query.all()
    print("After Querying Database")
    print("Admin Items from Database:", admin_listings)

    for item in admin_listings:
        print("Username:", item.username)
        print("Password:", item.password_hash)

    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('admin_login.html', form=form)

# Define route for the admin dashboard with form handling
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Fetch data for job seekers and employers and pass it to the template
    job_seekers = JobSeeker.query.all()
    employers = Employer.query.all()
    return render_template('admin_dashboard.html', job_seekers=job_seekers, employers=employers)

from flask_login import logout_user

#admin logout
@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))  # Redirect to the home page after logout




if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
