# IMPORTANT: IF you have additional modules inside your directory, use RELATIVE IMPORTING!

from dash import html

# IMPORT CACHING

# DEFINE TIMOUT FOR CACHING
TIMEOUT = 1800


# FUNCTIONS
# ------------------------------------------------------------------------------


# LAYOUT
# ------------------------------------------------------------------------------
def generate_tab():
    tab = html.Div("THIS IS TAB 1")
    return tab


# CALLBACKS
# ------------------------------------------------------------------------------
