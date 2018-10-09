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
    divya = User(fname = "divya", lname = "gupta", email = "dg@gmail", password = "123"), \
    jen = User(fname = "jen", lname = "low", email = "jl@gmail", password = "123"), \
    deb = User(fname = "deb", lname = "moore", email = "dm@gmail", password = "123")
    Preference((divya.user_p).user_id, cusine1 = "indian", cusine2 = "agh"), \
    Preference((jen.user_p).user_id, cusine1 = "gfh", cusine2 = "chg"), \
    Preference((deb.user_p).user_id, cusine1 = "fvh", cusine2 = "rdr"),\
    Restaurant_details((divya.user_r).user_id, sentiment_score = 2, category = "fb", price = "$", date_of_score = ),\
    Restaurant_details((jen.user_r).user_id, sentiment_score = 2, category = "fbd", price = "$", date_of_score = ),\
    Restaurant_details((deb.user_r).user_id, sentiment_score = 2, category = "fv", price = "$", date_of_score = ),\
    Favourite((divya.user_f).user_id, restaurant_id = (divya.rest_f).restaurant_id),\
    Favourite((jen.user_f).user_id, restaurant_id = (jen.rest_f).restaurant_id),\
    Favourite((deb.user_f).user_id, restaurant_id = (deb.rest_f).restaurant_id) 

    list1 = [divya,jen,deb]    



    # We need to add to the session
    db.session.add(list1)

    db.session.commit()

# def preferences():
#     """Insert sample user preferences into DB """


#     # Delete all rows in table, so if we need to run this a second time,
#     # we won't be trying to add duplicate users
#     Preference.query.delete()

#     #inserting records
#     pref = [Preference(user_id = ??, cusine1 = "indian", cusine2 = "agh"), \
#         Preference(user_id = ??, cusine1 = "gfh", cusine2 = "chg"), \
#         Preference(user_id = ??, cusine1 = "fvh", cusine2 = "rdr")

#     # We need to add to the session
#     db.session.add(pref)

#     db.session.commit()


# def rest_details():
#     """Insert sample restaurant details into DB """


#     # Delete all rows in table, so if we need to run this a second time,
#     # we won't be trying to add duplicate users
#     Restaurant_details.query.delete()

#     #inserting records
#     details = [Restaurant_details(user_id = ??, sentiment_score = 2, category = "fb", price = "$", date_of_score = ), \
#         Restaurant_details(user_id = ??, sentiment_score = 2, category = "fbd", price = "$", date_of_score = ), \
#         Restaurant_details(user_id = ??, sentiment_score = 2, category = "fv", price = "$", date_of_score = )

#     # We need to add to the session
#     db.session.add(details)

#     db.session.commit()


# def favs():
#     """Insert sample user favs into DB """


#     # Delete all rows in table, so if we need to run this a second time,
#     # we won't be trying to add duplicate users
#     Favourite.query.delete()

#     #inserting records
#     fav = [Favourite(user_id = ??, restaurant_id =  ), \
#         Favourite(user_id = ??, restaurant_id =  ), \
#         Favourite(user_id = ??, restaurant_id =  )

#     # We need to add to the session
#     db.session.add(fav)

#     db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    users()
    preferences()
    rest_details()
    favs()
        