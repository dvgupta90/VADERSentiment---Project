import unittest
from unittest import TestCase
from flask import Flask 
from server import app 
from model import db, connect_to_db, User, Preference, Restaurant_details, Favourite, Review
from example_data import users, reviews
from flask import session
import server

class Looged_out_Tests(unittest.TestCase): 
    #Tests that do not require user to be in session(logged in)

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        #Shows Flask errors that happen during tests
        app.config['TESTING'] = True

        #To test sessions we need to set Secret key 
        app.config['SECRET_KEY'] = 'key'


        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        users()
        reviews()


    def tearDown(self):
        db.session.close()
        db.drop_all()


    def test_homepage(self):
        result = self.client.get('/')
        self.assertIn(b'<h1>Reviews</h1>', result.data)


    def test_login(self):
        result = self.client.post('/process_login', 
                data={'email':'dg@gmail', 'password':'123'},
                follow_redirects=True)
        self.assertIn(b"Search",result.data)


    def test_invalid_login(self):
        result = self.client.post('/process_login',
                data={'email':'b@gmail.com', 'password': 'bob'},
                follow_redirects=True)
        self.assertNotIn(b"Search", result.data)
        self.assertIn(b"Reviews", result.data)     



class Logged_in_Tests(unittest.TestCase):
    #Tests that require user to be in session (logged in)

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        #To test sessions we need to set Secret key 
        app.config['SECRET_KEY'] = 'key'

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        users()
        reviews()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1


    def tearDown(self):
        """Do at end of every test."""
        db.session.close()
        db.drop_all()


    def test_logout(self):

        result = self.client.get('/logout',
                follow_redirects=True)
        self.assertIn(b'<h1>Reviews</h1>', result.data)
        self.assertNotIn(b"Search",result.data)


    def test_user_profile_page(self):
        """Test this page can only be reached if user is in session"""
        result = self.client.get("/profile", follow_redirects=True)
        self.assertIn(b"User ID", result.data)


    def test_search_page(self):
        """Test this page can only be reached if user is in session"""
        result = self.client.get("/search")
        self.assertIn(b"Search", result.data) 


    def test_add_to_fav_(self):
        """Test user's if favourite restaurant is added to DB"""
        result = self.client.post("/add_to_fav", data={"yelp_biz_id":"JA_V9TqDCrkgknqrcUndIQ", 
                "yelp_rest_name":"Siam", "yelp_rating":"4", 
                "yelp_category":"Thai", "yelp_price":"$$", 
                "yelp_image_url":"https://s3-media2.fl.yelpcdn.com/bphoto/1SkZwZrRZkQSzRMn_Trs3w/o.jpg" })

        DB_result = Restaurant_details.query.filter_by(biz_id = "JA_V9TqDCrkgknqrcUndIQ").first()
        self.assertIsNotNone(DB_result) #testing that the returned result is not NONE
        self.assertEqual(DB_result.restaurant_name, 'Siam') #testing restaurant name is what it should be
        
        self.assertIn(b"Your Favourite has been saved", result.data)



    def test_check_your_review_page(self):
        result = self.client.post('/process_check_your_review', 
                data={'review': 'food was good service was bad'})
        self.assertIn(b"neu",result.data)
             



class Mock_FlaskTests(unittest.TestCase):
    #Tests that require API and user to be in session (logged in)

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        users()
        reviews()


        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()  

    # Make mock
    def _mock_get_businesses_by_zip(zipcode,cuisine, offset=0):
        return {'businesses': [{'id': 'bmxi_Ts834MeAXa9_ysiVg', 'alias': 'dosa-paratha-mountain-view', 'name': 'Dosa Paratha', 'image_url': 'https://s3-media3.fl.yelpcdn.com/bphoto/p_hgt9AHWK3eoijaJnsftA/o.jpg', 'is_closed': False, 'url': 'https://www.yelp.com/biz/dosa-paratha-mountain-view?adjust_creative=YoZC3qnFQ5LTFgd4yEStVA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=YoZC3qnFQ5LTFgd4yEStVA', 'review_count': 50, 'categories': [{'alias': 'vegetarian', 'title': 'Vegetarian'}, {'alias': 'indpak', 'title': 'Indian'}], 'rating': 4.5, 'coordinates': {'latitude': 37.4141097896949, 'longitude': -122.093300409615}, 'transactions': [], 'location': {'address1': '2105 Old Middlefield Way', 'address2': '', 'address3': None, 'city': 'Mountain View', 'zip_code': '94043', 'country': 'US', 'state': 'CA', 'display_address': ['2105 Old Middlefield Way', 'Mountain View, CA 94043']}, 'phone': '+16509651888', 'display_phone': '(650) 965-1888', 'distance': 2246.059804935543},
                                 {'id': '3b0yY-kCOG-1Eq9oamlSzw', 'alias': 'zareens-palo-alto', 'name': "Zareen's", 'image_url': 'https://s3-media3.fl.yelpcdn.com/bphoto/o5_yGi3Qpk89hEQw1g-22Q/o.jpg', 'is_closed': False, 'url': 'https://www.yelp.com/biz/zareens-palo-alto?adjust_creative=YoZC3qnFQ5LTFgd4yEStVA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=YoZC3qnFQ5LTFgd4yEStVA', 'review_count': 648, 'categories': [{'alias': 'indpak', 'title': 'Indian'}, {'alias': 'halal', 'title': 'Halal'}, {'alias': 'pakistani', 'title': 'Pakistani'}], 'rating': 4.5, 'coordinates': {'latitude': 37.42675, 'longitude': -122.14404}, 'transactions': [], 'price': '$$', 'location': {'address1': '365 S California Ave', 'address2': None, 'address3': '', 'city': 'Palo Alto', 'zip_code': '94306', 'country': 'US', 'state': 'CA', 'display_address': ['365 S California Ave', 'Palo Alto, CA 94306']}, 'phone': '+16506008438', 'display_phone': '(650) 600-8438', 'distance': 2820.165733861648}]}

    server.get_businesses_by_zip = _mock_get_businesses_by_zip


    def test_process_searchbox_with_mock(self):
        """Find restaurant name by zipcode."""

        result = self.client.get('/process_searchbox', data={'zipcode': '94043', 'cuisine': 'indian'})
        self.assertIn(b"Dosa Paratha", result.data)
          





if __name__ == "__main__":
   unittest.main()



