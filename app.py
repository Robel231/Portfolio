import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Load email credentials from environment variables
sender_email = os.getenv("robelsh30@gmail.com")
sender_password = os.getenv("aloj qleh qewu ldfz")

# Configuring Flask-Mail for sending emails
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = sender_email
app.config['MAIL_PASSWORD'] = sender_password
app.config['MAIL_DEFAULT_SENDER'] = sender_email
mail = Mail(app)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# About route
@app.route('/about')
def about():
    return render_template('about.html')

# Projects route
@app.route('/projects')
def projects():
    return render_template('projects.html')

# Contact route (GET)
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Send email route (POST)
@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Create a message instance
        msg = Message(f"New Message from {name}", recipients=[sender_email])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        try:
            # Send email
            mail.send(msg)
            return redirect(url_for('contact', message="Message sent successfully!"))
        except Exception as e:
            # Handle failure
            return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
