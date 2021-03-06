import requests
from flask import Flask, redirect, request, render_template, session,flash,jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Preference, Restaurant_details, Favourite, Review
import os
from pprint import pprint
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk import punkt
from nltk.tokenize import sent_tokenize, word_tokenize 
import hashlib
import csv
import json



################################################################################
app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['SECRET_KEY']


####### Setting up for YELP API call ########################################### 
yelp_api = os.environ['YELP_API_KEY']
url = "https://api.yelp.com/v3/businesses"





################################################################################
#   Homepage, Registration and Adding User Preferences routes                  #
#                                                                              #
################################################################################

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


################################################################################
#   Login and Logout routes                                                    #
#                                                                              #
################################################################################

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""
    if 'user_id' in session:
        return redirect("/search")    

    return render_template("login_form.html")



@app.route('/process_login', methods=['POST'])
def login_process():
    """Process login."""

    # we are using POST here so that user's login info is not displayed in URL
    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    password = password.encode()
    user_hash_pwd = hashlib.sha256(password)
    user_hash_pwd = user_hash_pwd.hexdigest()

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/") # the user can register or enter the correct email

    if user.password != user_hash_pwd:
        flash("Incorrect password") # the user can register or enter the correct pwd
        return redirect("/")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/search")



@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")    


################################################################################
# Search page and Reviews page routes (includes YELP and GOOGLE MAPS API CALL) #
#                                                                              #
################################################################################

@app.route('/search')
def search():
    """Search for a restaurant"""

    if 'user_id' not in session:
        flash ("Please Log In to continue")
        return redirect("/login")

    if 'user_id' in session:
        user = User.query.get(session["user_id"])

    if len(user.pref) == 0:
        flash("Please select your preferences.") 
        return redirect("/preferences")   

    return render_template("search.html")



# defining Helper function that queries YELP API
#we just seperated this function from /process_searchbox route
def get_businesses_by_zip(zipcode, cuisine, offset=0):
    """Helper function that queries Yelp API"""
    headers = {'Authorization': 'Bearer ' + yelp_api}
    payload= {"location": str(zipcode), "term": str(cuisine), "limit": int(10), "offset": offset}
    response = requests.get(url+"/search", headers=headers, params = payload)
    return response.json()


@app.route('/process_searchbox', methods = ["GET"])
def processing_search():
    """User submits criteria to be searched"""
 
    if 'user_id' not in session:
        flash ("Please Log In to continue")
        return redirect("/login")

    zipcode = request.args.get("zipcode")
    cuisine = request.args.get("cuisine")
    offset = int(request.args.get("offset", 0)) #this is not coming from form , 
        #this gets loaded in the function when NEXT button is clicked. 
        # when the button is clicked the page gets re-rendered and with that 
        # this function gets re-called and then those parameters are inserted into html/jinja

    data = get_businesses_by_zip(zipcode, cuisine, offset) #calling this function
    #from above.. giving it parameters from this function

    business = data['businesses'] #this returns a list of dictionaries.     

    for buss in business:
        if 'price' not in buss.keys():
            buss['price'] = "$$"
       
    return render_template("trial_search_api_udi.html", businesses= business,
        offset = offset,zipcode=zipcode, cuisine=cuisine)

    


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
    restaurant_name = request.args.get('name')

    review = db.session.query(Review.review).filter(Review.biz_id == biz_id).all()
    
    final_list_d = []
    for tup in review:
        final_list_d.append(tup[0])

    
    analyser = SentimentIntensityAnalyzer()

    sum_compound_score = 0
    analyzed_reviews = []
    pos_word_list=set()
    neu_word_list=set()
    neg_word_list=set()

    
    word_cloud_dict = {}

    for sentence in final_list_d:
       
        snt = analyser.polarity_scores(sentence)
        sum_compound_score += snt['compound']

        tokenized_sent = word_tokenize(sentence)
        for word in tokenized_sent:
            word = word.lower()
            word_compound_score = (analyser.polarity_scores(word))['compound']

            if (word_compound_score) > 0:
                pos_word_list.add(word)
                # word_cloud_dict[word] = (word_compound_score*1000)

            elif (word_compound_score) < 0:
                neg_word_list.add(word)
                # word_cloud_dict[word] = (word_compound_score*1000)

            else:
                neu_word_list.add(word)
                # word_cloud_dict[word] = (word_compound_score*1000)
       
        analyzed_reviews.append(sentence + str(snt))


    for word in pos_word_list:
        pos_score = analyser.polarity_scores(word)
        word_cloud_dict[word] = (pos_score['compound']*1000)
    
        # print(word,pos_score)

    for word in neg_word_list:
        neg_score = analyser.polarity_scores(word)
        word_cloud_dict[word] = (neg_score['compound']*1000)
    
        # print(word,neg_score)    
    
    # print(word_cloud_dict)


    avg_compound_score = sum_compound_score/len(analyzed_reviews)
    avg_compound_score = ("%.3f" % avg_compound_score) 



    return render_template("reviews.html", restaurant_name=restaurant_name, 
        biz_id=biz_id, avg_score_for_restaurant= avg_compound_score,
        data = analyzed_reviews, api_key=googlemaps_api, 
        latitude=latitude, longitude=longitude)

