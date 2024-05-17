from cs50 import SQL
import os
from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from datetime import datetime as dt
import json
from werkzeug.utils import secure_filename
from flask import send_from_directory

from helpers import login_required

# Upload file
UPLOAD_FOLDER = './static/img/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///travel.db")

# Error dict
error_dict = {"num": "", "msg": "", "url": "", "name": ""}


# 404 error handling
@app.errorhandler(404)
def error_404(error):
    error_dict.update(num = 404, msg = "Page Is Not Exist", url = "", name = "Home")
    return render_template('error.html', error_dict = error_dict)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    """Log user in"""
    if request.method == "POST":
        username = request.form.get("username")
        birthday = request.form.get("birthday")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            error_dict.update(num = 400, msg = "Must Provide Username", url = "login", name = "Log In")
            return render_template('error.html', error_dict = error_dict)

        # Ensure username was submitted
        if not birthday:
            error_dict.update(num = 400, msg = "Must Provide Birthday", url = "login", name = "Log In")
            return render_template('error.html', error_dict = error_dict)

        # Ensure password was submitted
        elif not password:
            error_dict.update(num = 400, msg = "Must Provide Password", url = "login", name = "Log In")
            return render_template('error.html', error_dict = error_dict)

        # Query database for username
        else:
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            if len(rows) != 1 or not check_password_hash(
                rows[0]["hash"], request.form.get("password")
            ):
                error_dict.update(num = 403, msg = "invalid username and/or password", url = "login", name = "Log In")
                return render_template('error.html', error_dict = error_dict)

            elif rows[0]["birthday"] != birthday:
                print(rows[0]["birthday"])
                print(birthday)
                error_dict.update(num = 403, msg = "invalid birthday", url = "login", name = "Log In")
                return render_template('error.html', error_dict = error_dict)

            else:
                # Remember which user has logged in
                session["user_id"] = rows[0]["id"]

                # Redirect user to home page
                return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return render_template('login.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        birthday = request.form.get("birthday")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        today = datetime.date.today()
        if birthday:
            birthday_datetime = dt.strptime(birthday, '%Y-%m-%d')
            birthday_date = birthday_datetime.date()

        # Ensure username was submitted
        if not username:
            error_dict.update(num = 400, msg = "Must Provide Username", url = "register", name = "Register")
            return render_template('error.html', error_dict = error_dict)

        # Ensure birthday was submitted
        if not birthday:
            error_dict.update(num = 400, msg = "Must Provide Birthday", url = "register", name = "Register")
            return render_template('error.html', error_dict = error_dict)

        # Ensure password was submitted
        elif not password:
            error_dict.update(num = 400, msg = "Must Provide Password", url = "register", name = "Register")
            return render_template('error.html', error_dict = error_dict)

        # Ensure password and conform password are same
        elif password != confirmation:
            error_dict.update(num = 400, msg = "Passwords Do Not Match", url = "register", name = "Register")
            return render_template('error.html', error_dict = error_dict)

        # Ensure birthday is correct date
        elif birthday_date > today:
            error_dict.update(num = 400, msg = "Must Put Your Correct Birthday", url = "register", name = "Register")
            return render_template('error.html', error_dict = error_dict)

        else:
            # Check the username is already exist
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            if len(rows) != 0:
                error_dict.update(num = 400, msg = "Username Alrady Exitst", url = "register", name = "Register")
                return render_template('error.html', error_dict = error_dict)

            else:
                # Query database for username
                db.execute("INSERT INTO users (username, hash, birthday, register_date, update_date) VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", username, generate_password_hash(password), birthday_date)
                rows = db.execute("SELECT * FROM users WHERE username = ?", username)
                session["user_id"] = rows[0]["id"]

                return redirect("/")
    else:
        return render_template('register.html')


@app.route("/")
@login_required
def index():
    """Show home page"""
    user_id = session["user_id"]
    rows = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = rows[0]['username']

    return render_template("index.html", username = username)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change Password"""
    if request.method == "POST":
        user_id = session["user_id"]
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        crt_psw = request.form.get("crt_psw")
        cfm_pwd = request.form.get("cfm_pwd")
        new_psw = request.form.get("new_psw")

        if not crt_psw:
            error_dict.update(num = 400, msg = "Must Provide Current Password", url = "change_password", name = "Change Password")
            return render_template('error.html', error_dict = error_dict)

        elif not cfm_pwd:
            error_dict.update(num = 400, msg = "Must Provide Comfirm Password", url = "change_password", name = "Change Password")
            return render_template('error.html', error_dict = error_dict)

        elif not new_psw:
            error_dict.update(num = 400, msg = "Must Provide New Password", url = "change_password", name = "Change Password")
            return render_template('error.html', error_dict = error_dict)

        elif crt_psw != cfm_pwd:
            error_dict.update(num = 400, msg = "Password Does Not Same", url = "change_password", name = "Change Password")
            return render_template('error.html', error_dict = error_dict)

        elif len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("crt_psw")
        ):
            error_dict.update(num = 403, msg = "Invalid Username and/or Password", url = "change_password", name = "Change Password")
            return render_template('error.html', error_dict = error_dict)

        else:
            db.execute(
                "UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_psw), user_id
            )

            flash('You were successfully Changed Password')
            return redirect("/")
    else:
        return render_template('change_password.html')


@app.route("/wish", methods=["GET", "POST"])
@login_required
def wish():
    """Wish List Page"""
    wish_dict = {"username": "", "this_year": "", "seasons": "", "regions_rows": "", "country_rows": "", "relationship": "", "msg": ""}

    user_id = session["user_id"]
    rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    username = rows[0]['username']

    if request.method == "POST":
        year = request.form.get("year")
        season = request.form.get("season")

        region = request.form.get("region")
        # region_replace = region.replace("'", "\"")
        # dict_region = json.loads(region_replace)

        country = request.form.get("country")
        # country_replace = country.replace("'", "\"")
        # dict_country = json.loads(country_replace)

        relationship = request.form.get("relationship")

        if not year:
            error_dict.update(num = 400, msg = "Must Select Year", url = "wish", name = "Wish")
            return render_template('error.html', error_dict = error_dict)

        elif not season:
            error_dict.update(num = 400, msg = "Must Select Season", url = "wish", name = "Wish")
            return render_template('error.html', error_dict = error_dict)

        elif not region:
            error_dict.update(num = 400, msg = "Must Select Region", url = "wish", name = "Wish")
            return render_template('error.html', error_dict = error_dict)

        elif not country:
            error_dict.update(num = 400, msg = "Must Select Country", url = "wish", name = "Wish")
            return render_template('error.html', error_dict = error_dict)

        elif not relationship:
            error_dict.update(num = 400, msg = "Must Select Relationship", url = "wish", name = "Wish")
            return render_template('error.html', error_dict = error_dict)
        else:
            db.execute("INSERT INTO wish_list (user_id, year, season, region_id, country_id, with_who, register_date, update_date) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", user_id, year, season, region, country, relationship)
            # db.execute("INSERT INTO wish_list (user_id, year, season, region_id, country_id, with_who, register_date, update_date) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", user_id, year, season, dict_region['id'], dict_country['id'], relationship)
            flash("Your Wish Saved")


    # Select this year
    dt_now = datetime.datetime.now()
    this_year = dt_now.year

    # Season list
    seasons = ["Spring", "Summer", "Autumn", "Winter"]

    # Form date
    regions_rows = db.execute("SELECT * FROM region")
    country_rows = db.execute("SELECT * FROM country")

    # relationship list
    relationship = ["Just myself", "With my family", "With my partner", "With my friends"]

    wish_dict.update(username = username, this_year = this_year, seasons = seasons, regions_rows = regions_rows, country_rows = country_rows, relationship = relationship)

    db_date = db.execute("SELECT * FROM wish_list WHERE user_id = ? ORDER BY year", user_id)
    if len(db_date) != 0:
        regions_date = db.execute("SELECT * FROM region")
        countries_date = db.execute("SELECT * FROM country;")
        return render_template("wish.html", wish_dict = wish_dict, db_date = db_date, regions_date = regions_date, countries_date = countries_date)

    else:
        msg = "No Wish List Saved"
        return render_template("wish.html", wish_dict = wish_dict, msg = msg)


@app.route("/travel", methods=["GET", "POST"])
@login_required
def travel():
    """travel List Page"""
    user_id = session["user_id"]
    rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    username = rows[0]['username']
    birthday_year = rows[0]['birthday'][0:4]
    int_birthday_year = int(birthday_year)

    traveled_dict = {"username": "", "this_year": "", "seasons": "", "regions_rows": "", "country_rows": "", "relationship": "", "birthday_year": "", "msg": ""}

    if request.method == "POST":
        year = request.form.get("year")
        season = request.form.get("season")

        region = request.form.get("region")
        # if region is str not dirc, replace str to dict (No.1)
            # region_replace = region.replace("'", "\"")
            # dict_region = json.loads(region_replace)

        country = request.form.get("country")
        # if country is str not dirc, replace str to dict
            # country_replace = country.replace("'", "\"")
            # dict_country = json.loads(country_replace)


        relationship = request.form.get("relationship")

        # Upload file save
        if 'travel_file' not in request.files:
            error_dict.update(num = 400, msg = "Must Upload a file", url = "travel", name = "Travel")
            return render_template('error.html', error_dict = error_dict)

        file = request.files['travel_file']

        if file.filename == '':
            error_dict.update(num = 400, msg = "The File Is Not Exist", url = "travel", name = "Travel")
            return render_template('error.html', error_dict = error_dict)

        if file and allwed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(f"filename: {filename}")

        if not year:
            error_dict.update(num = 400, msg = "Must Select Year", url = "travel", name = "Travel")
            return render_template('error.html', error_dict = error_dict)

        elif not season:
            error_dict.update(num = 400, msg = "Must Select Season", url = "travel", name = "Travel")
            return render_template('error.html', error_dict = error_dict)

        elif not region:
            error_dict.update(num = 400, msg = "Must Select Region", url = "travel", name = "Travel")
            return render_template('error.html', error_dict = error_dict)

        elif not country:
            error_dict.update(num = 400, msg = "Must Select Country", url = "travel", name = "Travel")
            return render_template('error.html', error_dict = error_dict)

        elif not relationship:
            error_dict.update(num = 400, msg = "Must Select Relationship", url = "travel", name = "Travel")
            return render_template('error.html', error_dict = error_dict)
        else:
            file_pass = "../static/img/upload/"+filename

            # if javascript region,country return name not id, get id (No.2)
                # regions_date = db.execute("SELECT * FROM region")
                # countries_date = db.execute("SELECT * FROM country;")
                # for area in regions_date:
                #     if area['name'] == region:
                #         region_id = area['id']
                #         print(f"region_id: {region_id}")

                # for kuni in countries_date:
                #     if kuni['name'] == country:
                #         country_id = kuni['id']
                #         print(f"country_id: {country_id}")

            db.execute("INSERT INTO traveled_list (user_id, year, season, region_id, country_id, with_who, file_pass, register_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", user_id, year, season, region, country, relationship, file_pass)
            # No.1
                # db.execute("INSERT INTO traveled_list (user_id, year, season, region_id, country_id, with_who, file_pass, register_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", user_id, year, season, dict_region['id'], dict_country['id'], relationship, file_pass)
            # No.2
                # db.execute("INSERT INTO traveled_list (user_id, year, season, region_id, country_id, with_who, file_pass, register_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", user_id, year, season, region_id, country_id, relationship, file_pass)

            flash("Your travel report is Saved")

    # Select this year
    dt_now = datetime.datetime.now()
    this_year = dt_now.year

    # Season list
    seasons = ["Spring", "Summer", "Autumn", "Winter"]

    # Form date
    regions_rows = db.execute("SELECT * FROM region")
    country_rows = db.execute("SELECT * FROM country")

    # relationship list
    relationship = ["Just myself", "With my family", "With my partner", "With my friends"]

    traveled_dict.update(username = username, this_year = this_year, seasons = seasons, regions_rows = regions_rows, country_rows = country_rows, relationship = relationship, birthday_year = int_birthday_year)

    db_date = db.execute("SELECT * FROM traveled_list WHERE user_id = ? ORDER BY year", user_id)
    if len(db_date) != 0:
        regions_date = db.execute("SELECT * FROM region")
        countries_date = db.execute("SELECT * FROM country;")
        return render_template("travel.html", traveled_dict = traveled_dict, db_date = db_date, regions_date = regions_date, countries_date = countries_date)

    else:
        msg = "No travel Date Saved"
        return render_template("travel.html", traveled_dict = traveled_dict, msg = msg)


def allwed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
