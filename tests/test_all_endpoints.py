import unittest
import json
import os
from app import app, db, User, ServiceCategory, Service, Review, Message, bcrypt # Import all necessary components

class AllEndpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configure app for testing: use an in-memory SQLite database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for testing forms if you add them later
        app.config['DEBUG'] = False # Disable debug mode for tests

        with app.app_context():
            db.create_all() # Create tables for the in-memory database

        cls.client = app.test_client() # Create a test client for making requests (class-level)

    @classmethod
    def tearDownClass(cls):
        # Clean up after all tests are done
        with app.app_context():
            db.session.remove()
            db.drop_all() # Drop all tables from the in-memory database

    def setUp(self):
        # Assign the class-level client to the instance-level client for each test
        self.client = self.__class__.client

        with app.app_context():
            # Delete data from tables in reverse order of dependency
            db.session.execute(db.delete(Message))
            db.session.execute(db.delete(Review))
            db.session.execute(db.delete(Service))
            db.session.execute(db.delete(ServiceCategory))
            db.session.execute(db.delete(User))
            db.session.commit()

        # Pre-create common users and categories for tests that need them
        # User 1: Seeker
        seeker_user_data = {
            "username": "testseeker", "email": "seeker@example.com",
            "password": "securepassword", "user_type": "seeker", "location": "Kigali", "contact_info": "0781234567"
        }
        seeker_response = self.client.post('/users', json=seeker_user_data)
        self.seeker_id = seeker_response.json['user_id']
        self.seeker_username = seeker_user_data['username']

        # User 2: Provider
        provider_user_data = {
            "username": "testprovider", "email": "provider@example.com",
            "password": "securepassword", "user_type": "provider", "location": "Kigali", "contact_info": "0787654321", "bio": "Experienced plumber."
        }
        provider_response = self.client.post('/users', json=provider_user_data)
        self.provider_id = provider_response.json['user_id']
        self.provider_username = provider_user_data['username']

        # Service Category
        category_data = {"name": "Plumbing"}
        category_response = self.client.post('/categories', json=category_data)
        self.category_id = category_response.json['category_id']
        self.category_name = category_data['name']

    def test_101_create_seeker_user_success(self):
        """Test creating a new seeker user successfully."""
        user_data = {
            "username": "newseeker", "email": "newseeker@example.com",
            "password": "newpassword", "user_type": "seeker", "location": "Kigali", "contact_info": "0781112223"
        }
        response = self.client.post('/users', json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("User created successfully!", response.json['message'])
        self.assertIn("user_id", response.json)
        with app.app_context():
            self.assertIsNotNone(User.query.filter_by(username='newseeker').first())

    def test_102_create_user_existing_username(self):
        """Test creating a user with an already existing username."""
        response = self.client.post('/users', json={
            "username": self.seeker_username, "email": "another@example.com",
            "password": "pass", "user_type": "seeker"
        })
        self.assertEqual(response.status_code, 409)
        self.assertIn("Username already exists", response.json['message'])

    def test_103_login_user_success(self):
        """Test successful user login."""
        response = self.client.post('/login', json={
            "username": self.seeker_username, "password": "securepassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login successful!", response.json['message'])
        self.assertEqual(response.json['user_type'], 'seeker')

    def test_104_login_user_incorrect_password(self):
        """Test login with incorrect password."""
        response = self.client.post('/login', json={
            "username": self.seeker_username, "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid username or password", response.json['message'])

    def test_105_get_all_users(self):
        """Test retrieving all users."""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2) # seeker and provider created in setUp
        self.assertEqual(response.json[0]['username'], self.seeker_username)
        self.assertEqual(response.json[1]['username'], self.provider_username)

    def test_106_get_single_user_success(self):
        """Test retrieving a single user by ID successfully."""
        response = self.client.get(f'/users/{self.seeker_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], self.seeker_username)
        self.assertEqual(response.json['id'], self.seeker_id)

    def test_107_get_single_user_not_found(self):
        """Test retrieving a non-existent user by ID."""
        response = self.client.get('/users/9999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Resource not found", response.json['message'])

    # --- Test Cases for Service Category Endpoints ---

    def test_201_create_category_success(self):
        """Test creating a new service category successfully."""
        category_data = {"name": "Electrician"}
        response = self.client.post('/categories', json=category_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Category created successfully!", response.json['message'])
        self.assertIn("category_id", response.json)
        with app.app_context():
            self.assertIsNotNone(ServiceCategory.query.filter_by(name='Electrician').first())

    def test_202_create_category_existing_name(self):
        """Test creating a category with an already existing name."""
        response = self.client.post('/categories', json={"name": self.category_name}) # Using setUp category
        self.assertEqual(response.status_code, 409)
        self.assertIn("Category already exists", response.json['message'])

    def test_203_get_all_categories(self):
        """Test retrieving all service categories."""
        self.client.post('/categories', json={"name": "Gardening"}) # Add another category
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2) # Plumbing from setUp, Gardening just added
        self.assertEqual(response.json[0]['name'], self.category_name)
        self.assertEqual(response.json[1]['name'], 'Gardening')

    def test_204_get_single_category_success(self):
        """Test retrieving a single category by ID successfully."""
        response = self.client.get(f'/categories/{self.category_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], self.category_name)
        self.assertEqual(response.json['id'], self.category_id)

    # --- Test Cases for Service Endpoints ---

    def test_301_create_service_success(self):
        """Test creating a new service successfully."""
        service_data = {
            "provider_id": self.provider_id,
            "category_id": self.category_id,
            "name": "Drain Cleaning",
            "description": "Expert drain cleaning services.",
            "price": 75.00
        }
        response = self.client.post('/services', json=service_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Service created successfully!", response.json['message'])
        self.assertIn("service_id", response.json)
        with app.app_context():
            self.assertIsNotNone(Service.query.filter_by(name='Drain Cleaning').first())

    def test_302_create_service_invalid_provider_id(self):
        """Test creating a service with a non-existent provider ID."""
        service_data = {
            "provider_id": 9999,
            "category_id": self.category_id,
            "name": "Invalid Provider Service"
        }
        response = self.client.post('/services', json=service_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid or non-provider user ID", response.json['message'])

    def test_303_get_all_services(self):
        """Test retrieving all services."""
        self.client.post('/services', json={
            "provider_id": self.provider_id, "category_id": self.category_id, "name": "Pipe Repair"
        })
        response = self.client.get('/services')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1) # Only one service added in this test
        self.assertEqual(response.json[0]['name'], 'Pipe Repair')

    def test_304_update_service_success(self):
        """Test updating an existing service successfully."""
        create_response = self.client.post('/services', json={
            "provider_id": self.provider_id, "category_id": self.category_id, "name": "Old Service", "price": 100
        })
        service_id = create_response.json['service_id']

        update_data = {"name": "Updated Service Name", "price": 150.00}
        response = self.client.put(f'/services/{service_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Service updated successfully!", response.json['message'])
        with app.app_context():
            updated_service = Service.query.get(service_id)
            self.assertEqual(updated_service.name, "Updated Service Name")
            self.assertEqual(updated_service.price, 150.00)

    def test_305_delete_service_success(self):
        """Test deleting an existing service successfully."""
        create_response = self.client.post('/services', json={
            "provider_id": self.provider_id, "category_id": self.category_id, "name": "Service to Delete"
        })
        service_id = create_response.json['service_id']

        response = self.client.delete(f'/services/{service_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Service deleted successfully!", response.json['message'])
        with app.app_context():
            self.assertIsNone(Service.query.get(service_id))

    # --- Test Cases for Review Endpoints ---

    def test_401_create_review_success(self):
        """Test creating a new review successfully."""
        review_data = {
            "reviewer_id": self.seeker_id,
            "provider_id": self.provider_id,
            "rating": 5,
            "comment": "Outstanding work!"
        }
        response = self.client.post('/reviews', json=review_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Review created successfully!", response.json['message'])
        self.assertIn("review_id", response.json)
        with app.app_context():
            self.assertIsNotNone(Review.query.filter_by(reviewer_id=self.seeker_id, provider_id=self.provider_id).first())

    def test_402_create_review_invalid_rating(self):
        """Test creating a review with an invalid rating."""
        review_data = {
            "reviewer_id": self.seeker_id,
            "provider_id": self.provider_id,
            "rating": 6, # Invalid rating
            "comment": "Rating too high."
        }
        response = self.client.post('/reviews', json=review_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Rating must be between 1 and 5", response.json['message'])

    def test_403_get_all_reviews(self):
        """Test retrieving all reviews."""
        self.client.post('/reviews', json={
            "reviewer_id": self.seeker_id, "provider_id": self.provider_id, "rating": 4, "comment": "Good job."
        })
        response = self.client.get('/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['rating'], 4)
        self.assertEqual(response.json[0]['reviewer_username'], self.seeker_username)
        self.assertEqual(response.json[0]['provider_username'], self.provider_username)

    # --- Test Cases for Message Endpoints ---

    def test_501_send_message_success(self):
        """Test sending a new message successfully."""
        message_data = {
            "sender_id": self.seeker_id,
            "receiver_id": self.provider_id,
            "content": "Are you available next Tuesday?"
        }
        response = self.client.post('/messages', json=message_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Message sent successfully!", response.json['message'])
        self.assertIn("message_id", response.json)
        with app.app_context():
            self.assertIsNotNone(Message.query.filter_by(sender_id=self.seeker_id, receiver_id=self.provider_id).first())

    def test_502_send_message_invalid_sender_id(self):
        """Test sending a message with an invalid sender ID."""
        message_data = {
            "sender_id": 9999, # Non-existent ID
            "receiver_id": self.provider_id,
            "content": "This message should not go through."
        }
        response = self.client.post('/messages', json=message_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid sender or receiver ID", response.json['message'])

    def test_503_get_all_messages(self):
        """Test retrieving all messages."""
        self.client.post('/messages', json={
            "sender_id": self.seeker_id, "receiver_id": self.provider_id, "content": "Query about service."
        })
        response = self.client.get('/messages')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['content'], 'Query about service.')
        self.assertEqual(response.json[0]['sender_username'], self.seeker_username)
        self.assertEqual(response.json[0]['receiver_username'], self.provider_username)
