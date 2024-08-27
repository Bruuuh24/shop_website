from flask import Flask, render_template, request, redirect, abort, flash, session, get_flashed_messages
import pymysql
import hashlib 
import datetime

# creating connection with the SQL server 
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

# inputing the password then encrypting it to make it private
def encrypt(password):
    return hashlib.sha256(password.encode()).hexdigest()

# the route for the home page where the about and review information for the VPN is displayed. 
@app.route("/")
def home_page():
    if "username" in session:
        username_current = session["username"]
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users JOIN account_type ON users.account_type = account_type.id WHERE users.username = %s"
                values = username_current
                cursor.execute(sql, values)
                result = cursor.fetchone()
            account_type = result["account_type.account_type"]
    else:
        username_current = False
        account_type = False
    return render_template("home.html", username = username_current, account_type = account_type)

# displaying the avaliable products sold by Horizon VPN
@app.route("/product")
def product_page():
    if "username" in session:
        username_current = session["username"]
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users JOIN account_type ON users.account_type = account_type.id WHERE users.username = %s"
                values = username_current
                cursor.execute(sql, values)
                result = cursor.fetchone()
            account_type = result["account_type.account_type"]
    else:
        username_current = False
        account_type = False
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            productkey = cursor.fetchall()
    return render_template("product.html", products = productkey, username = username_current, account_type = account_type)

# this is the page where user's who have signed up will be able to login and access the site. 
@app.route("/login", methods = ["GET", "POST"])
def login_page():
    if request.method == "GET":
        if "username" in session:
            username_current = session["username"]
            with create_connection() as connection:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM users JOIN account_type ON users.account_type = account_type.id WHERE users.username = %s"
                    values = username_current
                    cursor.execute(sql, values)
                    result = cursor.fetchone()
                    print('here is the result!', result)
                account_type = result["account_type.account_type"]
        else:
            username_current = False
            account_type = False
        return render_template("login.html", username = username_current, account_type = account_type)
    elif request.method == "POST":
        username_entered = request.form["username"]
        password_entered = request.form["password"]
        passwordencode = encrypt(password_entered)
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT password FROM users WHERE username = %s"
                values = username_entered
                cursor.execute(sql, values)
                result = cursor.fetchone()
                # print(result["password"], passwordencode)
            if passwordencode == result["password"]:
                session["username"] = username_entered
                return redirect("/dashboard")
            else:
                flash("Incorrect Password Or Username")
                return render_template("login.html", username = username_current, account_type = account_type)
    #else:
    #    flash("Already Logged In")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/admindashboard")
def admin_dashboard():
    if "username" in session:
        username_current = session["username"]
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users JOIN account_type ON users.account_type = account_type.id WHERE users.username = %s"
                values = username_current
                cursor.execute(sql, values)
                result = cursor.fetchone()
            account_type = result["account_type.account_type"]
    else:
        username_current = False
        account_type = False
    if account_type == "admin":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM products")
                productkey = cursor.fetchall()
        return render_template("admin_dashboard.html", username = username_current, products = productkey, account_type = account_type)
    else:
        return redirect("/")
  
@app.route("/add", methods = ["GET", "POST"])
def add():  
    if request.method == "GET":
        if "username" in session:
            username_current = session["username"]
            with create_connection() as connection:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM users JOIN account_type ON users.account_type = account_type.id WHERE users.username = %s"
                    values = username_current
                    cursor.execute(sql, values)
                    result = cursor.fetchone()
                account_type = result["account_type.account_type"]
        else:
            username_current = False
            account_type = False
        return render_template("add.html", username = username_current, account_type = account_type)
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
                return redirect("/admindashboard")

