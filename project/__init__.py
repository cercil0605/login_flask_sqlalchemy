from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy
db = SQLAlchemy()

# setup flask-login
def setup_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User  # use models module
    # get user information by using primary key
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

def setup_blueprints(app):
    from .auth import auth as auth_blueprint # import auth.py
    app.register_blueprint(auth_blueprint) # register
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'V25rye3HQZPw'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)

    # set up for login manager
    setup_login_manager(app)
    # blueprint for auth routes in our app
    setup_blueprints(app)

    return app