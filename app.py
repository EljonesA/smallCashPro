from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import create_engine, Column, String, Integer, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from flask_mail import Mail, Message
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['UPLOAD_FOLDER'] = '/home/eljones/smallCashPro/static/images'

# Database configuration
sql_connection = 'mysql+mysqldb://jones:passwd@localhost/CREDENTIALS'
engine = create_engine(sql_connection)
Base = declarative_base()

# Login manager configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'eljones.odongo@gmail.com'
app.config['MAIL_PASSWORD'] = 'llas lfnw osjd iaob'
mail = Mail(app)

# User model definitions
# credentials model
class User(UserMixin, Base):
    __tablename__ = 'logins'

    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)

# user registration model
class UserDetails(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    full_name = Column(String(150), nullable=False)
    dob = Column(Date, nullable=False)
    phone = Column(String(20), nullable=False)
    gender = Column(String(20), nullable=False)
    id_type = Column(String(50), nullable=False)
    id_number = Column(String(50), nullable=False)
    issued_place = Column(String(100), nullable=False)
    issued_date = Column(Date, nullable=False)
    employment_status = Column(String(50), nullable=False)
    occupation = Column(String(100), nullable=False)
    employer_name = Column(String(100), nullable=False)
    years_with_employer = Column(Integer, nullable=False)
    monthly_income = Column(Integer, nullable=False)

# loan application model
class LoanApplication(Base):
    __tablename__ = 'loan_applications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    loan_type = Column(String(150), nullable=False)
    loan_limit = Column(Integer, nullable=False)
    desired_loan = Column(Integer, nullable=False)
    repayment_period = Column(String(150), nullable=False)
    due_date = Column(DateTime, nullable=False)
    interest_amount = Column(Integer, nullable=False)
    amount_due = Column(Integer, nullable=False)
    loan_reason = Column(String(150), nullable=False)
    application_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), nullable=False)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

# login route and function
#@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = session.query(User).filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

# signup route & function
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        if session.query(User).filter_by(email=email).first():
            flash('Email address already exists')
        elif password != confirm:
            flash('Passwprd mismatch')
        else:
            new_user = User(email=email, password=password)
            session.add(new_user)
            session.commit()
            return redirect(url_for('registration'))
    return render_template('signup.html')

# User Registration form
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # capture registration details & store in database
        full_name = request.form['full_name']
        dob = request.form['dob']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        id_type = request.form['id_type']
        id_number = request.form['id_number']
        issued_place = request.form['issued_place']
        issued_date = request.form['issued_date']
        employment_status = request.form['employment_status']
        occupation = request.form['occupation']
        employer_name = request.form['employer_name']
        years_with_employer = request.form['years_with_employer']
        monthly_income = request.form['monthly_income']
        
        # query user from logins table -> to get id
        user = session.query(User).filter_by(email=email).first()
        if user:
            user_details = UserDetails(
                    user_id=user.id,
                    full_name=full_name,
                    dob=dob,
                    phone=phone,
                    gender=gender,
                    id_type=id_type,
                    id_number=id_number,
                    issued_place=issued_place,
                    issued_date=issued_date,
                    employment_status=employment_status,
                    occupation=occupation,
                    employer_name=employer_name,
                    years_with_employer=years_with_employer,
                    monthly_income=monthly_income
            )
            session.add(user_details)
            session.commit()
            flash('Registration completed successfully')
            return redirect(url_for('home'))
        else:
            flash('User not found')
    return render_template('registration.html')

# app landing page
@app.route('/')
def landing():
    return render_template('landing.html')

# render landing/features page
@app.route('/features')
def features():
    return render_template('features.html')

# render lamding/about page
@app.route('/about')
def about():
    return render_template('about.html')

# app home page after login
@app.route('/home')
@login_required
def home():
    return render_template('home_two.html')

# handle user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# dashboard page route, function & logic
@app.route('/dashboard')
@login_required
def dashboard():
    total_loans = session.query(LoanApplication).count()
    approved_loans = session.query(LoanApplication).filter_by(status='Approved').count()
    rejected_loans = session.query(LoanApplication).filter_by(status='Rejected').count()
    pending_loans = session.query(LoanApplication).filter_by(status='Processing').count()

    payments_due = session.query(LoanApplication).limit(5).all()

    loan_status_counts = {
            'Approved': approved_loans,
            'Rejected': rejected_loans,
            'Pending': pending_loans
    }

    return render_template('dash.html', total_loans=total_loans, pending_loans=pending_loans,loan_status_counts=loan_status_counts, payments_due=payments_due)

