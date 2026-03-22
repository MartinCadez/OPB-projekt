import logging
from dash import html, register_page


logger = logging.getLogger("app." + __name__)
register_page(__name__, path="/logout", name="Logout", title="Dashboard - Logout")

# TODO: add logout layout
layout = html.Div()
