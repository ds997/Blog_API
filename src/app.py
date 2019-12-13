from flask import Flask

from .config import app_config
from .model_blog import db, bcrypt


def create_app(env_name):

    # app initiliazation

    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)

    db.init_app(app)

    @app.route('/', methods=['GET'])
    def index():
        """
        test endpoint
        """
        return 'Congratulations! Your first endpoint is working'

    return app
