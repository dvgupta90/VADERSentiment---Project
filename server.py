import requests
from flask import Flask, redirect, request, render_template, session,flash
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Preference, Restaurant_details, Favourite
import os

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"



yelp_api = os.environ['YELP_API_KEY']


url = "https://api.yelp.com/v3/businesses/search"


@app.route("/api_call", methods=['GET'])
def api_call():
    headers = {'Authorization': 'Bearer ' + yelp_api}
    payload= {"location": "Boston", "term": "food"}
    response = requests.get(url, headers=headers, params = payload)
    data = response.json()
    
    print(data)
    return render_template("trial_api.html",data =data)








@app.route('/')
def homepage():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")



@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    first_name = request.form["firstname"]
    last_name = request.form["lastname"]
    email = request.form["email"]
    password = request.form["password"]
   

    new_user = User(fname=first_name, lname=last_name, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {first_name} added.")
    return redirect("/")



@app.route('/preferences', methods=['GET'])
def preference_form():
    """Show form for user signup."""

    return render_template("preferences.html")



@app.route('/preferences', methods=['POST'])
def preference_form_process():
    """Process user preferences."""

    # Get form variables
    first_name = request.form["firstname"]
    last_name = request.form["lastname"]
    email = request.form["email"]
    password = request.form["password"]
   

    new_user = User(fname=first_name, lname=last_name, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {first_name} added.")
    return redirect("/")

app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/search")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")    




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')