# render -> paths for navigation pages
# nav bar - application form handling & logic
@app.route('/application_form', methods=['GET', 'POST'])
@login_required
def application_form():
    if request.method == 'POST':
        loan_type = request.form['loan_type']
        loan_limit = int(request.form['loan_limit'])
        desired_loan = int(request.form['desired_loan'])
        repayment_period = request.form['repayment_period']
        interest_amount = int(request.form['interest_amount'])
        amount_due = int(request.form['amount_due'])
        loan_reason = request.form['loan_reason']

        # compute due date based on repayment period
        application_date = datetime.utcnow()
        repayment_days = int(repayment_period.split()[0]) # split by space
        due_date = application_date + timedelta(days=repayment_days)

        new_application = LoanApplication(
                user_id=current_user.id,
                loan_type=loan_type,
                loan_limit=loan_limit,
                desired_loan=desired_loan,
                repayment_period=repayment_period,
                due_date=due_date,
                interest_amount=interest_amount,
                amount_due=amount_due,
                loan_reason=loan_reason,
                status='Processing'
            )
        try:
            session.add(new_application)
            session.commit() 

            # send email notification to the admin
            # retrieve applicant details
            applicant_details = session.query(UserDetails).filter_by(user_id=current_user.id).first()

            msg = Message(
                    subject="New Loan Application",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=["eljones.odongo@gmail.com"]
                    )
            msg.html = f"""
            <div style="background-color: #f0f0f0; border: 1px solid #d0d0d0; padding: 20px;">
                <p>A new loan application has been submitted. Log into <a href="#" style="color: #132e57; text-decoration: none; font-weight: bold;">smallCashPro</a> to review and approve / reject the application.</p>

                <h3>Applicant Details:</h3>
                <ul>
                    <li><strong>Full Name:</strong> {applicant_details.full_name}</li>
                    <li><strong>Monthly Income:</strong> {applicant_details.monthly_income}</li>
                </ul>

                <h3>Loan Application Details:</h3>
                    <ul>
                        <li><strong>Loan Type:</strong> {loan_type}</li>
                        <li><strong>Loan Limit:</strong> {loan_limit}</li>
                        <li><strong>Desired Loan:</strong> {desired_loan}</li>
                        <li><strong>Interest Amount:</strong> {interest_amount}</li>
                        <li><strong>Loan Reason:</strong> {loan_reason}</li>
                    </ul>

                    <footer style="background-color: #132e57; color: white; text-align: center; padding: 10px; margin-top: 20px;">
                        smallCashPro &copy; 2024
                    </footer>
                </div>
            """
            mail.send(msg)
            flash('Loan application submitted successfully', 'success')
        except Exception as e:
            session.rollback()
            flash('Failed to submit loan application.', 'error')
        
        return redirect(url_for('home'))
    return render_template('application_form.html')

# nav bar - approved report logic
@app.route('/approved')
@login_required
def approved_loans_report():
    # query db for approved loans
    approved_loans = session.query(LoanApplication).filter_by(status='Processing').all()
    return render_template('approved_loans_report.html', loans=approved_loans)

# nav bar - rejected report logic
@app.route('/rejected_loans')
def rejected_loans():
    # query db for rejected loans
    rejected_loans = session.query(LoanApplication).filter_by(status='Processing').all()
    return render_template('rejected_report.html', loans=rejected_loans)

# nav bar - all loans report logic
@app.route('/all_loans')
def all_loans():
    all_loans = session.query(LoanApplication).all()
    return render_template('all_loans_report.html')

# nav bar - settings logic
@app.route('/settings')
def settings():
    user_details = session.query(UserDetails).filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        user_details.full_name = request.form['full_name']
        user_details.dob = request.form['dob']
        user_details.phone = request.form['phone']
        user_details.gender = request.form['gender']
        User_details.id_type = request.form['id_type']
        user_details.id_number = request.form['id_number']
        user_details.issued_place = request.form['issued_place']
        user_details.issued_date = request.form['issued_date']
        user_details.employment_status = request.form['employment_status']
        user_details.occupation = request.form['occupation']
        user_details.employer_name = request.form['employer_name']
        user_details.years_with_employer = request.form['years_with_employer']
        user_details.monthly_income = request.form['monthly_income']

        # Handle profile picture update
        if 'profile_pic' in request.files:
            profile_pic = request.files['profile_pic']
            if profile_pic.filename != '':
                profile_pic_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(profile_pic.filename))
                profile_pic.save(profile_pic_path)
                user_details.profile_pic = profile_pic_path

        session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('settings'))

    user_profile_picture_url = url_for('static', filename=user_details.profile_pic) if user_details.profile_pic else url_for('static', filename='default_profile.png')
    return render_template('profile.html')


# app entry point
if __name__ == '__main__':
    app.run(debug=True)
