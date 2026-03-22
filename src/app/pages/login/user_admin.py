from dash import dcc, html
import dash_bootstrap_components as dbc
from dash import dash_table as dt
from dash.dependencies import Input, Output, State

from auth.user_manager import show_users, add_user
from dash import register_page, callback
import logging
from auth.authentication import authentication

logger = logging.getLogger("app." + __name__)
register_page(__name__, path="/admin", name="Admin", title="Dashboard - Admin")


@authentication(app_name="Admin", auth=True)
def layout():
    layout_main = dbc.Container(
        [
            html.Br(),
            dbc.Container(
                [
                    html.H3("Add New User"),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Label("Username: "),
                                    dcc.Input(
                                        id="new_username",
                                        className="form-control",
                                        n_submit=0,
                                        style={"width": "90%"},
                                    ),
                                    html.Br(),
                                    dbc.Label("Password: "),
                                    dcc.Input(
                                        id="newPwd1",
                                        type="password",
                                        className="form-control",
                                        n_submit=0,
                                        style={"width": "90%"},
                                    ),
                                    html.Br(),
                                    dbc.Label("Retype New Password: "),
                                    dcc.Input(
                                        id="newPwd2",
                                        type="password",
                                        className="form-control",
                                        n_submit=0,
                                        style={"width": "90%"},
                                    ),
                                    html.Br(),
                                ],
                                md=4,
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Email: "),
                                    dcc.Input(
                                        id="new_email",
                                        className="form-control",
                                        n_submit=0,
                                        style={"width": "90%"},
                                    ),
                                    html.Br(),
                                    dbc.Label("Admin? "),
                                    dcc.Dropdown(
                                        id="admin",
                                        style={"width": "90%"},
                                        options=[
                                            {"label": "Yes", "value": 1},
                                            {"label": "No", "value": 0},
                                        ],
                                        value=0,
                                        clearable=False,
                                    ),
                                    html.Br(),
                                    html.Br(),
                                    html.Button(
                                        children="Create User",
                                        id="createUserButton",
                                        n_clicks=0,
                                        type="submit",
                                        className="btn btn-primary btn-lg",
                                    ),
                                    html.Br(),
                                    html.Div(id="createUserSuccess"),
                                ],
                                md=4,
                            ),
                            dbc.Col([], md=4),
                        ]
                    ),
                ],
                className="jumbotron",
            ),
            dbc.Container(
                [
                    html.H3("View Users"),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dt.DataTable(
                                        id="users",
                                        columns=[
                                            {"name": "ID", "id": "ID"},
                                            {"name": "Username", "id": "username"},
                                            {"name": "Email", "id": "email"},
                                        ],
                                        data=show_users(),
                                    ),
                                ],
                                md=12,
                            ),
                        ]
                    ),
                ],
                className="jumbotron",
            ),
        ]
    )
    return layout_main


@callback(
    Output("new_username", "className"),
    [
        Input("createUserButton", "n_clicks"),
        Input("new_username", "n_submit"),
        Input("newPwd1", "n_submit"),
        Input("newPwd2", "n_submit"),
        Input("new_email", "n_submit"),
    ],
    [State("new_username", "value")],
)
def validate_username(
    n_clicks,
    username_submit,
    new_pass1_submit,
    new_pass2_submit,
    new_email_submit,
    new_username,
):
    if (
        (n_clicks > 0)
        or (username_submit > 0)
        or (new_pass1_submit > 0)
        or (new_pass2_submit > 0)
        or (new_email_submit > 0)
    ):
        if new_username is None or new_username == "":
            return "form-control is-invalid"
        else:
            return "form-control is-valid"
    else:
        return "form-control"