################################################################################




################################################################################
#   Creating Word Cloud route                                                  #
#                                                                              #
################################################################################


## creating route to feed review words csv data as json
@app.route('/process_word_cloud/<biz_id>.json')
def word_cloud_json(biz_id):
    """Creates Word Cloud for each restaurant"""

    
    review = db.session.query(Review.review).filter(Review.biz_id == biz_id).all()
    
    final_list_d = []
    for tup in review:
        final_list_d.append(tup[0])
    
    analyser = SentimentIntensityAnalyzer()
   
    pos_word_list=set()
    neu_word_list=set()
    neg_word_list=set()
 
    word_cloud_dict = {}

    for sentence in final_list_d:

        tokenized_sent = word_tokenize(sentence)
        for word in tokenized_sent:
            word = word.lower()
            word_compound_score = (analyser.polarity_scores(word))['compound']

            if (word_compound_score) > 0:
                pos_word_list.add(word)
                # word_cloud_dict[word] = (word_compound_score*1000)

            elif (word_compound_score) < 0:
                neg_word_list.add(word)
                # word_cloud_dict[word] = (word_compound_score*1000)

            else:
                neu_word_list.add(word)
                # word_cloud_dict[word] = (word_compound_score*1000)
 


    for word in pos_word_list:
        pos_score = analyser.polarity_scores(word)
        word_cloud_dict[word] = (pos_score['compound']*1000)

    for word in neg_word_list:
        neg_score = analyser.polarity_scores(word)
        word_cloud_dict[word] = (neg_score['compound']*1000)
    

    data =[]
    for key, value in word_cloud_dict.items():
       data.append({"word": key, "score": value})

     
    return jsonify(data)      




################################################################################
#   User Profile, About SAFIYA, Add/Remove Favourites routes                                  #
#                                                                              #
################################################################################

@app.route('/about')
def about_page():
    """Show info about website SAFIYA"""

    return render_template("about_page.html")



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




###############################################################################

@app.route("/remove_from_fav", methods=["POST"])
def remove_from_fav():
    """User can remove a restaurant from their fav"""
    
    user_object = User.query.get(session['user_id'])
    

    rest_id = request.form["database_rest_id"] ## restaurant id in favourites table
    

    restaurant = Restaurant_details.query.filter_by(restaurant_id = rest_id).first()
    

    remove_fav = Favourite.query.filter(Favourite.restaurant_id == restaurant.restaurant_id, 
        Favourite.user_id== user_object.user_id).all()
    
    

    if remove_fav is not None:
        fav_object = Favourite.query.filter_by(fav_id = remove_fav[0].fav_id).all()
        # remove_fav is a list. List of objects. so we need to access 
        # the object in it using index. same goes for fav_object.
        
        db.session.delete(fav_object[0])
        db.session.commit()


    show_status = {'message':'Your Favourite has been removed'}
    return jsonify(show_status)










################################################################################
#   Check score on your review route (interactive mode)                        #
#                                                                              #
################################################################################

@app.route("/check_your_review")
def check_review_sentiment():
    """User can type text and see the sentiment score on it"""  

    if 'user_id' not in session:
        flash ("Please Log In to continue")
        return redirect("/login")
    
    return render_template("check_your_review.html")  


@app.route("/process_check_your_review", methods=["POST"])
def process_check_review_sentiment():
    """Process check your review"""  

    sentence = request.form.get("review")
    print(sentence)

    analyser = SentimentIntensityAnalyzer()
    
    snt = analyser.polarity_scores(sentence) 
    print(snt)
    show_score= {'score':snt}  

    return jsonify(show_score) 






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')