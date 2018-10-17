import requests
from flask import Flask, redirect, request, render_template, session,flash
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Preference, Restaurant_details, Favourite, Review
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk import punkt


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"



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
    payload= {"location": "94043", "term": "Restaurants - Indian"}
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
    

    id_list = []
    for business in data['businesses']:
        id_list.append(business['id'])

    name_list = []
    for business in data['businesses']:
        name_list.append(business['name'])

    image_list = []
    for business in data['businesses']:
        image_list.append(business['image_url'])
    
    length= len(image_list) 

    categories_list = []
    for business in data['businesses']:
        categories_list.append(((business['categories'])[0])['title'])

    price_list = []
    for business in data['businesses']:
        price_list.append(business['price'])    
                

    # for business in data['businesses']:
    #     print(((business['categories'])[0])['title'])



    ############# ADDING TO FAVS ###########################################

        
        
    


    return render_template("trial_search_api_udi.html", name=name_list, image = image_list, 
        biz_id = id_list, length=length,
        categories=categories_list, price=price_list,
        offset = offset, zipcode=zipcode, cuisine=cuisine)





@app.route('/profile')
def user_profile():
    """Show info about a logged in user"""

    if 'user_id' not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    return render_template("user_profile.html", user=user)    




@app.route('/process_searchbox/<biz_id>')   
def reviews(biz_id):
    """Sentiment score for restaurant""" 


    
    review = db.session.query(Review.review).filter(Review.biz_id == biz_id).all()


    final_list_d = []
    for tup in review:
        final_list_d.append(tup[0])
    
    analyser = SentimentIntensityAnalyzer()

    analyzed_reviews = []
    for sentence in final_list_d:
       
        snt = analyser.polarity_scores(sentence)
       
        analyzed_reviews.append(sentence + str(snt))

      
  

    return render_template("reviews.html", data = analyzed_reviews)



@app.route("/add_to_fav")
def add_to_fav():
    """User can add a restaurant to their fav"""

    ###get data from javascript like you would do for a POST form. request.form
    ## and save that data in variables and push it to DB or push directly to DB 

    business = Restaurant_details.query.filter_by(biz_id = buss_id).first() 

        if business == None:
            business = Restaurant_details(biz_id = business['id'], 
                restaurant_name = business['name'], 
                category = ((business['categories'])[0])['title'], 
                price = business['price'], 
                image = business['image_url'])


            db.session.add(businesses)

            db.session.commit()

        user_object = User.query.get(session['user_id'])
        user_object.fav.append(Favourite(rest = business))
        db.session.commit()


        return jsonify(Message:str("Your Favourite has been saved."))





@app.route("/every_rest_score")
def each_restaurant_page():
    """shows each restaurant score and reviews"""   


    return render_template("every_rest_score.html")


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