from flask_login import UserMixin
from config import engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "app_user"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    @property
    def id(self):
        return self.user_id

    def check_password(self, password):
        return check_password_hash(self.password, password)


userTable = Table("app_user", User.metadata, autoload_with=engine)


def create_user_table():
    User.metadata.create_all(engine)


def add_user(username, password, email, admin):
    hashed_password = generate_password_hash(password, method="sha256")

    new_user = User(username=username, email=email, password=hashed_password)

    from app import server

    with server.app_context():
        db.session.add(new_user)
        db.session.commit()

    import yaml

    access_apps = ["all"] if admin else []

    access_file_path = "src/app/auth/authentication/access.yaml"
    try:
        with open(access_file_path, "r") as f:
            data = yaml.safe_load(f) or {}
    except FileNotFoundError:
        data = {}

    data[username] = {"admin": admin, "page_access": access_apps}

    with open(access_file_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)


def update_password(username, password):
    hashed_password = generate_password_hash(password, method="sha256")

    from app import server

    with server.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            user.password = hashed_password
            db.session.commit()


def show_users():
    from app import server

    with server.app_context():
        users = User.query.all()
        return [
            {"ID": user.user_id, "username": user.username, "email": user.email}
            for user in users
        ]
