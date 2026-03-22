from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path="/", title="Dashboard - Home")

carousel = dbc.Carousel(
    items=[
        {"key": "1", "src": "./assets/prikaz_1.png", "header": "MARKET REVIEW"},
        {"key": "2", "src": "./assets/prikaz_2.png", "header": "SHIPS DATA REVIEW"},
    ],
    controls=True,
    indicators=True,
    variant="dark",
    interval=1500,
)


def generate_contributor_card(name, team, email):
    card = dbc.Col(
        [
            dbc.Card(
                [
                    dbc.CardHeader(name),
                    dbc.CardBody(
                        [
                            html.P(team),
                            html.A(
                                html.Span(
                                    [html.I(className="fas fa-envelope"), " ", email]
                                ),
                                href=f"mailto:{email}",
                            ),
                        ],
                        style={"background-color": "#fcfcfc"},
                    ),
                ],
                color="#757e71",
            )
        ]
    )

    return card


layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Br(),
                                dbc.Card(
                                    [dbc.CardBody([carousel])],
                                    color="light",
                                    inverse=True,
                                ),
                                html.Br(),
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.H5("HELP & SUPPORT")),
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        generate_contributor_card(
                                                            "Martin Čadež",
                                                            "Student at the Faculty of Mathematics and Physics",
                                                            "mc18257@student.uni-lj.si",
                                                        ),
                                                        generate_contributor_card(
                                                            "Amanda Babič",
                                                            "Student at the Faculty of Mathematics and Physics",
                                                            "ab@student.uni-lj.si",  # Need to update
                                                        ),
                                                    ]
                                                )
                                            ]
                                        ),
                                    ],
                                    color="light",
                                    className="card text-center",
                                ),
                            ],
                            width=12,
                        )
                    ],
                    justify="center",
                ),
            ]
        )
    ],
    style={
        "background-image": 'url("assets/background.png")',
        "background-size": "cover",
        "background-color": "#fcfcfc",
    },
)
