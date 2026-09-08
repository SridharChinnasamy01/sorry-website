from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Your Google Apps Script Web App URL
GOOGLE_SCRIPT_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbyGmoPCuOEXwdAvN6taXLdZyQOFoRUfEtDLsEhHJ85sJsmJqnFHopdK_vy-1YSNNLSl"
    "/exec"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/date", methods=["POST"])
def date():
    # Get the date selected by your friend
    selected_date = request.form.get("selected_date")

    # Send the selected date to Google Apps Script
    try:
        response = requests.post(
            GOOGLE_SCRIPT_URL,
            json={
                "selected_date": selected_date
            },
            timeout=15
        )

        print("Google Apps Script response:", response.text)

    except requests.exceptions.RequestException as error:
        print("Email notification error:", error)

    # Show the success page even if the email request fails
    return redirect(url_for("success"))


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
