from flask import Flask, render_template, request, redirect, session
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "Smth"

# Configure the MongoDB connection
app.config["MONGO_URI"] = "mongodb://localhost:8000/covid_vaccination"
mongo = PyMongo(app)

# User collection
users = mongo.db.users

# VaccinationCenter collection
vaccination_centers = mongo.db.vaccination_centers

# User Use Cases
@app.route("/html/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.find_one({"username": username, "password": password})
        if user:
            session["user_id"] = str(user["_id"])
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html", error="")

@app.route("/html/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.find_one({"username": username})
        if user:
            return render_template("signup.html", error="Username already exists.")
        else:
            user_data = {"username": username, "password": password}
            users.insert_one(user_data)
            return redirect("/login")
    return render_template("signup.html", error="")

@app.route("/html/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if user_id:
        return render_template("dashboard.html")
    else:
        return redirect("/login")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/login")

# Admin Use Cases

@app.route("/html/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Implement admin authentication logic here
        if username == "admin" and password == "admin123":
            session["admin_id"] = 1
            return redirect("/admin/dashboard")
        else:
            return render_template("admin_login.html", error="Invalid username or password")
    return render_template("admin_login.html", error="")

@app.route("/html/admin_dashboard")
def admin_dashboard():
    admin_id = session.get("admin_id")
    if admin_id:
        return render_template("admin_dashboard.html")
    else:
        return redirect("/admin/login")

@app.route("/html/add_vaccination_center", methods=["GET", "POST"])
def add_vaccination_center():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        working_hours = request.form["working_hours"]
        center_data = {"name": name, "location": location, "working_hours": working_hours}
        vaccination_centers.insert_one(center_data)
        return redirect("/admin/dashboard")
    return render_template("add_vaccination_center.html")

@app.route("/admin/remove_vaccination_center/<string:center_id>", methods=["POST"])
def remove_vaccination_center(center_id):
    vaccination_centers.delete_one({"_id": center_id})
    return redirect("/admin/dashboard")

@app.route("/vaccination_centers")
def vaccination_centers():
    centers = vaccination_centers.find()
    return render_template("vaccination_centers.html", centers=centers)

if __name__ == "__main__":
    app.run(debug=False)
