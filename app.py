from flask import Flask, render_template, request, redirect, abort, flash, session
import pymysql
import hashlib 
import json

def load_products():
    global products
    with open("products.txt", "r") as file:
        products = json.load(file)

def save_products():
    with open("products.txt", "w") as file:
        json.dump(products, file)

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

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/login", methods = ["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                username = request.args["username"]
                password = request.args["password"]
                username_entered = request.form["username"]
                if username == username_entered:
                    
                    cursor.execute()
                    return render_template("login.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup_page():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                username = request.form["username"]
                password_org = request.form["password"]
                password_final = encrypt(password_org)
                values = (
                    username,
                    password_final,
                )
                sql = "INSERT into users (username, password) VALUES(%s, %s)"
                cursor.execute(sql, values)
                connection.commit()
            return redirect("/login")
    
app.run(debug = True)