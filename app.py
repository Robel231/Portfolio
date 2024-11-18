from flask import Flask, render_template, request, redirect, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flash messages


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send_email", methods=["POST"])
def send_email():
    # Get form data
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    # Email configuration
    sender_email = "robelsh30@gmail.com"  # Replace with your Gmail address
    sender_password = "aloj qleh qewu ldfz"  # Replace with your app-specific password
    recipient_email = "robelsh30@gmail.com"  # Your email where messages will be sent

    # Email subject and body
    subject = f"New Contact Message from {name}"
    body = f"""
    You have received a new message from your portfolio:

    Name: {name}
    Email: {email}

    Message:
    {message}
    """

    try:
        # Create the email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)  # Log in to your Gmail account
            server.send_message(msg)  # Send the email

        # Success message
        flash("Your message has been sent successfully!", "success")
    except Exception as e:
        # Error message
        flash(f"An error occurred: {e}", "danger")

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
