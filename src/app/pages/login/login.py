import dash_bootstrap_components as dbc
from dash import dcc, html, register_page
import logging

logger = logging.getLogger("app." + __name__)
register_page(__name__, path="/login", name="Login", title="Dashboard - Login")

layout = dbc.Container(
    [
        dcc.Location(id="url-1", refresh=True),
        html.Br(),
        dbc.Container(
            [
                html.Div(
                    [
                        dbc.Container(
                            id="login-container1",
                            children=[
                                dcc.Input(
                                    placeholder="Enter your username",
                                    type="text",
                                    id="login-usernameBox",
                                    className="form-control",
                                    n_submit=0,
                                ),
                                html.Br(),
                                dcc.Input(
                                    placeholder="Enter your password",
                                    type="password",
                                    id="login-passwordBox",
                                    className="form-control",
                                    n_submit=0,
                                ),
                                html.Br(),
                                html.Button(
                                    children="Login",
                                    n_clicks=0,
                                    type="submit",
                                    id="login-loginButton",
                                    className="btn btn-primary btn-lg",
                                ),
                                html.Br(),
                                html.Div(
                                    id="login-error-message",
                                    style={"color": "red", "margin-top": "10px"},
                                ),
                            ],
                            className="form-group",
                        ),
                    ]
                ),
                html.Div(
                    dbc.Container([""], id="login-message"),
                    style={"margin-top": "15px"},
                ),
            ],
            className="jumbotron",
        ),
    ]
)
