<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ISETA App README</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f4f7f6;
            color: #333;
        }
        .container {
            max-width: 900px;
            margin: 30px auto;
            background-color: #ffffff;
            padding: 30px 40px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #2c3e50;
            font-size: 2.5em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 30px;
            text-align: center;
        }
        h2 {
            color: #3498db;
            font-size: 1.8em;
            margin-top: 30px;
            margin-bottom: 15px;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 5px;
        }
        h3 {
            color: #2c3e50;
            font-size: 1.4em;
            margin-top: 25px;
            margin-bottom: 10px;
        }
        p {
            margin-bottom: 15px;
        }
        ul {
            list-style: disc;
            margin-left: 25px;
            margin-bottom: 15px;
        }
        ul li {
            margin-bottom: 8px;
        }
        strong {
            font-weight: 600;
        }
        code {
            background-color: #eef1f5;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9em;
            color: #c0392b; /* A darker red for inline code */
        }
        pre {
            background-color: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            margin-bottom: 20px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9em;
        }
        pre code {
            background-color: transparent;
            color: inherit;
            padding: 0;
            border-radius: 0;
        }
        .note {
            background-color: #eaf7fd;
            border-left: 5px solid #3498db;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
            color: #2c3e50;
        }
        .note strong {
            color: #3498db;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ISETA: Connecting Kigali with Skilled Professionals</h1>

        <h2>Project Overview</h2>
        <p>ISETA (meaning "a market place where we find skilled people for hire"in Kinyarwanda) is a web-based platform designed to revolutionize how urban residents in Kigali, Rwanda, connect with trustworthy local skilled professionals. It aims to create a transparent and efficient marketplace for various services, from plumbing and electrical work to specialized crafts.</p>

        <h2>The Problem ISETA Solves</h2>
        <p>In many urban areas, including Kigali, residents often face significant challenges when trying to find reliable and skilled local professionals. These challenges include:</p>
        <ul>
            <li><strong>Lack of Trust and Transparency:</strong> It's difficult to verify the credibility, skill level, and pricing of independent service providers, leading to uncertainty and potential exploitation.</li>
            <li><strong>Limited Discovery:</strong> Finding specific skilled workers (e.g., a reliable plumber, an experienced electrician, a professional cobbler, or even a recording studio) often relies on word-of-mouth, which can be inefficient and restrictive.</li>
            <li><strong>Marketing for Professionals:</strong> Independent professionals and small businesses struggle to effectively market their services and reach a wider client base beyond their immediate network.</li>
            <li><strong>Inconsistent Quality & Pricing:</strong> Without a centralized platform, quality standards and pricing can vary wildly, making it hard for consumers to make informed decisions.</li>
        </ul>
        <p>ISETA addresses these issues by providing a centralized, transparent, and user-friendly platform that fosters trust, enhances discovery, and empowers both service seekers and providers.</p>

        <h2>Current Functional Features (MVP)</h2>
        <p>The current Minimum Viable Product (MVP) of ISETA includes the following core functionalities:</p>
        <ol>
            <li>
                <h3>User Registration:</h3>
                <ul>
                    <li>Allows new users to register as either a <strong>Service Seeker</strong> (resident) or a <strong>Service Provider</strong> (professional).</li>
                    <li>Providers can include a bio, location, and contact information during registration.</li>
                </ul>
            </li>
            <li>
                <h3>User Login & Authentication:</h3>
                <ul>
                    <li>Secure login for registered users.</li>
                    <li>Basic session management using browser's <code>localStorage</code> to keep users logged in (for MVP purposes).</li>
                </ul>
            </li>
            <li>
                <h3>Service Category Management:</h3>
                <ul>
                    <li>Backend support for defining and managing various service categories (e.g., Plumbing, Electrical, IT Support, Carpentry).</li>
                    <li>Frontend dynamically loads these categories for service creation and browsing.</li>
                </ul>
            </li>
            <li>
                <h3>Service Listing & Browsing:</h3>
                <ul>
                    <li>Users can browse a comprehensive list of available services.</li>
                    <li>Basic filtering by service category and keyword search is supported.</li>
                </ul>
            </li>
            <li>
                <h3>Service Creation (for Providers):</h3>
                <ul>
                    <li>Logged-in Service Providers can add new services, specifying the service name, description, category, and price.</li>
                </ul>
            </li>
            <li>
                <h3>Provider Profile Viewing:</h3>
                <ul>
                    <li>Users can view detailed profiles of individual service providers, including their bio, contact information, services offered, and received reviews.</li>
                </ul>
            </li>
            <li>
                <h3>Review Submission:</h3>
                <ul>
                    <li>Logged-in users can submit star ratings (1-5) and written comments for service providers.</li>
                </ul>
            </li>
            <li>
                <h3>Direct Messaging:</h3>
                <ul>
                    <li>A simple in-app messaging interface allows logged-in users to send messages to service providers.</li>
                </ul>
            </li>
        </ol>

        <h2>How to Visit the Site</h2>

        <h3>Option 1: Accessing the Live Deployment (Render)</h3>
        <p>If the application is successfully deployed on Render, you can visit it directly via the public URL.</p>
        <ol>
            <li><strong>Open your web browser.</strong></li>
            <li>
                <p><strong>Navigate to the following URL:</strong><br>
                <code>https://your-iseta-backend.onrender.com</code> (Replace <code>your-iseta-backend.onrender.com</code> with the actual URL provided by Render for your backend service).</p>
                <div class="note">
                    <strong>Note:</strong> If your frontend is hosted separately (e.g., on a different Render service or Netlify), you will need to visit its specific URL. The backend URL provided above is for the API.
                </div>
            </li>
        </ol>

        <h3>Option 2: Running the Application Locally (Development Environment)</h3>
        <p>To run ISETA on your local machine, follow these steps:</p>

        <h4>Prerequisites</h4>
        <ul>
            <li>Python 3.9+ installed.</li>
            <li><code>pip</code> (Python package installer) installed.</li>
            <li><code>git</code> installed.</li>
        </ul>

        <h4>Step-by-Step Guide</h4>
        <ol>
            <li>
                <strong>Clone the Repository:</strong><br>
                Open your terminal or command prompt and clone the ISETA application from GitHub:
                <pre><code>git clone https://github.com/TWA-Coder/iseta-app.git
cd iseta-app</code></pre>
            </li>
            <li>
                <strong>Create and Activate a Virtual Environment:</strong><br>
                It's best practice to use a virtual environment to manage project dependencies.
                <pre><code>python3 -m venv venv</code></pre>
                <ul>
                    <li><strong>On macOS/Linux:</strong>
                        <pre><code>source venv/bin/activate</code></pre>
                    </li>
                    <li><strong>On Windows (Command Prompt):</strong>
                        <pre><code>venv\Scripts\activate.bat</code></pre>
                    </li>
                    <li><strong>On Windows (PowerShell):</strong>
                        <pre><code>.\venv\Scripts\Activate.ps1</code></pre>
                    </li>
                </ul>
            </li>
            <li>
                <strong>Install Dependencies:</strong><br>
                Install all required Python packages using <code>pip</code> from the <code>requirements.txt</code> file.
                <pre><code>pip install -r requirements.txt</code></pre>
            </li>
            <li>
                <strong>Initialize the Database:</strong><br>
                The Flask application uses SQLite, and the tables need to be created.
                <pre><code>python app.py</code></pre>
                <div class="note">
                    You will see a message like "Database tables created (or already exist)!" in your terminal. After this, you can press <code>Ctrl+C</code> to stop the development server for a moment, or simply proceed to the next step as it will restart.
                </div>
            </li>
            <li>
                <strong>Run the Flask Application:</strong><br>
                Start the Flask development server. This will serve both your backend API and your frontend HTML/CSS/JS files.
                <pre><code>python app.py</code></pre>
                <div class="note">
                    The server will typically run on <code>http://127.0.0.1:5000</code>.
                </div>
            </li>
            <li>
                <strong>Access the Frontend in Your Browser:</strong><br>
                Open your web browser and go to:
                <pre><code>http://127.0.0.1:5000/</code></pre>
                <p>You can then navigate through the application (e.g., <code>/register</code>, <code>/login_page</code>, <code>/services_page</code>) to test its functionalities.</p>
            </li>
        </ol>
        <p>Enjoy using ISETA!</p>
    </div>
</body>
</html>

