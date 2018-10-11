from model import User
from model import Preference
from model import Restaurant_details
from model import Favourite

from model import connect_to_db, db
from server import app
import datetime


def users():
    """Insert sample users into DB """

    print("users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    #inserting records
    divya = User(fname = "divya", lname = "gupta", email = "dg@gmail", password = "123")
    jen = User(fname = "jen", lname = "low", email = "jl@gmail", password = "123")
    deb = User(fname = "deb", lname = "moore", email = "dm@gmail", password = "123")
    
    divya.pref.append(Preference(cuisine="indian"))
    divya.pref.append(Preference(cuisine="thai"))
    jen.pref.append(Preference(cuisine = "thai"))
    jen.pref.append(Preference(cuisine = "chinese"))
    deb.pref.append(Preference(cuisine = "thai"))
    deb.pref.append(Preference(cuisine = "indian"))
    rest1 = Restaurant_details(restaurant_name = "taj1", category = "fb", price = "$")
    rest2 = Restaurant_details(restaurant_name = "taj2", category = "fbfv", price = "$$")
    rest3 = Restaurant_details(restaurant_name = "taj3", category = "fbnhm", price = "$")
    divya.fav.append(Favourite(rest = rest1))
    jen.fav.append(Favourite(rest = rest3))
    deb.fav.append(Favourite(rest = rest1))
    
    list1 = [divya,jen,deb,rest1,rest2,rest3]    

    # We need to add to the session
    db.session.add_all(list1)

    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    users()

        