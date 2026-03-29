import os
from pathlib import Path
import config

import dash
import dash_bootstrap_components as dbc
from flask_login import LoginManager
from auth.user_manager import db, User


app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.SANDSTONE,
        dbc.icons.FONT_AWESOME,
        dbc.icons.BOOTSTRAP,
    ],
    use_pages=True,
    update_title="Dashboard - Updating",
    title="Dashboard",
)

app._favicon = (
    Path(__file__).parent / "assets" / "img" / "dashboard_icon.png"
).as_posix()

server = app.server
app.config.suppress_callback_exceptions = True

server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=config.DB_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db.init_app(server)

with server.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
