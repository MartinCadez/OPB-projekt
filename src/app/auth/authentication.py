import yaml
import os
from functools import wraps
from dash import html, dcc
import dash_bootstrap_components as dbc
from flask_login import current_user


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ACCESS_YAML_PATH = os.path.join(CURRENT_DIR, "authentication", "access.yaml")


def load_access_config():
    with open(ACCESS_YAML_PATH, "r") as f:
        return yaml.safe_load(f) or {}


def is_admin(username: str) -> bool:
    return load_access_config().get(username, {}).get("admin", False)


def get_page_access(username: str) -> list:
    """returns which page groups are authorized for user to view"""
    return load_access_config().get(username, {}).get("page_access", [])


def get_users_with_access(page_group_name: str) -> list[str]:
    """returns list of all usernames authorized to access a specific page group"""
    return [
        user
        for user, info in load_access_config().items()
        if page_group_name in info.get("page_access", [])
        or "all" in info.get("page_access", [])
    ]


def check_access(app_name: str, username: str) -> bool:
    """returns true if user has access to all group pages"""
    permissions = get_page_access(username)
    return "all" in permissions or app_name in permissions


# --- UI COMPONENTS ---


def print_access_denied_msg(is_guest: bool):
    if is_guest:
        title = "Authentication Required"
        msg1 = "This page is not open for guest users."
        msg2 = "Please [log in](/login) or contact your Site Administrator to request access."
    else:
        title = "Access Denied"
        msg1 = "You do not have permission to view this page."
        msg2 = "Please contact your Site Administrator(s) to request access."

    return dbc.Container(
        [
            html.Br(),
            dbc.Row(
                dbc.Col(
                    [
                        html.H2(
                            [html.I(className="bi bi-x-circle-fill"), f" {title}"],
                            style={"color": "#ad1207"},
                        ),
                        html.Hr(),
                        html.P(msg1),
                        dcc.Markdown(msg2),
                    ],
                    md=6,
                    className="text-center shadow-sm p-4 bg-white rounded",
                ),
                justify="center",
            ),
        ],
        className="py-5",
    )


def authentication(app_name: str, auth: bool = False):
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            # display pages, if no auth is needed
            if not auth:
                return func(*args, **kwargs)

            # check if user is logged in via Flask-Login
            if not current_user or not current_user.is_authenticated:
                return print_access_denied_msg(is_guest=True)

            # check permissions
            has_access = check_access(app_name, current_user.username)
            is_profile = app_name == "Profile"

            if has_access or is_profile:
                return func(*args, **kwargs)

            # display access denied if user is logged in but has no permission
            return print_access_denied_msg(is_guest=False)

        return inner

    return outer
