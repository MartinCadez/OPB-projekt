import logging
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash

from app import User, app
from auth.authentication import is_admin
from config import VERSION, cache

logger = logging.getLogger("app." + __name__)

cache.init_app(app.server)


GROUP_ICONS = {
    "MARKET DATA": html.I(className="fas fa-chart-area"),
    # "ENERGY": html.I(className="fas fa-bolt"),
    # "MODELS": html.I(className="bi bi-bar-chart-line-fill"),
    # "OUTLOOK": html.I(className="bi bi-calendar"),
    # "TEMPLATE GROUP": html.I(className="bi bi-bar-chart-line-fill"),
}


grouped_navigation_menu = {}
authorized_sidebar_pages = []

for _, data in dash.page_registry.items():
    excluded_pages = ["Login", "Profile", "Admin", "Home", "Logout"]
    if data["name"] not in excluded_pages:
        menu_item = {
            "display_name": data["name"],
            "url_path": data["path"],
            "category": data["group"].upper(),
            "requires_auth": data["auth"],
        }

        category_name = menu_item["category"]
        grouped_navigation_menu.setdefault(category_name, []).append(menu_item)
        authorized_sidebar_pages.append(menu_item)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=True),
        dcc.Store(id="login-status", storage_type="session"),
        dbc.Navbar(
            dbc.Container(
                [
                    dbc.Button(
                        html.I(
                            className="fas fa-bars",
                            style={"font-size": "40px", "color": "#EFEBE9"},
                        ),
                        outline=True,
                        id="hamburger-menu",
                        n_clicks=0,
                    ),
                    html.A(
                        dbc.Row(
                            [
                                dbc.Col(),
                            ],
                            align="center",
                            class_name="g-0",
                        ),
                        href="/",
                        style={"textDecoration": "none"},
                    ),
                    dbc.Nav(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.A(
                                            html.I(
                                                className="fas fa-home",
                                                style={
                                                    "font-size": "30px",
                                                    "color": "#EFEBE9",
                                                },
                                            ),
                                            href="/",
                                        )
                                    ),
                                    dbc.Col(
                                        html.A(
                                            html.I(
                                                className="fas fa-envelope",
                                                style={
                                                    "font-size": "30px",
                                                    "color": "#EFEBE9",
                                                },
                                            ),
                                            href="mailto:mc18257@student.uni-lj.si",
                                        )
                                    ),
                                    dbc.Col(
                                        dbc.DropdownMenu(
                                            [
                                                dbc.DropdownMenuItem(
                                                    "Log in", href="/login"
                                                )
                                            ],
                                            id="login-user-dropdown",
                                            nav=True,
                                            in_navbar=True,
                                            label="Guest",
                                            style={
                                                "font-size": "15px",
                                                "font-color": "#EFEBE9",
                                            },
                                            align_end=True,
                                        )
                                    ),
                                ]
                            ),
                        ],
                        navbar=True,
                    ),
                ],
            ),
            dark=True,
            color="#150357",
        ),
        dbc.Offcanvas(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span([group_icon, " ", group_name]),
                                html.Hr(style={"margin-bottom": "0"}),
                                html.Div(
                                    [
                                        html.Div(
                                            dbc.Button(
                                                f"{page['display_name']}",
                                                href=page["url_path"],
                                                outline=True,
                                                id=f"{page['display_name']}-button",
                                            ),
                                        )
                                        for page in grouped_navigation_menu[group_name]
                                    ]
                                ),
                                html.Br(),
                                html.Br(),
                            ]
                        )
                        for group_name, group_icon in GROUP_ICONS.items()
                    ]
                )
            ],
            id="offcanvas",
            scrollable=True,
            is_open=False,
            style={"backgroundColor": "#c9c9c4", "opacity": "1"},
        ),
        html.Div(dash.page_container, id="page-content"),
        html.Small(f"Version {VERSION}"),
    ],
    style={"background-color": "#fcfcfc"},
)

