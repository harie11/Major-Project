from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import threading

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Create tables if they don't exist
with app.app_context():
    db.create_all()
    
@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect('http://localhost:5001')
        else:
            return 'Invalid Credentials. Please try again.'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return 'Username already exists.'
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

def run_first_app():
    print("Starting first app on port 5000")
    app.run(port=5000)

def run_second_app():
    try:
        from second_app import app as second_app
        print("Starting second app on port 5001")
        second_app.run(port=5001)
    except ImportError as e:
        print(f"Error importing second app: {e}")

if __name__ == '__main__':
    t1 = threading.Thread(target=run_first_app)
    t2 = threading.Thread(target=run_second_app)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
