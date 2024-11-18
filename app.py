from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact_messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # for flashing messages
db = SQLAlchemy(app)

# Create the database model
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<ContactMessage {self.id}>'

# Create database tables (if not exist)
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Contact route (GET)
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route to handle form submission (POST)
@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Save the message to the database
        new_message = ContactMessage(name=name, email=email, message=message)

        try:
            db.session.add(new_message)
            db.session.commit()
            flash("Message sent successfully!", "success")
            return redirect(url_for('contact'))

        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('contact'))

if __name__ == "__main__":
    app.run(debug=True)
