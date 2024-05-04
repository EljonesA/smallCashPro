from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# test user database
users = {'user@example.com': {'password': 'test'}}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(user_id):
        if user_id in users:
            return User(user_id)
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['email']
        password = request.form['password']
        if user_id in users and users[user_id]['password'] == password:
            user = User(user_id)
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users[request.form['email']] == {'password': request.form['password']}
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/')
@login_required
def home():
    return 'Welcome to your dashboard'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main_':
    app.run(debug=True)
