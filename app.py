from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

GOOGLE_SCRIPT_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbyc1WaP-rDL4S2hRXZZdXQEquuVk0-r13hYyHegkWs8iBmbQjUPRaN5k_tl8W4G0HDK"
    "/exec"
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/date", methods=["GET", "POST"])
def date():
    # When your friend clicks Yes ❤️ on the first page
    if request.method == "GET":
        return render_template("date.html")

    # When your friend selects a date and clicks Yes 💕
    selected_date = request.form.get("selected_date")

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
