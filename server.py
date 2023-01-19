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
    regex_pass = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

    if len(username) >= 30:
        flash("Username must be less than 30 characters", "error")
        return 0

    if password != password2:
        flash("Passwords don't match!", "error")
        return 0

    if not re.fullmatch(regex_email, email):
        flash("Invalid email", "error")
        return 0

    if not re.fullmatch(regex_pass, password):
        flash(
                "Password must be at least 8 characters and must contain at "
                "least one uppercase, one lowercase and one number",
                "error"
        )
        return 0

    return 1


def get_db_connection():
    conn = sqlite3.connect('config/database/database.db')
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

    conn = get_db_connection()
    command = 'SELECT * FROM trips WHERE uid="{}"'.format(
            existing_users[0]['uid']
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
    command = 'SELECT uid FROM users WHERE username="{}"'.format(
            session.get('username')
    )
    uid = conn.execute(command).fetchall()
    print(uid)

    command = 'SELECT * FROM trips WHERE uid={} AND trip_id={}'.format(
            int(uid[0]["uid"]), current_game_id
    )

    existing_users = conn.execute(command).fetchall()
    if len(existing_users) != 0:
        conn.close()
        return redirect("/")

    command = 'SELECT * FROM quests WHERE id={}'.format(current_game_id)
    trip_name = conn.execute(command).fetchall()[0][2]

    conn.execute(
            'INSERT INTO trips (uid, trip_id, name) VALUES (?, ?, ?)',
            (int(uid[0]["uid"]), current_game_id, trip_name)
    )

    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("psw", "")
        password2 = request.form.get("psw2", "")

        email = request.form.get("email", "")
        valid_data = check_user_info(username, email, password, password2)

        if valid_data:
            conn = get_db_connection()
            command = 'SELECT * FROM users WHERE username="{}" OR mail="{}"'. \
                format(username, email)

            existing_users = conn.execute(command).fetchall()

            if len(existing_users) != 0:
                conn.close()

                flash("User already exists!", "error")
                return render_template("signup.html")

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
        username = request.form.get("uname", "")
        password = request.form.get("psw", "")

        conn = get_db_connection()
        command = 'SELECT * FROM users WHERE username="{}" OR mail="{}"'. \
            format(username, username)

        existing_users = conn.execute(command).fetchall()
        if len(existing_users) == 0:
            conn.close()

            flash("Wrong credentials!", "error")

            return render_template("login_page.html")

        if check_password_hash(existing_users[0][2], password):
            conn.close()
            session['username'] = existing_users[0][1]

            return redirect("/")

        flash("Wrong credentials!", "error")

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
    app.run(host = "0.0.0.0", port = 8080, debug = True)
