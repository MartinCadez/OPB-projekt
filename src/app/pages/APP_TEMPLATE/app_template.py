import logging

from dash import html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from auth.authentication import authentication

from .tabs import tab1, tab2

logger = logging.getLogger("app." + __name__)

NAME = "Template App"
GROUP = "TEMPLATE GROUP"
AUTH = False


@authentication(app_name=NAME, auth=AUTH)
def layout():
    layout_main = html.Div(
        [
            html.Div(
                [
                    dbc.Tabs(
                        [
                            dbc.Tab(
                                label="Tab 1",
                                tab_id="app-template-tab1-tab",
                                tabClassName="flex-grow-1 text-center",
                            ),
                            dbc.Tab(
                                label="Tab 2",
                                tab_id="app-template-tab2-tab",
                                tabClassName="flex-grow-1 text-center",
                            ),
                        ],
                        id="app-template-tabs",
                        active_tab="app-template-tab1-tab",
                    ),
                ]
            ),
            html.Div(id="app-template-tabs-content", style={"width": "100%"}),
        ]
    )

    return layout_main


@callback(
    Output("app-template-tabs-content", "children"),
    [Input("app-template-tabs", "active_tab")],
)
def render_tabs_content(tab):
    if tab == "app-template-tab1-tab":
        return tab1.generate_tab()
    elif tab == "app-template-tab2-tab":
        return tab2.generate_tab()
    else:
        return "404"
