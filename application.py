import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
import time


# Configure application
app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure SQLite database
db = SQL("sqlite:///restaurant.db")

# Main page
@app.route("/")
def index():
    return render_template("/index.html")

# Section "about"
@app.route("/about")
def about():
    return render_template("/about.html")

# Section "menu"
@app.route("/menu")
def menu():
    appetizer = db.execute("SELECT name FROM food WHERE type = 'APPETIZER'")
    pizza = db.execute("SELECT name FROM food WHERE type = 'PIZZA'")
    pasta = db.execute("SELECT name FROM food WHERE type = 'PASTA'")
    dessert = db.execute("SELECT name FROM food WHERE type = 'DESSERT'")
    return render_template("/menu.html", appetizer=appetizer, pizza=pizza, pasta=pasta, dessert=dessert)

# Section "opinions"
@app.route("/opinions", methods=["GET", "POST"])
def opinions():
    # Displaying opinions
    if request.method == "GET":
        opinions = db.execute("SELECT name, opinion, timestamp FROM opinions ORDER BY timestamp DESC")

    # Adding opinion
    else:
        # sumbission:
        name = request.form.get("name")
        opinion = request.form.get("opinion")

        # validating submission:
        if not name or not opinion:
            messageWrong = "Please fill in both name and opinion."
            opinions = db.execute("SELECT name, opinion, timestamp FROM opinions ORDER BY timestamp DESC")
            return render_template("/opinions.html", opinions=opinions, messageWrong=messageWrong)

        # adding opinion to database
        db.execute("INSERT INTO opinions (name, opinion, timestamp) VALUES(?, ?, ?)", name, opinion, time.strftime('%D %H:%M:%S'))
        messageOk = "Thank you for your opinion!"
        opinions = db.execute("SELECT name, opinion, timestamp FROM opinions ORDER BY timestamp DESC")
        return render_template("/opinions.html", opinions=opinions, messageOk=messageOk)

    return render_template("/opinions.html", opinions=opinions)

# Section "delivery"
@app.route("/delivery", methods=["GET", "POST"])
def delivery():
    appetizer = db.execute("SELECT id, name, price FROM food WHERE type = 'APPETIZER'")
    pizza = db.execute("SELECT id, name, price FROM food WHERE type = 'PIZZA'")
    pasta = db.execute("SELECT id, name, price FROM food WHERE type = 'PASTA'")
    dessert = db.execute("SELECT id, name, price FROM food WHERE type = 'DESSERT'")
    
    # Displaying delivery site
    if request.method == "GET":
        return render_template("/delivery.html", appetizer=appetizer, pizza=pizza, pasta=pasta, dessert=dessert)
   
    # Adding products to the cart
    else:
        # Getting product from the form
        id = request.form.get("id")
        name = db.execute("SELECT name FROM food WHERE id IN (?)", id)[0]["name"]
        price = int(db.execute("SELECT price FROM food WHERE id IN (?)", id)[0]["price"])
        number = int(request.form.get("number"))
        totalPrice = price * number

        # Starting the cart if it doesn't exist
        if "cart" not in session:
            session["cart"] = []

        # Update number of products if they are already in the cart
        for i in range(len(session["cart"])):
            if id == session["cart"][i].get("id"):
                tempNumber = int(session["cart"][i].get("number"))
                tempTotalPrice = int(session["cart"][i].get("totalPrice"))
                newNumber = tempNumber + number
                newTotalPrice = tempTotalPrice + totalPrice
                session["cart"][i].update({"number": newNumber})
                session["cart"][i].update({"totalPrice": newTotalPrice})
                message = "ok"
                return render_template("/delivery.html", message=message, appetizer=appetizer, pizza=pizza, pasta=pasta, dessert=dessert)
        
        # Add product if it's not in cart
        session["cart"].append({"id": id, "name": name,"price": price, "number": number, "totalPrice": totalPrice})
        message = "ok"
        return render_template("/delivery.html", message=message, appetizer=appetizer, pizza=pizza, pasta=pasta, dessert=dessert)

# Cart
@app.route("/cart", methods=["GET", "POST"])
def cart():
    priceSum = 0
    
    # Starting the cart if it doesn't exist
    if "cart" not in session:
        session["cart"] = []

    if request.method == "GET":
        # Summary of prices
        for i in range(len(session["cart"])):
            priceSum = priceSum + int(session["cart"][i].get("totalPrice"))
            
        return render_template("/cart.html", food=session["cart"], numberOfFood=len(session["cart"]), priceSum=priceSum)
    
    # Changing number of items in cart        
    else:
        plus = request.form.get("plus")
        minus = request.form.get("minus")
        id = request.form.get("id")
        
        if plus:
            for i in range(len(session["cart"])):
                if id == session["cart"][i].get("id"):
                    newNumber = int(session["cart"][i].get("number")) + 1
                    newTotalPrice = int(session["cart"][i].get("price")) * newNumber
                    session["cart"][i].update({"number": newNumber})
                    session["cart"][i].update({"totalPrice": newTotalPrice})
                
                priceSum = priceSum + int(session["cart"][i].get("totalPrice"))
            
            return render_template("/cart.html", food=session["cart"], numberOfFood=len(session["cart"]), priceSum=priceSum)
        
        elif minus:
            for i in range(len(session["cart"])):
                if id == session["cart"][i].get("id"):
                    newNumber = int(session["cart"][i].get("number")) - 1
                    # Update of number
                    if newNumber > 0:
                        newTotalPrice = int(session["cart"][i].get("price")) * newNumber
                        session["cart"][i].update({"number": newNumber})
                        session["cart"][i].update({"totalPrice": newTotalPrice})
                    # Deleting item if number = 0
                    elif newNumber == 0:
                        session["cart"].pop(i)
                        
            for j in range(len(session["cart"])):
                priceSum = priceSum + int(session["cart"][j].get("totalPrice"))
            
            return render_template("/cart.html", food=session["cart"], numberOfFood=len(session["cart"]), priceSum=priceSum)
            
