import unittest
from unittest import TestCase
from flask import Flask 
from server import app 
from model import db, connect_to_db 
from example_data import users, reviews
from flask import session

class FlaskTest(unittest.TestCase):
    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        #Shows Flask errors that happen during tests
        app.config['TESTING'] = True

        #To test sessions we need to set Secret key 
        app.config['SECRET_KEY'] = 'key'

        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_homepage(self):
        result = self.client.get('/')
        self.assertIn(b'<h1>Reviews</h1>', result.data)

class TestDatabase(unittest.TestCase):

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
        self.assertIn(b"Login", result.data)    


    def logout(self):
        result = self.client.get('/logout',
                follow_redirects=True)
        self.assertIn(b'<h1>Reviews</h1>', result.data)
        self.assertNotIn(b"Search",result.data)


    def test_user_profile_page(self):
        """Test this page can only be reached if user is in session"""

        result = self.client.get("/profile", follow_redirects=True)
        self.assertIn(b"User ID", result.data)








    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()



if __name__ == "__main__":
   unittest.main()



