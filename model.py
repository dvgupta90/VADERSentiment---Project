from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

##############################################################################
# Model definitions

class User(db.Model):
    """User of reviews website"""

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<User user_id={} fname={} lname={} email={}>".format(self.user_id, self.fname, self.lname, self.email))


    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique = True)
    password = db.Column(db.String(100), nullable=False)

    pref = db.relationship("Preference")
    fav = db.relationship("Favourite")
    rest = db.relationship("Restaurant_details")


    

class Preference(db.Model):
    """User preferences"""

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Preference preference_id={} user_id={} cusine1={} cusine2={}".format(self.preference_id, self.user_id, self.cusine1, self.cusine2))


    __tablename__ = "preferences"

    preference_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable= False)
    cusine1 = db.Column(db.String(100), nullable=False)
    cusine2 = db.Column(db.String(100), nullable=False)

    user_p = db.relationship("User")
    

class Restaurant_details(db.Model):
    """Save restaurant info from API calls to use as cache"""

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Restaurant_details restaurant_id={} user_id={} sentiment_score={} category={} price={}".format(self.preference_id, self.user_id, self.sentiment_score, self.category, self.price))


    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable= False)
    sentiment_score = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(6))
    date_of_score = db.Column(db.DateTime)

    user_r = db.relationship("User")


    
class Favourite(db.Model):
    """Save user's favourite restaurants"""

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Favourite fav_id={} user_id={} restaurant_id".format(self.fav_id, self.user_id, self.restaurant_id))


    __tablename__ = "favourites"

    fav_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable= False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable= False)

    user_f = db.relationship("User")
    rest_f = db.relationship("Restaurant_details")
  


       




def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///reviews'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    #from server import app
    connect_to_db(app)
    print("Connected to DB.")