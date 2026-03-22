import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from flask_login import current_user
from werkzeug.security import check_password_hash

from dash import register_page, callback
from auth.user_manager import update_password
from auth.authentication import authentication

import logging

logger = logging.getLogger("app." + __name__)
register_page(__name__, path="/profile", name="Profile", title="Dashboard - Profile")


@authentication(app_name="Profile", auth=True)
def layout():
    main_layout = dbc.Container(
        [
            html.Br(),
            dbc.Container(
                [
                    html.H3("Profile Management"),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Label("Username:"),
                                    html.Br(),
                                    html.Br(),
                                    dbc.Label("Email:"),
                                ],
                                md=2,
                            ),
                            dbc.Col(
                                [
                                    dbc.Label(
                                        id="profile-username", className="text-success"
                                    ),
                                    html.Br(),
                                    html.Br(),
                                    dbc.Label(id="email", className="text-success"),
                                ],
                                md=4,
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Old Password: "),
                                    dcc.Input(
                                        id="profile-oldpassword",
                                        type="password",
                                        className="form-control",
                                        placeholder="old password",
                                        n_submit=0,
                                        style={"width": "40%"},
                                    ),
                                    html.Br(),
                                    dbc.Label("New Password: "),
                                    dcc.Input(
                                        id="profile-newpassword1",
                                        type="password",
                                        className="form-control",
                                        placeholder="new password",
                                        n_submit=0,
                                        style={"width": "40%"},
                                    ),
                                    html.Br(),
                                    dbc.Label("Retype New Password: "),
                                    dcc.Input(
                                        id="profile-newpassword2",
                                        type="password",
                                        className="form-control",
                                        placeholder="retype new password",
                                        n_submit=0,
                                        style={"width": "40%"},
                                    ),
                                    html.Br(),
                                    html.Button(
                                        children="Update Password",
                                        id="profile-update-pass-button",
                                        n_clicks=0,
                                        type="submit",
                                        className="btn btn-primary btn-lg",
                                    ),
                                    html.Br(),
                                    html.Div(id="updateSuccess"),
                                ],
                                md=6,
                            ),
                        ]
                    ),
                ],
                className="jumbotron",
            ),
        ]
    )
    return main_layout


@callback(Output("profile-username", "children"), [Input("page-content", "children")])
def current_username(page_content):
    try:
        username = current_user.username
        return username
    except AttributeError:
        return ""


@callback(Output("email", "children"), [Input("page-content", "children")])
def current_user_email(page_content):
    try:
        email = current_user.email
        return email
    except AttributeError:
        return ""


@callback(
    Output("profile-oldpassword", "className"),
    [
        Input("profile-update-pass-button", "n_clicks"),
        Input("profile-newpassword1", "n_submit"),
        Input("profile-newpassword2", "n_submit"),
    ],
    [State("profile-oldpassword", "value")],
)
def validate_old_password(n_clicks, new_pass1_submit, new_pass2_submit, old_pass):
    if (n_clicks > 0) or (new_pass1_submit > 0) or new_pass2_submit > 0:
        if check_password_hash(current_user.password, old_pass):
            return "form-control is-valid"
        else:
            return "form-control is-invalid"
    else:
        return "form-control"


@callback(
    Output("profile-newpassword1", "className"),
    [
        Input("profile-update-pass-button", "n_clicks"),
        Input("profile-newpassword1", "n_submit"),
        Input("profile-newpassword2", "n_submit"),
    ],
    [State("profile-newpassword1", "value"), State("profile-newpassword2", "value")],
)
def validate_password_1(
    n_clicks, new_pass1_submit, new_pass2_submit, new_pass1, new_pass2
):
    if (n_clicks > 0) or (new_pass1_submit > 0) or new_pass2_submit > 0:
        if new_pass1 == new_pass2:
            return "form-control is-valid"
        else:
            return "form-control is-invalid"
    else:
        return "form-control"


@callback(
    Output("profile-newpassword2", "className"),
    [
        Input("profile-update-pass-button", "n_clicks"),
        Input("profile-newpassword1", "n_submit"),
        Input("profile-newpassword2", "n_submit"),
    ],
    [State("profile-newpassword1", "value"), State("profile-newpassword2", "value")],
)
def validate_password2(
    n_clicks, new_pass1_submit, new_pass2_submit, new_pass1, new_pass2
):
    if (n_clicks > 0) or (new_pass1_submit > 0) or new_pass2_submit > 0:
        if new_pass1 == new_pass2:
            return "form-control is-valid"
        else:
            return "form-control is-invalid"
    else:
        return "form-control"


@callback(
    Output("updateSuccess", "children"),
    [
        Input("profile-update-pass-button", "n_clicks"),
        Input("profile-newpassword1", "n_submit"),
        Input("profile-newpassword2", "n_submit"),
    ],
    [
        State("profile-oldpassword", "value"),
        State("profile-newpassword1", "value"),
        State("profile-newpassword2", "value"),
    ],
)
def change_password(
    n_clicks, new_pass1_submit, new_pass2_submit, old_pass, new_pass1, new_pass2
):
    if (n_clicks > 0) or (new_pass1_submit > 0) or new_pass2_submit > 0:
        if (
            check_password_hash(current_user.password, old_pass)
            and new_pass1 == new_pass2
        ):
            try:
                update_password(current_user.username, new_pass1)
                return html.Div(
                    children=["Update Successful"], className="text-success"
                )
            except Exception as e:
                return html.Div(
                    children=["Update Not Successful: {e}".format(e=e)],
                    className="text-danger",
                )
        else:
            return html.Div(children=["Old Password Invalid"], className="text-danger")