# Order
@app.route("/adress", methods=["GET", "POST"])
def adress():
    if request.method == "GET":
        return render_template("/adress.html")
    else:
        # Getting adress from the form
        name = request.form.get("name")
        phone = request.form.get("phone")
        street = request.form.get("street")
        number = request.form.get("number")
        zipCode = request.form.get("zip")
        city = request.form.get("city")
        
        # Validatiing zip code
        if zipCode.isnumeric() == False:
            message = "Please enter valid ZIP code."
            return render_template("/adress.html", message=message)
            
        # Validatiing building number
        if int(number) < 0:
            message = "Please enter valid building number."
            return render_template("/adress.html", message=message)
            
        # Changing adress in session if it already exists
        if "adress" in session:
            session["adress"][0].update({"name": name,"phone": phone, "street": street, "number": number, "zipCode": zipCode, "city": city})
            return redirect("/summary")
        
        # Starting the session adress if it doesn't exist
        if "adress" not in session:
            session["adress"] = []
            
        # Adding adress to the session
        session["adress"].append({"name": name,"phone": phone, "street": street, "number": number, "zipCode": zipCode, "city": city})
        return redirect("/summary")
        
# Order summary
@app.route("/summary", methods=["GET", "POST"])
def summary():
    # Food summary
    food = session["cart"]
    PRICEDELIVERY = 5
        
    priceSum = 0
    for i in range(len(food)):
        priceSum = priceSum + int(food[i].get("totalPrice"))
        
    priceSumTotal = priceSum + PRICEDELIVERY
        
    # Adress summary
    adress = session["adress"][0]

    if request.method == "GET":
        return render_template("/summary.html", food=food, priceDelivery=PRICEDELIVERY, priceSumTotal=priceSumTotal, adress=adress)
    
    else:
        # Adding order to the orders table
        db.execute("INSERT INTO orders (name, phone, street, number, zipCode, city, timestamp) VALUES(?, ?, ?, ?, ?, ?, ?)", adress["name"], adress["phone"], adress["street"], adress["number"], adress["zipCode"], adress["city"], time.strftime('%D %H:%M:%S'))
        orderID = db.execute("SELECT id FROM orders ORDER BY timestamp DESC LIMIT 1")[0]["id"]
        print(orderID)

        # Adding food to the order in food&orders table
        for i in range(len(food)):
            db.execute("INSERT INTO foodANDorders (orderID, foodID, foodNumber) VALUES(?, ?, ?)", orderID, food[i]["id"], food[i]["number"])
        
        message = "ok"
        
        # Clearing session 
        session.clear()
        
        return render_template("/summary.html", message=message)
        
# Section "reservations"
@app.route("/reservations", methods=["GET", "POST"])
def reservations():
    if request.method == "GET":
        return render_template("/reservations.html")
    
    else:
        # Getting info from the form
        name = request.form.get("name")
        phone = request.form.get("phone")
        number = request.form.get("number")
        date = request.form.get("date")
        bookingTime = request.form.get("time")
        
        # Number of tables in restaurant
        TABLESNUMBER = 10
        
        # Checking if there are any free tables at chosen date and time
        bookedTables = db.execute("SELECT COUNT(id) FROM reservations WHERE date = ? AND time = ?", date, bookingTime)
        
        if TABLESNUMBER - bookedTables[0]["COUNT(id)"] > 0:
            db.execute("INSERT INTO reservations (name, phone, number, date, time, timestamp) VALUES(?, ?, ?, ?, ?, ?)", name, phone, number, date, bookingTime, time.strftime('%D %H:%M:%S'))
            messageOK = "Your reservation has been made correctly."
            return render_template("/reservations.html", messageOK=messageOK)
        
        else:
            messageWrong = "There are no free tables. Plese choose different date or time."
            return render_template("/reservations.html", messageWrong=messageWrong)

# Section "contact"
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("/contact.html")
        
    else:
        # Getting message from the form
        name = request.form.get("name")
        email = request.form.get("mail")
        contactMessage = request.form.get("contactMessage")
        
        # Validating submission:
        if not name or not email or not contactMessage:
            messageWrong = "Please fill in all of the fields."
            return render_template("/contact.html", messageWrong=messageWrong)
        
        if email.find("@") == -1:
            messageWrong = "Please use valid e-mail adress."
            return render_template("/contact.html", messageWrong=messageWrong)
        
        # Adding message to the database
        db.execute("INSERT INTO contactForm (name, mail, contactMessage, timestamp) VALUES(?, ?, ?, ?)", name, email, contactMessage, time.strftime('%D %H:%M:%S'))
        
        messageOK = "Your message has been sent."
        return render_template("/contact.html", messageOK=messageOK)
        