@app.route("/edit", methods = ["GET", "POST"])
def edit():  
    if request.method == "GET":
        if "username" in session:
            username_current = session["username"]
            with create_connection() as connection:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM users JOIN account_type ON users.account_type = account_type.id WHERE users.username = %s"
                    values = username_current
                    cursor.execute(sql, values)
                    result = cursor.fetchone()
                account_type = result["account_type.account_type"]
        else:
            username_current = False
            account_type = False
        return render_template("edit.html", username = username_current, account_type = account_type)
    elif request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                id = request.form["id"]
                product = request.form["product"]
                price = request.form["price"]
                product_type = request.form["product_type"]
                values = (
                    product, 
                    price, 
                    product_type, 
                    id, 
                )
                sql = "UPDATE products SET product = %s, price = %s, product_type = %s WHERE id = %s"
                cursor.execute(sql, values)
                connection.commit()
        return redirect("/admindashboard")
            
@app.route("/delete", methods = ["GET", "POST"])
def delete():  
    if request.method == "GET":
        if "username" in session:
            username_current = session["username"]
            with create_connection() as connection:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM users JOIN account_type ON users.account_type = account_type.id WHERE users.username = %s"
                    values = username_current
                    cursor.execute(sql, values)
                    result = cursor.fetchone()
                account_type = result["account_type.account_type"]
        else:
            username_current = False
            account_type = False
        return render_template("delete.html", username = username_current, account_type = account_type)
    elif request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                values = request.form["id"]
                sql = "DELETE FROM products WHERE id = %s"
                cursor.execute(sql, values)
                connection.commit()
        return redirect("/admindashboard")

@app.route("/dashboard")
def dashboard():
    if "username" in session:
        username_current = session["username"]
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users JOIN account_type ON users.account_type = account_type.id WHERE users.username = %s"
                values = username_current
                cursor.execute(sql, values)
                result = cursor.fetchone()
            account_type = result["account_type.account_type"]
    else:
        username_current = False
        account_type = False
    return render_template("dashboard.html", username = username_current, account_type = account_type)

@app.route("/signup", methods = ["GET", "POST"])
def signup_page():
    if request.method == "GET":
        if "username" in session:
            username_current = session["username"]
            with create_connection() as connection:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM users JOIN account_type ON users.account_type = account_type.id WHERE users.username = %s"
                    values = username_current
                    cursor.execute(sql, values)
                    result = cursor.fetchone()
                account_type = result["account_type.account_type"]
        else:
            username_current = False
            account_type = False
        return render_template("signup.html", username = username_current, account_type = account_type)
    elif request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                username_org = request.form["username"]
                password_org = request.form["password"]
                default_user_type = "1"
                password_final = encrypt(password_org)
                values = (
                    username_org,
                    password_final,
                    default_user_type,
                )
                sql = "INSERT into users (username, password, account_type) VALUES(%s, %s, %s)"
                cursor.execute(sql, values)
                connection.commit()
            return redirect("/login")
        
@app.route("/view")
def view():
    if "username" in session:
        username_current = session["username"]
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users JOIN account_type ON users.account_type = account_type.id WHERE users.username = %s"
                values = username_current
                cursor.execute(sql, values)
                result = cursor.fetchone()
            account_type = result["account_type.account_type"]
    else:
        username_current = False
        account_type = False
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s", (request.args["id"]))
            productkey = cursor.fetchone()
            return render_template("view.html", product = productkey, username = username_current, account_type = account_type)

@app.route("/checkout")
def buy():
    if "username" in session:
        username_current = session["username"]
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users JOIN account_type ON users.account_type = account_type.id WHERE users.username = %s"
                values = username_current
                cursor.execute(sql, values)
                result = cursor.fetchone()
            account_type = result["account_type.account_type"]
    else:
        username_current = False
        account_type = False
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s", (request.args["id"]))
            productkey = cursor.fetchone()
            return render_template("checkout.html", product = productkey, username = username_current, account_type = account_type)
        
@app.route("/payment")
def payment():
    pass

@app.route("/review")
def review():
    if "username" in session:
        username_current = session["username"]
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users JOIN account_type ON users.account_type = account_type.id WHERE users.username = %s"
                values = username_current
                cursor.execute(sql, values)
                result = cursor.fetchone()
            account_type = result["account_type.account_type"]
    else:
        username_current = False
        account_type = False
    return render_template("review.html", username = username_current, account_type = account_type)

app.run(host="0.0.0.0",port=5001,debug = True)