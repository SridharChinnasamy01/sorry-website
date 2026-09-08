from flask import Flask, render_template, request
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)


def send_notification(selected_date):
    sender_email = os.environ.get("SENDER_EMAIL")
    receiver_email = os.environ.get("RECEIVER_EMAIL")
    app_password = os.environ.get("EMAIL_APP_PASSWORD")

    # Check that Render has all required settings
    if not sender_email:
        raise Exception("SENDER_EMAIL is missing")

    if not receiver_email:
        raise Exception("RECEIVER_EMAIL is missing")

    if not app_password:
        raise Exception("EMAIL_APP_PASSWORD is missing")

    # Create the email
    message = EmailMessage()
    message["Subject"] = "Sorry Website - New Date Selected"
    message["From"] = sender_email
    message["To"] = receiver_email

    message.set_content(
        f"""Someone submitted the Sorry Website form.

Selected date: {selected_date}

Open your website to see the confirmation.
"""
    )

    # Connect to Gmail and send the email
    print("Connecting to Gmail SMTP...", flush=True)

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
        server.starttls()

        print("Logging in to Gmail...", flush=True)
        server.login(sender_email, app_password)

        print("Sending email...", flush=True)
        server.send_message(message)

    print("EMAIL SENT SUCCESSFULLY", flush=True)


# PAGE 1
@app.route("/")
def home():
    return render_template("index.html")


# PAGE 2
@app.route("/date")
def date():
    return render_template("date.html")


# PAGE 3
@app.route("/success", methods=["POST"])
def success():
    selected_date = request.form.get("selected_date")

    try:
        send_notification(selected_date)
        notification_sent = True

    except Exception as error:
        print("Email error:", error, flush=True)
        notification_sent = False

    return render_template(
        "success.html",
        selected_date=selected_date,
        notification_sent=notification_sent
    )


if __name__ == "__main__":
    app.run(debug=True)
