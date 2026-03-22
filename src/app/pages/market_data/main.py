import logging

from dash import html, callback
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
from dash import register_page

from .tabs import tab_1, tab_2


NAME = "CRYPTO MARKET DATA"
GROUP = "MARKET DATA"
AUTH = False

logger = logging.getLogger("app." + __name__)


register_page(
    __name__,
    path=f"/{NAME.lower().replace(' ', '_')}",
    name=NAME,
    group=GROUP,
    auth=AUTH,
    title=f"Dashboard - {NAME}",
)


def layout():
    return html.Div(
        [
            html.Div(
                [
                    dbc.Tabs(
                        id="market_data_tabs",
                        active_tab="tab_1",
                        children=[
                            dbc.Tab(
                                label="TAB 1 name update",
                                tab_id="tab_1",
                                tabClassName="flex-grow-1 text-center",
                            ),
                            dbc.Tab(
                                label="TAB 2 name update",
                                tab_id="tab_2",
                                tabClassName="flex-grow-1 text-center",
                            ),
                        ],
                    ),
                    html.Div(id="market_data_content", style={"width": "100%"}),
                ]
            )
        ]
    )


@callback(
    Output("market_data_content", "children"), [Input("market_data_tabs", "active_tab")]
)
def render_content(tab):
    if tab == "tab_1":
        return tab_1.generate_tab()
    elif tab == "tab_2":
        return tab_2.generate_tab()
    else:
        return "404"
