from flask import Flask, render_template, request

app = Flask(__name__)


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
    return render_template("success.html", selected_date=selected_date)


if __name__ == "__main__":
    app.run(debug=True)