import os


class Config:
    # Flask secret key to handle sessions and form validation
    # Ensure you use a strong key in production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key'

    # # SQLite database URI (now points to the site.db in the root directory)
    # SQLALCHEMY_DATABASE_URI = os.environ.get(
    #     'DATABASE_URL') or 'sqlite:///site.db'  # Changed from instance/site.db to root directory

    # SQLALCHEMY_DATABASE_URI = os.path.join(
    #     os.path.dirname(__file__), 'site.db')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    # Disable SQLAlchemy event system for better performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload configuration (for handling student image uploads)
    UPLOAD_FOLDER = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'static/uploads')  # Points to the static/uploads folder in the root
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB file upload limit
