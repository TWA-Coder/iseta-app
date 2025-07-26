from flask_bcrypt import Bcrypt
from flask import Flask, request, jsonify
from flask import render_template 
from flask_sqlalchemy import SQLAlchemy
import os
import unittest

# --- Flask Application Setup ---
app = Flask(__name__)
# Initialize Bcrypt
bcrypt = Bcrypt(app)
# --- Database Configuration ---
# Create an 'instance' folder if it doesn't exist to store the database file
# This helps keep the database file separate from your code
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable tracking modifications for performance

# --- Initialize SQLAlchemy ---
db = SQLAlchemy(app)

# --- Define Your Database Models (Tables) ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False) # Store hashed passwords, NEVER plain text!
    user_type = db.Column(db.String(20), nullable=False) # e.g., 'seeker', 'provider'
    location = db.Column(db.String(100), nullable=True)
    contact_info = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True) # For service providers

    def __repr__(self):
        return f'<User {self.username} ({self.user_type})>'

class ServiceCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    services = db.relationship('Service', backref='category', lazy=True)

    def __repr__(self):
        return f'<ServiceCategory {self.name}>'

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('service_category.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=True)
    provider = db.relationship('User', backref='services_offered', lazy=True)


    def __repr__(self):
        return f'<Service {self.name} by User ID {self.provider_id}>'

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False) # 1-5 stars
    comment = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    reviewer = db.relationship('User', foreign_keys=[reviewer_id], backref='reviews_given', lazy=True)
    provider = db.relationship('User', foreign_keys=[provider_id], backref='reviews_received', lazy=True)

    def __repr__(self):
        return f'<Review ID {self.id} for Provider {self.provider_id} by Reviewer {self.reviewer_id}>'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages', lazy=True)
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages', lazy=True)

    def __repr__(self):
        return f'<Message from {self.sender_id} to {self.receiver_id}>'
    
#---Front end connection(API Routes)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login_page') # Renamed to avoid conflict with /login API endpoint
def login_page():
    return render_template('login.html')

@app.route('/services_page') # Renamed for clarity
def services_page():
    return render_template('services.html')

@app.route('/profile_page/<int:user_id>')
def profile_page(user_id):
    return render_template('profile.html', user_id=user_id) # Pass ID to template

@app.route('/messages_page')
def messages_page():
    return render_template('messages.html')

@app.route('/review_page/<int:provider_id>')
def review_page(provider_id):
    return render_template('review_form.html', provider_id=provider_id)

# --- Basic Routes (API Endpoints) ---

@app.route('/')
def home():
    return "Welcome to ISETA Backend"

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid JSON"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')
    location = data.get('location')
    contact_info = data.get('contact_info')
    bio = data.get('bio') if user_type == 'provider' else None

    if not all([username, email, password, user_type]):
        return jsonify({"message": "Missing required fields"}), 400

    # Hash the password before storing it!
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Basic validation for user_type
    if user_type not in ['seeker', 'provider']:
        return jsonify({"message": "Invalid user_type. Must be 'seeker' or 'provider'."}), 400

    # Check if username or email already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409

    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        user_type=user_type,
        location=location,
        contact_info=contact_info,
        bio=bio
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully!", "user_id": new_user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating user", "error": str(e)}), 500

# login route
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data or not all(k in data for k in ['username', 'password']):
        return jsonify({"message": "Username and password are required"}), 400

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid username or password"}), 401 # 401 Unauthorized

    return jsonify({"message": "Login successful!", "user_id": user.id, "user_type": user.user_type}), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = []
    for user in users:
        users_data.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "user_type": user.user_type,
            "location": user.location,
            "contact_info": user.contact_info,
            "bio": user.bio
        })
    return jsonify(users_data), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "user_type": user.user_type,
        "location": user.location,
        "contact_info": user.contact_info,
        "bio": user.bio
    }
    return jsonify(user_data), 200

@app.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"message": "Category name is required"}), 400

    name = data['name'].strip()
    if not name:
        return jsonify({"message": "Category name cannot be empty"}), 400

    if ServiceCategory.query.filter_by(name=name).first():
        return jsonify({"message": "Category already exists"}), 409

    new_category = ServiceCategory(name=name)
    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message": "Category created successfully!", "category_id": new_category.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating category", "error": str(e)}), 500

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = ServiceCategory.query.all()
    categories_data = [{"id": cat.id, "name": cat.name} for cat in categories]
    return jsonify(categories_data), 200

@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = ServiceCategory.query.get_or_404(category_id)
    return jsonify({"id": category.id, "name": category.name}), 200

