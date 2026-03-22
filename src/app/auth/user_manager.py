import json

from config import engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from werkzeug.security import generate_password_hash

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


def create_user_table():
    User.metadata.create_all(engine)


def edit_user():
    # Dostopi?
    pass


def send_msg_user_created():
    # Dostopi, geslo
    pass


def send_msg_user_edited():
    # Dostopi, ponastavitev gesla
    pass


def add_user(username, password, email, admin):
    hashed_password = generate_password_hash(password, method="sha256")

    insert_stmt = userTable.insert().values(
        username=username, email=email, password=hashed_password
    )

    access_apps = ["all"] if admin else []

    with open("authentication/access.json", "r+") as f:
        data = json.load(f)
        data[username] = {"admin": str(int(admin)), "access_apps": access_apps}
        f.seek(0)
        json.dump(data, f, indent=4)

    conn = engine.connect()
    conn.execute(insert_stmt)
    conn.close()


def update_password(username, password):
    hashed_password = generate_password_hash(password, method="sha256")

    update = (
        userTable.update()
        .values(password=hashed_password)
        .where(userTable.c.username == username)
    )

    conn = engine.connect()
    conn.execute(update)
    conn.close()


def show_users():
    select_stmt = select([userTable.c.id, userTable.c.username, userTable.c.email])

    conn = engine.connect()
    results = conn.execute(select_stmt)

    users = []

    for result in results:
        users.append({"ID": result[0], "username": result[1], "email": result[2]})

    conn.close()

    return users
