# ISETA: Connecting Kigali with Skilled Professionals

#### ISETA (meaning "a market place where we find skilled people for hire" in Kinyarwanda) is a web-based platform designed to revolutionize how urban residents in Kigali connect with trustworthy local skilled professionals. It aims to create a transparent and efficient marketplace for various services, like  plumbing and electrical etc.

The Problem ISETA Solves
* Lack of Trust and Transparency
* Limited Discovery
* Marketing for professionals
* Inconsistent Quality & Pricing

## Current Functional Features 
* User Registration:
    1. Allows new users to register as either a Service Seeker (resident) or a Service Provider (professional).
    2. Providers can include a bio, location, and contact information during registration.
* User Login & Authentication:
    1. Secure login for registered users.
    2. Basic session management using browser's localStorage to keep users logged in (for MVP purposes).
* Service Category Management:
    1. Backend support for defining and managing various service categories (e.g., Plumbing, Electrical, IT Support, Carpentry).
    2. Frontend dynamically loads these categories for service creation and browsing.
* Service Listing & Browsing:
    1. Users can browse a comprehensive list of available services.
    2. Basic filtering by service category and keyword search is supported.

## How to Visit the Site

###  Accessing the Live Deployment (Render)
1. Open your web browser
2. Navigate to the following URL: https://iseta-app.onrender.com

    * NB: If using this link you face any issue Kindly follow the steps below as they are issues with deployment that i am still trouble shooting



### Running the Application Locally (Development Environment)

#### Prerequisites

* Python 3.9+ installed.
* pip (Python package installer) installed.
* git installed.
#### Step by Step Guide 
0. Clone the Repository: Open your terminal or command prompt and clone the ISETA application from GitHub
    * git clone https://github.com/TWA-Coder/iseta-app.git

1. Create and Activate a Virtual Environment: python3 -m venv venv

    * On macOS/Linux: source venv/bin/activate
    * On Windows (Command Prompt): venv\Scripts\activate.bat
    * On Windows (PowerShell): .\venv\Scripts\Activate.ps1

2. Install Dependencies: pip install -r requirements.txt

3. Initialize the Database: python3 app.py

4. Run the Flask Application: The server will typically run on http://127.0.0.1:5000.

5. Access the Frontend in Your Browser: Open your web browser and go to: http://127.0.0.1:5000/

### Enjoy using ISETA!
