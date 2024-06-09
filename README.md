# smallCashPro
# Overview
__smallCashPro__ is a web-based loan application platform designed to simplify the loan application process for users. Built as part of my journey to becoming a certified software engineer through ALX, this project demonstrates a comprehensive approach to modern web development using Flask and related technologies.

# Table of Contents
- Inspiration
- Features
- Architecture
- Tech Stack
- Setup
- Usage

# Inspiration
The idea for smallCashPro originated while working on a payroll system at my day job. The payroll system included a loan module, but I envisioned a more powerful standalone loan application. This project aims to create an independent, user-friendly platform to streamline the loan application process.

# Features
- User Authentication: Secure login and registration system.
- Loan Application Form: A user-friendly form for submitting loan applications.
- Dashboard: Overview of loan status, including total loans, outstanding amounts, and pending applications.
- Reports: Detailed reports on approved and rejected loans.
- Notifications: Email notifications for loan application updates.

# Architecture
The architecture is designed with a clear separation between the frontend and backend, ensuring that each component can be developed, tested, and scaled independently. This modular approach makes it easier to maintain and extend the application in the future.

# Tech Stack
## Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap
## Backend
- Python
- Flask
## Database
- MySQL
## Other Tools
- SQLAlchemy
-Flask-Login for authentication
- Flask-Mail for email notifications

# Setup
## Prerequisites
- Python 3.8+
- MySQL
- Flask

# Installation
1. Clone the repository:
   `git clone https://github.com/yourusername/smallCashPro.git`
   `cd smallCashPro`

2. Install the dependencies:
   `pip install -r requirements.txt`
   
3. Set up the database:
   `CREATE DATABASE CREDENTIALS;`
   
5. Configure your database credentials in app.py:
   `sql_connection = 'mysql+mysqldb://yourusername:yourpassword@localhost/CREDENTIALS'`
   
7. Run the application:
   `flask run`
   
Usage
- Navigate to the home page: http://127.0.0.1:5000/
- Register a new user or log in with existing credentials.
- Apply for loans through the loan application form.
- View loan status on the dashboard.
- Admins can approve or reject loans and view detailed reports (Still in development).

## Contributing
Contributions are welcome! Please follow these steps:
- Fork the repository.
- Create a new branch: git checkout -b feature-branch
- Make your changes and commit them: git commit -m 'Add new feature'
- Push to the branch: git push origin feature-branch
- Submit a pull request.

Contact
For any inquiries or feedback, please reach out to me by sending a linkedIn message:
[LinkedIn](https://www.linkedin.com/in/eljones-odongo/)