menu_button_list = [
    f"{page['display_name']}-button" for page in authorized_sidebar_pages
]


@app.callback(
    Output("offcanvas", "is_open"),
    [State("offcanvas", "is_open")],
    [Input("hamburger-menu", "n_clicks")]
    + [Input(i, "n_clicks") for i in menu_button_list],
)
def toggle_offcanvas(is_open, n1, *args):
    if n1:
        return not is_open
    else:
        return False


@app.callback(
    Output("url", "pathname"),
    Output("login-error-message", "children"),
    [
        Input("login-loginButton", "n_clicks"),
        Input("login-usernameBox", "n_submit"),
        Input("login-passwordBox", "n_submit"),
    ],
    [State("login-usernameBox", "value"), State("login-passwordBox", "value")],
)
def sucess(n_clicks, username_submit, password_submit, username, password):
    if not (n_clicks or username_submit or password_submit):
        return dash.no_update, ""

    if not username or not password:
        return dash.no_update, "Enter both username and password"

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        logger.info(f"User {username} login successful.")
        return "/", ""
    else:
        logger.info(f"User {username} login failed!")
        return dash.no_update, "Invalid username or password"


@app.callback(
    Output("login-usernameBox", "className"),
    [
        Input("login-loginButton", "n_clicks"),
        Input("login-usernameBox", "n_submit"),
        Input("login-passwordBox", "n_submit"),
    ],
    [State("login-usernameBox", "value")],
)
def user_invalid(n_clicks, username_submit, password_submit, username):
    if (n_clicks > 0) or (username_submit > 0) or password_submit > 0:
        user = User.query.filter_by(username=username).first()
        if user:
            return "form-control"
        else:
            return "form-control is-invalid"
    else:
        return "form-control"


@app.callback(
    Output("login-passwordBox", "className"),
    [
        Input("login-loginButton", "n_clicks"),
        Input("login-usernameBox", "n_submit"),
        Input("login-passwordBox", "n_submit"),
    ],
    [State("login-usernameBox", "value"), State("login-passwordBox", "value")],
)
def pass_invalid(n_clicks, username_submit, password_submit, username, password):
    if (n_clicks > 0) or (username_submit > 0) or password_submit > 0:
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                return "form-control"
            else:
                return "form-control is-invalid"
        else:
            return "form-control is-invalid"
    else:
        return "form-control"


@app.callback(
    Output("login-status", "data"),
    Output("login-user-dropdown", "children"),
    Output("login-user-dropdown", "label"),
    Input("url", "pathname"),
)
def update_authentication_status(path):
    if path == "/logout" and current_user.is_authenticated:
        logout_user()

    logged_in = current_user.is_authenticated

    if logged_in:
        user_name = current_user.username
        drop_down_list = [dbc.DropdownMenuItem("Profile", href="/profile")]
        if is_admin(current_user.username):
            drop_down_list.append(dbc.DropdownMenuItem("Admin", href="/admin"))
        drop_down_list.extend(
            [
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Logout", href="/logout"),
            ]
        )

    else:
        user_name = "Guest"
        drop_down_list = [dbc.DropdownMenuItem("Log in", href="/login")]

    return logged_in, drop_down_list, user_name


if __name__ == "__main__":
    base_path = Path(__file__).resolve().parent

    log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_output = logging.StreamHandler()
    console_output.setFormatter(log_formatter)

    file_output_path = (base_path / "app.log").as_posix()
    file_output = logging.FileHandler(file_output_path)
    file_output.setFormatter(log_formatter)

    app.logger.setLevel(logging.INFO)
    app.logger.handlers = [console_output, file_output]

    # app.server.wsgi_app = ProxyFix(
    #     app.server.wsgi_app,
    #     x_for=1,  # Number of proxies in front (Client IP)
    #     x_proto=1,  # Protocol (http vs https)
    #     x_host=1,  # Original host header
    #     x_prefix=1,  # URL prefix/subfolder
    # )

    app.run(host="0.0.0.0", port=8052, debug=True)
