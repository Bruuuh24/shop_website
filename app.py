from flask import Flask, render_template, request, redirect, abort, flash, session
import pymysql
import hashlib 
# import json
import datetime

'''
def load_products():
    global products
    with open("products.txt", "r") as file:
        products = json.load(file)

def save_products():
    with open("products.txt", "w") as file:
        json.dump(products, file)
'''

def create_connection():
    return pymysql.connect(
        host = "10.0.0.17",
    #   host = "localhost"
    #   user = "root"
        user = "nicsok",
        password = "ANVIL",
        db = "nicsok_assessment",
        cursorclass = pymysql.cursors.DictCursor
    )    

app = Flask(__name__)

app.secret_key = "dslkklclkdsklfklkldsklfklsdlklkfrioewiotfwklkr3258"

def encrypt(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/")
def home_page():
    # if "username" in session:
    return render_template("home.html")

@app.route("/product")
def about_page():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            productkey = cursor.fetchall()
            return render_template("product.html", products = productkey)

@app.route("/login", methods = ["GET", "POST"])
def login_page():
    #if "username" in session:
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username_entered = request.form["username"]
        password_entered = request.form["password"]
        passwordencode = encrypt(password_entered)
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT password FROM users WHERE username = %s"
                values = (username_entered)
                cursor.execute(sql, values)
                result = cursor.fetchone()
                # print(result["password"], passwordencode)
            if passwordencode == result["password"]:
                session["username"] = username_entered
                return redirect("/dashboard")
            else:
                return redirect("/")
            #    flash("Incorrect Password")
    #else:
    #    flash("Already Logged In")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/managementdashboard", methods = ["GET", "POST"])
def product_manager():  
    if request.method == "GET":
        return render_template("management_dashboard.html")
    elif request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                product = request.form["product"]
                price = request.form["price"]
                product_type = request.form["product_type"]
                values = (
                    product, 
                    price, 
                    product_type, 
                )
                sql = "INSERT into products (product, price, product_type) VALUES(%s, %s, %s)"
                cursor.execute(sql, values)
                connection.commit()
            return redirect("/dashboard")
        
                
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup_page():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                username = request.form["username"]
                password_org = request.form["password"]
                default_user_type = "normal"
                password_final = encrypt(password_org)
                values = (
                    username,
                    password_final,
                    default_user_type,
                )
                sql = "INSERT into users (username, password, account_type) VALUES(%s, %s)"
                cursor.execute(sql, values)
                connection.commit()
            return redirect("/login")
        
@app.route("/view")
def view():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s", (request.args["id"]))
            productkey = cursor.fetchone()
            return render_template("view.html", product = productkey)

@app.route("/checkout")
def buy():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s", (request.args["id"]))
            productkey = cursor.fetchone()
            return render_template("checkout.html", product = productkey)

app.run(host="0.0.0.0",debug = True)