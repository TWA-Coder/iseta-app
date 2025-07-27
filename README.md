ISETA: Connecting Kigali with Skilled Professionals
Project Overview
ISETA (meaning "a market place where we find skilled people for hire" in Kinyarwanda) is a web-based platform designed to revolutionize how urban residents in Kigali connect with trustworthy local skilled professionals. It aims to create a transparent and efficient marketplace for various services, like  plumbing and electrical etc.
The Problem ISETA Solves
In many urban areas, including Kigali, residents often face significant challenges when trying to find reliable and skilled local professionals. These challenges include:
Lack of Trust and Transparency: It's difficult to verify the credibility, skill level, and pricing of independent service providers, leading to uncertainty and potential exploitation.
Limited Discovery: Finding specific skilled workers (e.g., a reliable plumber, an experienced electrician, a professional cobbler, or even a recording studio) often relies on word-of-mouth, which can be inefficient and restrictive.
Marketing for Professionals: Independent professionals and small businesses struggle to effectively market their services and reach a wider client base beyond their immediate network.
Inconsistent Quality & Pricing: Without a centralized platform, quality standards and pricing can vary wildly, making it hard for consumers to make informed decisions.
ISETA addresses these issues by providing a centralized, transparent, and user-friendly platform that fosters trust, enhances discovery, and empowers both service seekers and providers.
Current Functional Features 
The current Minimum Viable Product (MVP) of ISETA includes the following core functionalities:
User Registration:
Allows new users to register as either a Service Seeker (resident) or a Service Provider (professional).
Providers can include a bio, location, and contact information during registration.
User Login & Authentication:
Secure login for registered users.
Basic session management using browser's localStorage to keep users logged in (for MVP purposes).
Service Category Management:
Backend support for defining and managing various service categories (e.g., Plumbing, Electrical, IT Support, Carpentry).
Frontend dynamically loads these categories for service creation and browsing.
Service Listing & Browsing:
Users can browse a comprehensive list of available services.
Basic filtering by service category and keyword search is supported.
Service Creation (for Providers):
Logged-in Service Providers can add new services, specifying the service name, description, category, and price.
Provider Profile Viewing:
Users can view detailed profiles of individual service providers, including their bio, contact information, services offered, and received reviews.

How to Visit the Site
Option 1: Accessing the Live Deployment (Render)
If the application is successfully deployed on Render, you can visit it directly via the public URL.
Open your web browser.
Navigate to the following URL: 
https://iseta-app.onrender.com.
Note: If you face the fetch error while registering, that means that I am still trouble shooting to find the issue, Please use this second method instead.
Option 2: Running the Application Locally (Development Environment)
To run ISETA on your local machine, follow these steps:
Prerequisites
Python 3.9+ installed.
pip (Python package installer) installed.
git installed.
Step-by-Step Guide
Clone the Repository: Open your terminal or command prompt and clone the ISETA application from GitHub:
git clone https://github.com/TWA-Coder/iseta-app.git

cd iseta-app

Create and Activate a Virtual Environment: It's best practice to use a virtual environment to manage project dependencies.
python3 -m venv venv



On macOS/Linux:
source venv/bin/activate


On Windows (Command Prompt):
venv\Scripts\activate.bat


On Windows (PowerShell):
.\venv\Scripts\Activate.ps1


Install Dependencies: Install all required Python packages using pip from the requirements.txt file.
pip install -r requirements.txt

Initialize the Database: The Flask application uses SQLite, and the tables need to be created.
python3 app.py



You will see a message like "Database tables created (or already exist)!" in your terminal. After this, you can press Ctrl+C to stop the development server for a moment, or simply proceed to the next step as it will restart.
Run the Flask Application: Start the Flask development server. This will serve both your backend API and your frontend HTML/CSS/JS files.
python app.py



The server will typically run on http://127.0.0.1:5000.
Access the Frontend in Your Browser: Open your web browser and go to:
http://127.0.0.1:5000/


You can then navigate through the application (e.g., /register, /login_page, /services_page) to test its functionalities.
Enjoy using ISETA!

