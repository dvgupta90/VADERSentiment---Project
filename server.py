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


url = "https://api.yelp.com/v3/businesses"


@app.route("/api_call", methods=['GET'])
def api_call():
    headers = {'Authorization': 'Bearer ' + yelp_api}
    payload= {"location": "94043", "term": "bars"}
    response = requests.get(url+"/search", headers=headers, params = payload)
    data = response.json()

    list1 = []
    for business in data['businesses']:
        list1.append(business['name'])
    
    
    return render_template("trial_api.html",data =list1)


@app.route("/api1", methods=['GET'])
def api1_call():
    headers = {'Authorization': 'Bearer ' + yelp_api}
    payload= {"location": "94043", "term": "bars"}
    response = requests.get(url+"/search", headers=headers, params = payload)
    data = response.json()
    
    # goal: collect reviews for each business
    # data = {bizI-d: [reviews], ...}
    # list of ids = []
    # loop through data json and pull out each busibness id
        # append to list of ids
    # create empty dictionary of biz_data called d
    # loop through each id in list of ids
        # make a request to yelp api for reviews based on business id
        # d[biz_id] = resp.json()['reviews']

    # for each key in the biz dictionary
        # run analysis of value (reviews)



    biz_dic = {}
   
    for business in data['businesses']:
        biz_id = business['id']
        d1 = requests.get(url+"/"+biz_id+"/reviews",
            headers=headers,
            params = {"locale":"en_US"})
        # biz_dic[biz_id] = d1.json()['reviews']
        biz_dic[biz_id] = [r['text'] for r in d1.json()['reviews']]

            
    # biz_dic = {}
   
    # for business in data['businesses']:
    #     biz_id = business['id']
    #     d1 = requests.get(url+"/"+biz_id+"/reviews",
    #         headers=headers,
    #         params = {"locale":"en_US"})
    #     data1 = d1.json()['reviews']
    #     for item in data1:
    #         biz_dic[biz_id] = item['text']
        

        
   
   

       


    
    return render_template("api1.html",data=biz_dic)    








@app.route('/')
def homepage():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")



@app.route('/process_registeration', methods=['POST'])
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
    session['user_id'] = new_user.user_id

    flash(f"User {first_name} added.")
    return redirect("/preferences")



@app.route('/preferences', methods=['GET'])
def preference_form():
    """Show options for user cuisine selection."""

    return render_template("preferences.html")



@app.route('/process_preferences', methods=['POST'])
def preference_form_process():
    """Process user preferences."""

    user_object = User.query.get(session['user_id'])

    # Get form variables
    user_pref1 = request.form["pref1"]
    user_pref2 = request.form["pref2"]

    user_object.pref.append(Preference(cuisine=user_pref1))
    user_object.pref.append(Preference(cuisine=user_pref2))      
    
    #don't need to db.add because the user already exists in DB, we are just modifying it.
    db.session.commit()

    flash(f"Your cuisine preferences have been saved.")
    return redirect("/search")

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""
    if 'user_id' in session:
        return redirect("/search")    

    return render_template("login_form.html")


@app.route('/process_login', methods=['POST'])
def login_process():
    """Process login."""

    # we are using POST here so that user's login ingo is not displayed in URL
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


@app.route('/search')
def search():
    """Search for a restaurant"""

    if 'user_id' in session:
        user = User.query.get(session["user_id"])
    if len(user.pref) == 0:
        flash("Please select your preferences.") 
        return redirect("/preferences")   

    return render_template("search.html")


@app.route('/profile')
def user_profile():
    """Show info about a logged in user"""

    if 'user_id' not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    return render_template("user_profile.html", user=user)    



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