"""
This is the main application file for
the Flask web application. It sets up
the Flask app, configures session management,
and registers the main blueprint for handling routes.
The app serves templates from the 'templates' directory
and static files from the 'assets' directory.
The application is designed to run in debug mode
for development purposes."""

import os
from flask import Flask
from views import main_blueprint

# Load environment variables from .env file
app = Flask(__name__,
            template_folder='templates',
            static_folder='assets',
            static_url_path='/assets')

# Enable sessions - use environment variable or fallback for development
app.secret_key = os.environ.get('session_secret_key', 'dev-secret-key')

# Register blueprint for routes
app.register_blueprint(main_blueprint)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
