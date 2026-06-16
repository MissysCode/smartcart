import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        db = get_db()
        error = None

        if not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                    (email, generate_password_hash(password)),
                )
                db.commit()
            except sqlite3.IntegrityError:
                error = "An account with this email already exists."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        db = get_db()
        error = None

        user = db.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,),
        ).fetchone()

        if user is None:
            error = "Incorrect email."
        elif not check_password_hash(
            user["password_hash"],
            password
        ):
            error = "Incorrect password."

        if error is None:
            return redirect(url_for("main.home"))

        flash(error)

    return render_template("login.html")


@auth.route("/logout")
def logout():
    return "Logout will go here"