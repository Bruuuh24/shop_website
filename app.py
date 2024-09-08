from flask import Flask, render_template, request, redirect, abort, flash, session, get_flashed_messages
import pymysql
import hashlib 
from datetime import datetime, timedelta

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

# deleting expired products check
def delete_expired_items():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            # delete products where the expiration date has passed
            sql = "DELETE FROM products_sold WHERE duration < NOW();"
            cursor.execute(sql)
            connection.commit()

# the route for the home page where the about and review information for the VPN is displayed. 
@app.route("/")
def home_page():
    # checks if someone has logged in and gets the account type from the database.
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
    # checks if someone has logged in and gets the account type from the database.
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
    # pulls products list and so that it can be rendered
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            productkey = cursor.fetchall()
    return render_template("product.html", products = productkey, username = username_current, account_type = account_type)

# this is the page where user's who have signed up will be able to login and access the site. 
@app.route("/login", methods = ["GET", "POST"])
def login_page():
    if request.method == "GET":
        # checks if someone has logged in and gets the account type from the database. 
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
        # checks if the password is correct or if the username doesn't exist and flashes a message
        if result is None:
            flash("Incorrect Password Or Username")
            return render_template("login.html", username = False, account_type = False)
        if passwordencode == result["password"]:
            session["username"] = username_entered
            return redirect("/dashboard")
        else:
            flash("Incorrect Password Or Username")
            return render_template("login.html", username = False, account_type = False)

# logs out the user when the link is clicked by clearing the session
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/admindashboard")
def admin_dashboard():
    # checks if someone has logged in and gets the account type from the database.
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
    # checks if the user is an admin and then gets all of the current products being sold
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
        # checks if someone has logged in and gets the account type from the database.
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
        product = request.form["product"]
        price = request.form["price"]
        product_type = request.form["product_type"]
        description = request.form["description"]
        benfits = request.form["benfits"]
        
        # Check if any input exceeds 255 characters
        if (len(product) > 255 or len(price) > 255 or 
            len(product_type) > 255 or len(description) > 255 or 
            len(benfits) > 255):
            flash("All fields must be 255 characters or fewer.")
            return redirect("/add")

        # adds new products to the page when values are correctly inputed
        with create_connection() as connection:
            with connection.cursor() as cursor:
                values = (
                    product, 
                    price, 
                    product_type, 
                    description,
                    benfits,
                )
                sql = "INSERT INTO products (product, price, product_type, description, benfits) VALUES(%s, %s, %s, %s, %s)"
                cursor.execute(sql, values)
                connection.commit()
                flash("Product added successfully!")
                return redirect("/admindashboard")

@app.route("/edit", methods = ["GET", "POST"])
def edit():  
    if request.method == "GET":
        # checks if someone has logged in and gets the account type from the database.
        if "username" in session:
            username_current = session["username"]
            with create_connection() as connection:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM users JOIN account_type ON users.account_type = account_type.id WHERE users.username = %s"
                    values = username_current
                    cursor.execute(sql, values)
                    result = cursor.fetchone()
                account_type = result["account_type"]
        else:
            username_current = False
            account_type = False
        return render_template("edit.html", username = username_current, account_type = account_type)
    elif request.method == "POST":
        id = request.form["id"]
        product = request.form["product"]
        price = request.form["price"]
        product_type = request.form["product_type"]
        description = request.form["description"]
        benfits = request.form["benfits"]
        
        # Check if any input exceeds 255 characters
        if (len(product) > 255 or len(price) > 255 or 
            len(product_type) > 255):
            flash("All fields must be 255 characters or fewer.")
            return redirect("/edit")

        # edits products when inputs are correctly added
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
                if cursor.fetchone() is None:
                    flash("Product ID does not match any existing records.")
                    return redirect("/edit")
                values = (
                    product, 
                    price, 
                    product_type, 
                    description, 
                    benfits,
                    id, 
                )
                sql = "UPDATE products SET product = %s, price = %s, product_type = %s, description = %s, benfits = %s WHERE id = %s"
                cursor.execute(sql, values)
                connection.commit()
                flash("Product updated successfully!")
                return redirect("/admindashboard")
            
@app.route("/delete", methods = ["GET", "POST"])
def delete():  
    if request.method == "GET":
        # checks if someone has logged in and gets the account type from the database.
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
        # deletes products using the id from the database
        id = request.form["id"]
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
                if cursor.fetchone() is None:
                    flash("Product ID does not match any existing records.")
                    return redirect("/delete")
                values = request.form["id"]
                sql = "DELETE FROM products WHERE id = %s"
                cursor.execute(sql, values)
                connection.commit()
                flash("Product deleted successfully!")
        return redirect("/admindashboard")

