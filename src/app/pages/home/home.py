from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path="/", title="Dashboard - Home")


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
                                    [
                                        dbc.CardBody(
                                            [
                                                dbc.Carousel(
                                                    items=[
                                                        {
                                                            "key": "1",
                                                            "src": "/assets/img/home_slideshow_market_1.jpg",
                                                            "header": "MARKET REVIEW",
                                                        },
                                                        {
                                                            "key": "2",
                                                            "src": "/assets/img/home_slideshow_ships_1.jpg",
                                                            "header": "SHIPS REVIEW",
                                                        },
                                                        {
                                                            "key": "3",
                                                            "src": "/assets/img/home_slideshow_market_2.png",
                                                            "header": "MARKET REVIEW",
                                                        },
                                                        {
                                                            "key": "4",
                                                            "src": "/assets/img/home_slideshow_ships_2.jpg",
                                                            "header": "SHIPS REVIEW",
                                                        },
                                                    ],
                                                    controls=True,
                                                    indicators=True,
                                                    variant="dark",
                                                    interval=1500,
                                                )
                                            ]
                                        )
                                    ],
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
                                                            "ab@student.uni-lj.si",  # need to update
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
        "background-image": 'url("/assets/img/background.png")',
        "background-size": "cover",
        "background-color": "#fcfcfc",
    },
)