@callback(
    Output("newPwd1", "className"),
    [
        Input("createUserButton", "n_clicks"),
        Input("new_username", "n_submit"),
        Input("newPwd1", "n_submit"),
        Input("newPwd2", "n_submit"),
        Input("new_email", "n_submit"),
    ],
    [State("newPwd1", "value"), State("newPwd2", "value")],
)
def validate_pass1(
    n_clicks,
    username_submit,
    new_pass1_submit,
    new_pass2_submit,
    new_email_submit,
    new_pass_1,
    new_pass_2,
):
    if (
        (n_clicks > 0)
        or (username_submit > 0)
        or (new_pass1_submit > 0)
        or (new_pass2_submit > 0)
        or (new_email_submit > 0)
    ):
        if new_pass_1 == new_pass_2 and len(new_pass_1) > 7:
            return "form-control is-valid"
        else:
            return "form-control is-invalid"
    else:
        return "form-control"


@callback(
    Output("newPwd2", "className"),
    [
        Input("createUserButton", "n_clicks"),
        Input("new_username", "n_submit"),
        Input("newPwd1", "n_submit"),
        Input("newPwd2", "n_submit"),
        Input("new_email", "n_submit"),
    ],
    [State("newPwd1", "value"), State("newPwd2", "value")],
)
def validate_pass2(
    n_clicks,
    username_submit,
    new_pass1_submit,
    new_pass2_submit,
    new_email_submit,
    new_pass_1,
    new_pass_2,
):
    if (
        (n_clicks > 0)
        or (username_submit > 0)
        or (new_pass1_submit > 0)
        or (new_pass2_submit > 0)
        or (new_email_submit > 0)
    ):
        if new_pass_1 == new_pass_2 and len(new_pass_2) > 7:
            return "form-control is-valid"
        else:
            return "form-control is-invalid"
    else:
        return "form-control"


@callback(
    Output("new_email", "className"),
    [
        Input("createUserButton", "n_clicks"),
        Input("new_username", "n_submit"),
        Input("newPwd1", "n_submit"),
        Input("newPwd2", "n_submit"),
        Input("new_email", "n_submit"),
    ],
    [State("new_email", "value")],
)
def validate_email(
    n_clicks,
    username_submit,
    new_pass1_submit,
    new_pass2_submit,
    new_email_submit,
    new_email,
):
    if (
        (n_clicks > 0)
        or (username_submit > 0)
        or (new_pass1_submit > 0)
        or (new_pass2_submit > 0)
        or (new_email_submit > 0)
    ):
        if new_email is None or new_email == "":
            return "form-control is-invalid"
        else:
            return "form-control is-valid"
    else:
        return "form-control"


@callback(
    Output("createUserSuccess", "children"),
    [
        Input("createUserButton", "n_clicks"),
        Input("new_username", "n_submit"),
        Input("newPwd1", "n_submit"),
        Input("newPwd2", "n_submit"),
        Input("new_email", "n_submit"),
    ],
    [
        State("page-content", "children"),
        State("new_username", "value"),
        State("newPwd1", "value"),
        State("newPwd2", "value"),
        State("new_email", "value"),
        State("admin", "value"),
    ],
)
def create_user(
    n_clicks,
    username_submit,
    new_pass1_submit,
    new_pass2_submit,
    new_email_submit,
    page_content,
    new_user,
    new_pass_1,
    new_pass_2,
    new_email,
    admin,
):
    if (
        (n_clicks > 0)
        or (username_submit > 0)
        or (new_pass1_submit > 0)
        or (new_pass2_submit > 0)
        or (new_email_submit > 0)
    ):
        if new_user and new_pass_1 and new_pass_2 and new_email != "":
            if new_pass_1 == new_pass_2:
                if len(new_pass_1) > 7:
                    try:
                        add_user(new_user, new_pass_1, new_email, admin)
                        return html.Div(
                            children=["New User created"], className="text-success"
                        )
                    except Exception as e:
                        return html.Div(
                            children=["New User not created: {e}".format(e=e)],
                            className="text-danger",
                        )
                else:
                    return html.Div(
                        children=["New Password Must Be Minimum 8 Characters"],
                        className="text-danger",
                    )
            else:
                return html.Div(
                    children=["Passwords do not match"], className="text-danger"
                )
        else:
            return html.Div(
                children=["Invalid details submitted"], className="text-danger"
            )
