from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__)

    # used by flask-login
    app.config['SECRET_KEY'] = 'secret-key-goes-here'

    bootstrap.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User(id)

    return app

app = create_app()