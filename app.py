import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure database (using SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact_messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Used for flash messages
db = SQLAlchemy(app)

# Create a model for storing contact form submissions
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<ContactMessage {self.id}>'

# Create the database tables (if not exist)
with app.app_context():
    db.create_all()

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

# Send email route (POST) - storing data in DB instead of sending email
@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Create a new ContactMessage object
        new_message = ContactMessage(name=name, email=email, message=message)

        try:
            # Add the message to the database
            db.session.add(new_message)
            db.session.commit()

            # Flash a success message and redirect back to the contact page
            flash("Message sent successfully!", "success")
            return redirect(url_for('contact'))

        except Exception as e:
            # Handle failure (flash an error message)
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('contact'))

# Admin route (GET) - for viewing all messages (optional)
@app.route('/admin')
def admin():
    messages = ContactMessage.query.all()  # Fetch all stored messages from the database
    return render_template('admin.html', messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
