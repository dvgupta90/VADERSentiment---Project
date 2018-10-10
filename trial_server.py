import requests
# from flask import Flask, redirect, request, render_template, session
# from flask_debugtoolbar import DebugToolbarExtension
# from jinja2 import StrictUndefined


# app = Flask(__name__)
# app.jinja_env.undefined = StrictUndefined
# app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar



# @app.route("/api_call", methods=['GET'])
# def api_call():
    
#   return data


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.debug = True
    # # make sure templates, etc. are not cached in debug mode
    # app.jinja_env.auto_reload = app.debug

    #connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    # app.run(port=5000, host='0.0.0.0')
    secret_key = "ABC"



    yelp_api = "EQL25pZkO4IPDpkORcacFNfBaSzfjYYK-pxP_YgFnoFIa7xavAazVxu0ghPDRqKn0Kc3HCo8x0TocDpejtHRh1bLh1SjXR7zvlG46b2RKoAUyufeZxA6b7PUMDy8W3Yx"



    url = "https://api.yelp.com/v3/businesses/search?location=Boston&term=food"

    # payload = {name: taj-campton-san-francisco}
    headers = {'Authorization': 'Bearer %s' % yelp_api}
    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)