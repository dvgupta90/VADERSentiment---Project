from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()



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


    

class Preference(db.Model):
    """User preferences"""

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Preference preference_id={} user_id={} cuisine={}".format(self.preference_id, self.user_id, self.cuisine))


    __tablename__ = "preferences"

    preference_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable= False)
    cuisine = db.Column(db.String(100), nullable=False)

    user = db.relationship("User")
    

class Restaurant_details(db.Model):
    """Save restaurant info """

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Restaurant_details restaurant_id={} restaurant_name={} category={} price={}".format(self.preference_id, self.user_id, self.restaurant_name, self.category, self.price))


    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    biz_id = db.Column(db.String(100), nullable=False)
    restaurant_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String(6))
    image = db.Column(db.String(1000))
    url = db.Column(db.String(1000))
    



    
class Favourite(db.Model):
    """Save user's favourite restaurants"""

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Favourite fav_id={} user_id={} restaurant_id".format(self.fav_id, self.user_id, self.restaurant_id))


    __tablename__ = "favourites"

    fav_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable= False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable= False)

    user = db.relationship("User")
    rest = db.relationship("Restaurant_details")



class Review(db.Model):
    """Data of reviews"""

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Review table_id={} biz_id={} review={}>".format(self.table_id, self.biz_id, self.review))


    __tablename__ = "reviews"

    table_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    biz_id = db.Column(db.String(100), nullable=False)
    review = db.Column(db.String(10000), nullable=False) 
  


       


def connect_to_db(app, db_uri='postgresql:///reviews'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # us in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")