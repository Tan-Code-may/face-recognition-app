from flask import Flask
from config import Config  # Import configuration
from extensions import db, bcrypt, login_manager  # Import extensions
from flask_migrate import Migrate  # Import Flask-Migrate

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    from routes import app_routes
    app.register_blueprint(app_routes)

    return app

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()

    app.run(debug=True)
