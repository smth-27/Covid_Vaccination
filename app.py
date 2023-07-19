# main.py
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Smth"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:hebn0jgp@localhost:5432/covid_vaccination"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app,session_options={"expire_on_commit": False})
# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

# VaccinationCenter model
class VaccinationCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    working_hours = db.Column(db.String(100), nullable=False)

    def __init__(self, name, location, working_hours):
        self.name = name
        self.location = location
        self.working_hours = working_hours

# Login route for users
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["user_id"] = user.id
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html", error="")

# Sign up route for users
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("signup.html")

# Dashboard route for users
@app.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if user_id:
        return render_template("dashboard.html")
    else:
        return redirect("/login")

# Logout route for users
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/login")

# Login route for admin
@app.route("/admin/login", methods=["GET", "POST"])
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

# Admin dashboard route
@app.route("/admin/dashboard")
def admin_dashboard():
    admin_id = session.get("admin_id")
    if admin_id:
        return render_template("admin_dashboard.html")
    else:
        return redirect("/admin/login")

# Add Vaccination Centre route for admin
@app.route("/admin/add_vaccination_center", methods=["GET", "POST"])
def add_vaccination_center():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        working_hours = request.form["working_hours"]
        new_center = VaccinationCenter(name=name, location=location, working_hours=working_hours)
        db.session.add(new_center)
        db.session.commit()
        return redirect("/admin/dashboard")
    return render_template("add_vaccination_center.html")

# Remove Vaccination Centre route for admin
@app.route("/admin/remove_vaccination_center/<int:center_id>", methods=["POST"])
def remove_vaccination_center(center_id):
    center = VaccinationCenter.query.get(center_id)
    db.session.delete(center)
    db.session.commit()
    return redirect("/admin/dashboard")

# Vaccination Centre List route for users and admin
@app.route("/vaccination_centers")
def vaccination_centers():
    centers = VaccinationCenter.query.all()
    return render_template("vaccination_centers.html", centers=centers)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
