import os
import re
import sqlite3

from flask import Flask, request, session, redirect, flash, render_template
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder = "public")
app.config["SECRET_KEY"] = "12345"
# you can use a dict as user/pass database
UPLOAD_FOLDER = './upload'
current_quest = 0


def check_user_info(username, email, password, password2):
    regex_email = r"^\S+@\S+\.\S+$"
    regex_name = r"^(?=.{6,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"
    SpecialSym = ['$', '@', '#', '%', '!']

    print("Entered function")
    if len(username) >= 30:
        print("1")
        return 0
    if password != password2:
        print("1")
        flash("Passwords don't match!", "error")
        return 0

    if not re.fullmatch(regex_email, email):
        print("2")
        return 0

    if not re.fullmatch(regex_name, username):
        print("3")
        return 0

    if len(password) < 6 or len(password) > 30:
        print("4")
        return 0

    if not any(
            char.isdigit() or char.islower() or char.isupper()
            or char in SpecialSym for char in password
    ):
        return 0
    return 1


def get_db_connection():
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/profile")
def profile():
    user = session.get('username')
    if not user:
        return redirect("/login")

    conn = get_db_connection()
    command = 'SELECT * FROM users WHERE username="{}"'.format(user)
    existing_users = conn.execute(command).fetchall()
    conn.close()

    current_game_id = session.get('game_id')
    if not current_game_id:
        return redirect("/")

    conn = get_db_connection()
    command = 'SELECT * FROM trips WHERE user="{}"'.format(
            session.get('username')
    )
    trips = conn.execute(command).fetchall()
    conn.close()
    return render_template("cont.html", user = existing_users[0], trips = trips)


@app.route("/endtrip")
def endtrip():
    current_game_id = session.get('game_id')
    if not current_game_id:
        return redirect("/")

    conn = get_db_connection()
    command = 'SELECT * FROM trips WHERE user="{}" AND trip_id={}'.format(
            session.get('username'), current_game_id
    )
    existing_users = conn.execute(command).fetchall()
    if len(existing_users) != 0:
        conn.close()
        print("User already existing!")
        flash("User already exists!", "error")
        return redirect("/")

    command = 'SELECT * FROM quests WHERE id={}'.format(current_game_id)
    trip_name = conn.execute(command).fetchall()[0][2]

    print("Adding game")
    conn.execute(
            'INSERT INTO trips (user, trip_id, name) VALUES (?, ?, ?)',
            (session.get('username'), current_game_id, trip_name)
    )
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == "POST":
        print("test")
        username = request.form.get("username", "")
        password = request.form.get("psw", "")
        password2 = request.form.get("psw2", "")

        email = request.form.get("email", "")
        valid_data = check_user_info(username, email, password, password2)
        if valid_data:
            conn = get_db_connection()
            command = 'SELECT * FROM users WHERE username="{}" OR mail="{}"'. \
                format(username, email)

            print(command)
            existing_users = conn.execute(command).fetchall()

            if len(existing_users) != 0:
                conn.close()
                print("User already existing!")
                flash("User already exists!", "error")
                return render_template("signup.html")

            print("Valid data")
            password = generate_password_hash(password, "sha256")
            conn.execute(
                    'INSERT INTO users (username, password, mail) VALUES \
                    (?, ?, ?)', (username, password, email)
            )
            conn.commit()
            conn.close()
            return redirect("/login")

    return render_template("signup.html")


@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        print("test")
        username = request.form.get("uname", "")
        password = request.form.get("psw", "")
        valid_data = check_user_info(
                username, "test_email@test.com", password, password
        )

        if valid_data:
            conn = get_db_connection()
            command = 'SELECT * FROM users WHERE username="{}" OR mail="{}"'. \
                format(username, username)

            print(command)
            existing_users = conn.execute(command).fetchall()
            if len(existing_users) == 0:
                conn.close()

                print("User doesn't exist!")
                flash("User doesn't exist!", "error")

                return render_template("login_page.html")

            print("Valid data")
            if check_password_hash(existing_users[0][2], password):
                print("Valid password! Logging user in")

                conn.close()
                session['username'] = existing_users[0][1]

                return redirect("/")

            print("Passwords don't match")
            flash("Wrong password!", "error")

            conn.close()

    return render_template("login_page.html")


@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")


@app.route("/game")
def game():
    if not session.get('username'):
        return redirect("/login")

    current_quest = request.args.get('game_id')
    got_request = 1

    if not current_quest:
        current_quest = 1
        got_request = 0
    else:
        session['game_id'] = current_quest

    if current_quest:
        conn = get_db_connection()
        command = 'SELECT * FROM quests WHERE id={}'.format(current_quest)
        quest = conn.execute(command).fetchall()

        command = 'SELECT * FROM quests'
        all_quests = conn.execute(command).fetchall()

        conn.close()
        print(quest[0])

        return render_template(
                "Game.html", quest = quest[0], current_quest = current_quest,
                got_request = got_request, all_quests = all_quests
        )
    return "Invalid game id."


@app.route("/")
def index():
    return render_template("home.html")


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)
