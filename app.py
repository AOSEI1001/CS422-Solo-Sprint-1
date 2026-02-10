

from flask import Flask
from views import main_blueprint

app = Flask(__name__, template_folder='templates', static_folder='assets', static_url_path='/assets')

# Register blueprint for routes
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)