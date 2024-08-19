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
        # host = "10.0.0.17",
        host = "localhost",
        user = "root",
        # user = "nicsok",
        # password = "ANVIL",
        password = "v8%!~By]_K80",
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
                flash("Incorrect Password")
                return render_template("login.html")
    #else:
    #    flash("Already Logged In")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/admindashboard")
def admin_dashboard():
    return render_template("management_dashboard.html")
  
        
@app.route("/productmanager", methods = ["GET", "POST"])
def product_manager():  
    if request.method == "GET":
        return render_template("product_manager.html")
    elif request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                product = request.form["product"]
                price = request.form["price"]
                product_type = request.form["product_type"]
                try:
                    action_type = request.form["add_product"]
                    action_type = request["edit_product"]
                    action_type = request["delete_product"]
                except:
                    pass
                values = (
                    product, 
                    price, 
                    product_type, 
                )
                sql_add = "INSERT into products (product, price, product_type) VALUES(%s, %s, %s)"
                sql_edit = "UPDATE products SET (product, price, product_type) VALUES(%s, %s, %s)"
                sql_delete = "DELETE FROM products WHERE (product, price, product_type) VALUES(%s, %s, %s)"
                if action_type == "add_product":
                    cursor.execute(values, sql_add)
                    connection.commit()
                    return redirect("/dashboard")
                elif action_type == "edit_product":
                    cursor.execute(values, sql_edit)
                    connection.commit()
                    return redirect("/dashboard")
                elif action_type == "delete_product":
                    cursor.execute(values, sql_delete)
                    connection.commit()
                    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html")
    else:
        return redirect("/")

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
                sql = "INSERT into users (username, password, account_type) VALUES(%s, %s, %s)"
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

app.run(host="0.0.0.0",port=5001,debug = True)