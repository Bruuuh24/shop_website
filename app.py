from flask import Flask, render_template, request, redirect, abort, flash, session
import pymysql
import hashlib 

def create_connection():
    return pymysql.connect(
        host = "10.0.0.17",
        user = "nicsok",
        password = "ANVIL",
        db = "nicsok_assessment",
        cursorclass = pymysql.cursors.DictCursor
    )

app = Flask(__name__)

def encrypt(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/product")
def about_page():
    return render_template("product.html")

@app.route("/login")
def login_page():
    #with create_connection() as connection:
    #    with connection.cursor() as cursor:
    #        cursor.excute
    return render_template("login.html")

app.run(debug = True)