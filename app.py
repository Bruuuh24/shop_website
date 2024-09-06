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
    # checks if the someone has logged in and gets the account type from the database.
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
    # checks if the someone has logged in and gets the account type from the database.
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
        # checks if the someone has logged in and gets the account type from the database. 
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
        if "username" in session:
            flash("Already Logged In!")
            return redirect("/dashboard")
    
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
        if result is None:
            flash("Incorrect Password Or Username")
            return render_template("login.html", username = False, account_type = False)
        if passwordencode == result["password"]:
            session["username"] = username_entered
            return redirect("/dashboard")
        else:
            flash("Incorrect Password Or Username")
            return render_template("login.html", username = False, account_type = False)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/admindashboard")
def admin_dashboard():
    # checks if the someone has logged in and gets the account type from the database.
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

# the route for the add page which where you can add new products to the database.
@app.route("/add", methods = ["GET", "POST"])
def add():  
    if request.method == "GET":
        # checks if the someone has logged in and gets the account type from the database.
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
                description = request.form["description"]
                benfits = request.form["benfits"]
                values = (
                    product, 
                    price, 
                    product_type, 
                    description,
                    benfits,
                )
                sql = "INSERT into products (product, price, product_type, description, benfits) VALUES(%s, %s, %s, %s)"
                cursor.execute(sql, values)
                connection.commit()
                return redirect("/admindashboard")

@app.route("/edit", methods = ["GET", "POST"])
def edit():  
    if request.method == "GET":
        # checks if the someone has logged in and gets the account type from the database.
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
        # checks if the someone has logged in and gets the account type from the database.
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
        # checks if the someone has logged in and gets the account type from the database.
        flash("Logged In Successfully!")
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
    if "username" in session:
        return render_template("dashboard.html", username = username_current, account_type = account_type)
    else:
        return redirect("/")

@app.route("/signup", methods = ["GET", "POST"])
def signup_page():
    if request.method == "GET":
        if "username" in session:
            # checks if the someone has logged in and gets the account type from the database.
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
                username_entered = request.form["username"]
                value = username_entered
                sql = "SELECT username FROM users WHERE username = %s"
                cursor.execute(sql, value)
                result = cursor.fetchone()
                # print(result)
                if result:
                    flash("This Username Is Already Taken")
                    return render_template("signup.html")
                else:
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
        # checks if the someone has logged in and gets the account type from the database.
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

@app.route("/cart")
def cart():
    if "username" in session:
        # checks if the someone has logged in and gets the account type from the database.
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

    if not username_current:
        flash("Please Login to buy a subscription or signup for an account")
        return redirect("/login")

    product_id = request.args.get('id')  # Get the product ID from the query parameter

    if not product_id:
        flash('Invalid product ID.')
        return redirect("/product")

    with create_connection() as connection:
        with connection.cursor() as cursor:
            # Check if the product exists in the products table
            cursor.execute('SELECT product, price FROM products WHERE id = %s', (product_id,))
            product_data = cursor.fetchone()

            if not product_data:
                flash('Product not found.')
                return redirect("/product")
            
            product = product_data["product"]
            price = product_data["price"]
            
            # Insert the product into the cart for the current user
            sql = "INSERT INTO cart (user, product_id, product, price, quantity) VALUES (%s, %s, %s, %s, %s)"
            values = (
                username_current, 
                product_id,
                product,
                price,
                1,
            )
            cursor.execute(sql, values)
            connection.commit()

            flash(f'Added {product} to cart.')

    return redirect("/product")

@app.route('/removefromcart')
def remove_from_cart():
    # Ensure the user is logged in
    if 'username' not in session:
        flash('You must be logged in to remove items from the cart.')
        return redirect("/login")

    cart_id = request.args.get('id')  # Get the cart item ID
    username = session['username']

    if not cart_id:
        flash('Invalid cart item.')
        return redirect("/viewcart")

    with create_connection() as connection:
        with connection.cursor() as cursor:
            # Remove the item from the cart
            cursor.execute('DELETE FROM cart WHERE id = %s AND user = %s', (cart_id, username))
            connection.commit()

    flash('Item removed from cart.')
    return redirect("/viewcart")

@app.route("/viewcart")
def view_cart():
    if "username" in session:
        # checks if the someone has logged in and gets the account type from the database.
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
            # Get all cart items for the current user
            sql = "SELECT cart.id as cart_id, products.product, products.price, cart.quantity FROM cart \
                   JOIN products ON cart.product_id = products.id WHERE cart.user = %s"
            value = username_current
            cursor.execute(sql, value)
            cart_items = cursor.fetchall()
    
    # Calculate the total price
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    return render_template("cart.html", username = username_current, account_type = account_type, \
                           cart_items = cart_items, total_price = total_price)
                                
        
@app.route("/payment", methods = ["GET", "POST"])
def payment():
    if request.method == "GET":
        if "username" in session:
        # checks if the someone has logged in and gets the account type from the database.
            username_current = session["username"]
            with create_connection() as connection:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM users JOIN account_type ON users.account_type = account_type.id WHERE users.username = %s"
                    values = username_current
                    cursor.execute(sql, values)
                    result = cursor.fetchone()
                    sql = "SELECT cart.id as cart_id, products.product, products.price, cart.quantity FROM cart \
                           JOIN products ON cart.product_id = products.id WHERE cart.user = %s"
                    value = username_current
                    cursor.execute(sql, value)
                    cart_items = cursor.fetchall()
                    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
                account_type = result["account_type.account_type"]
        else:
            username_current = False
            account_type = False
        if not username_current:
            return redirect("/login")
        else:
            return render_template("payment.html", username = username_current, account_type = account_type, total_price = total_price, \
                                   cart_items = cart_items)
    elif request.method == "POST":
        amount = request.form.get('amount')
        card_number = request.form.get('card_number')
        expiry_date = request.form.get('expiry_date')
        cvv = request.form.get('cvv')
        if not amount or not card_number or not expiry_date or not cvv:
            flash("Fill in all fields")
            return render_template("payment", username = username_current, account_type = account_type, total_price = total_price, \
                                   cart_items = cart_items)
        else:
            username_current = session["username"]
            product = cart_items["product"]
            date = datetime.now()
            duration = "1"
            quantity = 1
            with create_connection() as connection:
                with connection.cursor() as cursor:
                    values = (
                        username_current,
                        product,
                        date, 
                        duration, 
                        quantity, 
                    )
                    sql = "INSERT into products_sold (user, product, date, duration, quantity) VALUES(%s, %s, %s, %s, %s)"
                    cursor.execute(sql, values)
                    connection.commit()
                    return redirect("/dashboard")
                
'''
@app.route("/review")
def review():
    if "username" in session:
        # checks if the someone has logged in and gets the account type from the database.
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
'''

app.run(host="0.0.0.0",port=5001,debug = True)