@app.route("/dashboard")
def dashboard():
    if "username" in session:
        # checks if someone has logged in and gets the account type from the database.
        flash("Logged In Successfully!")
        username_current = session["username"]
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users JOIN account_type ON users.account_type = account_type.id WHERE users.username = %s"
                values = username_current
                cursor.execute(sql, values)
                result = cursor.fetchone()
            account_type = result["account_type.account_type"]

        # checks if products are expired
        delete_expired_items()
        
        # checks for the products owned by the user
        username_current = session["username"]
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT product, duration, date FROM products_sold WHERE user = %s"
                values = username_current
                cursor.execute(sql, values)
                products_sold = cursor.fetchall()
        return render_template("dashboard.html", username = username_current, account_type = account_type, products_sold = products_sold)
    else:
        username_current = False
        account_type = False
        return redirect("/")
        
@app.route("/signup", methods = ["GET", "POST"])
def signup_page():
    if request.method == "GET":
        if "username" in session:
            # checks if someone has logged in and gets the account type from the database.
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
        # checks for if the username is taken and if not inserts the information into the database
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
        # checks if someone has logged in and gets the account type from the database.
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
    # gets the product with the id from the database
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s", (request.args["id"]))
            productkey = cursor.fetchone()
            return render_template("view.html", product = productkey, username = username_current, account_type = account_type)

@app.route("/cart")
def cart():
    if "username" in session:
        # checks if someone has logged in and gets the account type from the database.
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

    # check if the user has logged in
    if not username_current:
        flash("Please Login to buy a subscription or signup for an account")
        return redirect("/login")

    product_id = request.args['id']  # Get the product ID from the query parameter

    # checks if the product id is valid
    if not product_id:
        flash('Invalid product ID.')
        return redirect("/product")

    # inserts products into the cart if they are valid and then renders the template
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

    cart_id = request.args['id']  # Get the cart item ID
    username = session['username']

    # checks if the cart's items id's are valid
    if not cart_id:
        flash('Invalid cart item.')
        return redirect("/viewcart")

    # removes the item from the cart and the database
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
        # checks if someone has logged in and gets the account type from the database.
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
    username_current = session["username"]
    with create_connection() as connection:
                with connection.cursor() as cursor:
                    sql = "SELECT cart.id as cart_id, products.product, products.price, cart.quantity FROM cart \
                           JOIN products ON cart.product_id = products.id WHERE cart.user = %s"
                    value = username_current
                    cursor.execute(sql, value)
                    cart_items = cursor.fetchall()
                    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    if request.method == "GET":
        if "username" in session:
        # checks if someone has logged in and gets the account type from the database.
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
            return redirect("/login")
        else:
            return render_template("payment.html", username = username_current, account_type = account_type, total_price = total_price, \
                                   cart_items = cart_items)
    elif request.method == "POST":
        # request information from the form
        username_current = session["username"]
        card_number = request.form["card_number"]
        expiry_date = request.form["expiry_date"]
        cvv = request.form["cvv"]
        # checks if the information is all filled in
        if not card_number or not expiry_date or not cvv:
            flash("Fill in all fields")
            return redirect("/payment")
        # checks if the expiry date format is correct
        try:
            month, year = expiry_date.split('/')
            month = int(month)
            year = int(year)
        except ValueError:
            flash("Invalid expiry date format. Use MM/YY.")
            return redirect("/payment")

        # Validate month and year
        current_year = datetime.now().year % 100  # Last two digits of current year
        current_month = datetime.now().month

        # checks if the month is valid for the expiry date then flashes a message if so
        if month < 1 or month > 12:
            flash("Invalid month in expiry date.")
            return redirect("/payment")

        # checks if the card's year if correct and if its expired then flashes a message if so
        if year < current_year or (year == current_year and month < current_month):
            flash("The card has expired.")
            return redirect("/payment")
        
        # gets product from the cart and then insert the item into the products sold so that it can be displayed in the dashboard.
        for item in cart_items:
            product = item["product"]
            cart_id = item["cart_id"]
        date = datetime.now()
        duration = datetime.now() + timedelta(days=30)
        quantity = 1
        with create_connection() as connection:
            with connection.cursor() as cursor:
                for item in cart_items:
                    product = item["product"]
                    cart_id = item["cart_id"]
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
                    sql = "DELETE FROM cart WHERE id = %s"
                    values = cart_id
                    cursor.execute(sql, values)
            connection.commit()
        return redirect("/dashboard")

# runs the flask application
app.run(host="0.0.0.0",port=5001,debug = True)