@app.route('/services', methods=['POST'])
def create_service():
    data = request.get_json()
    if not data or not all(k in data for k in ['provider_id', 'category_id', 'name']):
        return jsonify({"message": "Missing required service fields"}), 400

    provider = User.query.get(data['provider_id'])
    category = ServiceCategory.query.get(data['category_id'])
    if not provider or provider.user_type != 'provider':
        return jsonify({"message": "Invalid or non-provider user ID"}), 400
    if not category:
        return jsonify({"message": "Invalid category ID"}), 400

    new_service = Service(
        provider_id=data['provider_id'],
        category_id=data['category_id'],
        name=data['name'],
        description=data.get('description'),
        price=data.get('price')
    )
    try:
        db.session.add(new_service)
        db.session.commit()
        return jsonify({"message": "Service created successfully!", "service_id": new_service.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating service", "error": str(e)}), 500

@app.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    services_data = []
    for service in services:
        services_data.append({
            "id": service.id,
            "provider_id": service.provider_id,
            "category_id": service.category_id,
            "name": service.name,
            "description": service.description,
            "price": service.price,
            "provider_username": service.provider.username,
            "category_name": service.category.name
        })
    return jsonify(services_data), 200

@app.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = Service.query.get_or_404(service_id)
    return jsonify({
        "id": service.id,
        "provider_id": service.provider_id,
        "category_id": service.category_id,
        "name": service.name,
        "description": service.description,
        "price": service.price,
        "provider_username": service.provider.username,
        "category_name": service.category.name
    }), 200

@app.route('/services/<int:service_id>', methods=['PUT', 'PATCH'])
def update_service(service_id):
    service = Service.query.get_or_404(service_id)
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided for update"}), 400

    if 'name' in data:
        service.name = data['name']
    if 'description' in data:
        service.description = data['description']
    if 'price' in data:
        service.price = data['price']

    try:
        db.session.commit()
        return jsonify({"message": "Service updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating service", "error": str(e)}), 500

@app.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    try:
        db.session.delete(service)
        db.session.commit()
        return jsonify({"message": "Service deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting service", "error": str(e)}), 500

@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    if not data or not all(k in data for k in ['reviewer_id', 'provider_id', 'rating']):
        return jsonify({"message": "Missing required review fields"}), 400

    reviewer = User.query.get(data['reviewer_id'])
    provider = User.query.get(data['provider_id'])

    if not reviewer or not provider:
        return jsonify({"message": "Invalid reviewer or provider ID"}), 400
    if not (1 <= data['rating'] <= 5):
        return jsonify({"message": "Rating must be between 1 and 5"}), 400

    new_review = Review(
        reviewer_id=data['reviewer_id'],
        provider_id=data['provider_id'],
        rating=data['rating'],
        comment=data.get('comment')
    )
    try:
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"message": "Review created successfully!", "review_id": new_review.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating review", "error": str(e)}), 500

@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    reviews_data = []
    for review in reviews:
        reviews_data.append({
            "id": review.id,
            "reviewer_id": review.reviewer_id,
            "provider_id": review.provider_id,
            "rating": review.rating,
            "comment": review.comment,
            "timestamp": review.timestamp.isoformat() if review.timestamp else None,
            "reviewer_username": review.reviewer.username,
            "provider_username": review.provider.username
        })
    return jsonify(reviews_data), 200

@app.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review.query.get_or_404(review_id)
    return jsonify({
        "id": review.id,
        "reviewer_id": review.reviewer_id,
        "provider_id": review.provider_id,
        "rating": review.rating,
        "comment": review.comment,
        "timestamp": review.timestamp.isoformat() if review.timestamp else None,
        "reviewer_username": review.reviewer.username,
        "provider_username": review.provider.username
    }), 200

@app.route('/messages', methods=['POST'])
def send_message():
    data = request.get_json()
    if not data or not all(k in data for k in ['sender_id', 'receiver_id', 'content']):
        return jsonify({"message": "Missing required message fields"}), 400

    sender = User.query.get(data['sender_id'])
    receiver = User.query.get(data['receiver_id'])

    if not sender or not receiver:
        return jsonify({"message": "Invalid sender or receiver ID"}), 400

    new_message = Message(
        sender_id=data['sender_id'],
        receiver_id=data['receiver_id'],
        content=data['content']
    )
    try:
        db.session.add(new_message)
        db.session.commit()
        return jsonify({"message": "Message sent successfully!", "message_id": new_message.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error sending message", "error": str(e)}), 500

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    messages_data = []
    for message in messages:
        messages_data.append({
            "id": message.id,
            "sender_id": message.sender_id,
            "receiver_id": message.receiver_id,
            "content": message.content,
            "timestamp": message.timestamp.isoformat() if message.timestamp else None,
            "sender_username": message.sender.username,
            "receiver_username": message.receiver.username
        })
    return jsonify(messages_data), 200

@app.route('/messages/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = Message.query.get_or_404(message_id)
    return jsonify({
        "id": message.id,
        "sender_id": message.sender_id,
        "receiver_id": message.receiver_id,
        "content": message.content,
        "timestamp": message.timestamp.isoformat() if message.timestamp else None,
        "sender_username": message.sender.username,
        "receiver_username": message.receiver.username
    }), 200

#general error handler
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"message": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback() # Ensure any pending transactions are rolled back
    return jsonify({"message": "Internal server error"}), 500

# --- Main execution block ---
if __name__ == '__main__':
    with app.app_context():
        instance_path = os.path.join(basedir, 'instance')
        os.makedirs(instance_path, exist_ok=True)
        db.create_all()
        print("Database tables created (or already exist)!")

    app.run()