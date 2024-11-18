from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Secret key for session management
app.secret_key = os.urandom(24)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'robelsh30@gmail.com'  # Replace with your Gmail address
app.config['MAIL_PASSWORD'] = 'aloj qleh qewu ldfz'  # Replace with your Gmail password
mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        # Get data from the form
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Create message
        msg = Message('Contact Form Message', sender=email, recipients=['robelsh30@gmail.com'])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        # Send email
        mail.send(msg)

        # Flash success message
        flash("Your message has been sent successfully!", "success")
        return render_template("contact.html", thank_you=True)  # Display thank you message

    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
