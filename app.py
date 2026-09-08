from flask import Flask, render_template, request
import os
import urllib.parse
import urllib.request

app = Flask(__name__)


def send_notification(selected_date):
    receiver_email = os.environ.get("RECEIVER_EMAIL")

    if not receiver_email:
        raise Exception("RECEIVER_EMAIL is missing")

    # FormSubmit email endpoint
    url = f"https://formsubmit.co/{receiver_email}"

    data = urllib.parse.urlencode({
        "Subject": "Sorry Website - New Date Selected",
        "Selected Date": selected_date,
        "message": (
            "Someone submitted the Sorry Website form.\n\n"
            f"Selected date: {selected_date}\n\n"
            "Open your website to see the confirmation."
        ),
        "_captcha": "false",
        "_template": "table"
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise Exception(f"Email service returned status {response.status}")

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
