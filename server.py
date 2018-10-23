import requests
from flask import Flask, redirect, request, render_template, session,flash,jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Preference, Restaurant_details, Favourite, Review
import os
from pprint import pprint
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk import punkt
import hashlib




app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['SECRET_KEY']



yelp_api = os.environ['YELP_API_KEY']



url = "https://api.yelp.com/v3/businesses"


# @app.route("/api_call", methods=['GET'])
# def api_call():
#     headers = {'Authorization': 'Bearer ' + yelp_api}
#     payload= {"location": "94043", "term": "Restaurants - Indian"}
#     response = requests.get(url+"/search", headers=headers, params = payload)
#     data = response.json()

#     list1 = []
#     for business in data['businesses']:
#         list1.append(business['name'])
    
    
#     return render_template("trial_api.html",data =list1)

@app.route("/trial_api_call", methods=['GET'])
def trial_api_call():
    headers = {'Authorization': 'Bearer ' + yelp_api}
    payload= {"location": "94043", "term": "Restaurants - thai"}
    response = requests.get(url+"/search", headers=headers, params = payload)
    data = response.json()

    
    
    return render_template("trial_api_review.html",data =data)


@app.route("/api1", methods=['GET'])
def api1_call():
    headers = {'Authorization': 'Bearer ' + yelp_api}
    payload= {"location": "94043", "term": "bars"}
    response = requests.get(url+"/search", headers=headers, params = payload)
    data = response.json()
    
   



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
    password = password.encode()
    #####hashing#########
    hash_pwd = hashlib.sha256(password)
    hash_pwd = hash_pwd.hexdigest()
    print()
    print()
    print()
    print()
    print(hash_pwd)
   

    new_user = User(fname=first_name, lname=last_name, 
        email=email, password=hash_pwd)

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
    # password = password.encode()
    # user_hash_pwd = hashlib.sha256(password)
    # user_hash_pwd = user_hash_pwd.hexdigest()

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
    # if user.password != user_hash_pwd:
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


@app.route('/process_searchbox', methods = ["GET"])
def processing_search():
    """User submits criteria to be searched"""
 
    

    zipcode = request.args.get("zipcode")
    cuisine = request.args.get("cuisine")
    offset = int(request.args.get("offset", 0)) #this is not coming from form , 
        #this gets loaded in the function when NEXT button is clicked. 
        # when the button is clicked the page gets re-rendered and with that 
        # this function gets re-called and then those parameters are inserted into html/jinja


    headers = {'Authorization': 'Bearer ' + yelp_api}
    payload= {"location": str(zipcode), "term": str(cuisine), "limit": int(10), "offset": offset}
    response = requests.get(url+"/search", headers=headers, params = payload)
    data = response.json()



    business = data['businesses'] #this returns a list of dictionaries.     

    for buss in business:
        if 'price' not in buss.keys():
            buss['price'] = "$$"

    for buss in business:
        pprint ((buss['coordinates'])['latitude'])       



    return render_template("trial_search_api_udi.html", businesses= business,
        offset = offset,zipcode=zipcode, cuisine=cuisine)




@app.route('/profile')
def user_profile():
    """Show info about a logged in user"""

    if 'user_id' not in session:
        return redirect("/login")

    #in this one query--> we are doing a double joined load,
    #by (accessing relationship deeper than one level)..
    #meaning trying to get from one table to another to another
    #also we are getting user object from User table by using .get
    user = User.query.options(db.joinedload('fav').joinedload('rest')).get(session["user_id"])


    return render_template("user_profile.html", user=user)    




@app.route('/process_searchbox/<biz_id>')   
def reviews(biz_id):
    """Sentiment score for restaurant""" 


    googlemaps_api = os.environ['GOOGLE_API_KEY']

    # we stored lat and lng as parameters/ form way dictionary values 
    # in the HREF of restaurant name in html that loops over each restaurant div
    # we are extracting that information here and passing to reviews.html in jinja 
    # and then passing that info to JS through data attributes
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')

    review = db.session.query(Review.review).filter(Review.biz_id == biz_id).all()
    
    final_list_d = []
    for tup in review:
        final_list_d.append(tup[0])
    
    analyser = SentimentIntensityAnalyzer()

    analyzed_reviews = []
    for sentence in final_list_d:
       
        snt = analyser.polarity_scores(sentence)
       
        analyzed_reviews.append(sentence + str(snt))

      
  

    return render_template("reviews.html", data = analyzed_reviews, 
        api_key=googlemaps_api, latitude=latitude, longitude=longitude)



@app.route("/add_to_fav", methods=["POST"])
def add_to_fav():
    """User can add a restaurant to their fav"""

    ###get data from javascript like you would do for a POST form. request.form
    ## and save that data in variables and push it to DB or push directly to DB 
    user_object = User.query.get(session['user_id'])

    # Get form variables in javascript file
    rest_biz_id = request.form["yelp_biz_id"]
    rest_name = request.form["yelp_rest_name"]
    rest_rating = request.form["yelp_rating"]
    rest_category = request.form["yelp_category"]
    rest_price = request.form["yelp_price"]
    rest_image = request.form["yelp_image_url"]


    restaurant = Restaurant_details.query.filter_by(biz_id = rest_biz_id).first() 

    if restaurant is None:
        restaurant = Restaurant_details(biz_id = rest_biz_id, 
            restaurant_name = rest_name,
            rating = int(float(rest_rating)), 
            category = rest_category, 
            price = rest_price, 
            image = rest_image)


        db.session.add(restaurant)

        db.session.commit()

    
    #checking if the user already has saved a restaurant as a fav
    #checking if the restaurant saved and user who saved the restaurant are not repeated
    #making sure that another user is able to add the same restaurant in thier fav but,
    #does not add that restaurant again to the Restaurant tables in DB
    fav = Favourite.query.filter(Favourite.restaurant_id == restaurant.restaurant_id, 
        Favourite.user_id== user_object.user_id).all()
    if not fav:
        user_object.fav.append(Favourite(rest = restaurant))
        db.session.commit()

    show_status = {'message':'Your Favourite has been saved'}
    return jsonify(show_status)





@app.route("/every_rest_score")
def each_restaurant_page():
    """shows each restaurant score and reviews"""   


    return render_template("every_rest_score.html")




@app.route("/check_your_review")
def check_review_sentiment():
    """user can type text and see the sentiment score on it"""  


    return render_template("check_your_review.html")  


@app.route("/process_check_your_review", methods=["GET"])
def process_check_review_sentiment():
    """user can type text and see the sentiment score on it"""  

    sentence = request.args.get("review")
    print(sentence)

    analyser = SentimentIntensityAnalyzer()

       
    snt = analyser.polarity_scores(sentence) 
    print(snt)
    show_score= {'score':snt}  

    return jsonify(show_score) 


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