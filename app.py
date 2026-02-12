

from flask import Flask
from views import main_blueprint
import os

app = Flask(__name__, template_folder='templates', static_folder='assets', static_url_path='/assets')

# Enable sessions - use environment variable or fallback for development
app.secret_key = os.environ.get('session_secret_key', 'dev-secret-key')

# Register blueprint for routes
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)