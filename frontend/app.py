"""
FPL Analytics Platform Frontend

Dash application providing interactive web dashboard for FPL analytics.
"""

import os
from typing import Any

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dotenv import load_dotenv

from components.dashboard import create_dashboard_layout
from layouts.main import create_main_layout
from layouts.navigation import create_navbar
from utils.api_client import APIClient

# Load environment variables
load_dotenv()

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
        "assets/style.css"
    ],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0"
        }
    ],
    title="FPL Analytics Platform",
    suppress_callback_exceptions=True,
)

# Server for deployment
server = app.server

# Initialize API client
api_client = APIClient(
    base_url=os.getenv("BACKEND_URL", "http://localhost:8000")
)

# App layout
app.layout = dbc.Container([
    # Store components for sharing data between callbacks
    dcc.Store(id="league-data-store"),
    dcc.Store(id="manager-data-store"),
    dcc.Store(id="analytics-data-store"),
    dcc.Store(id="bootstrap-data-store"),
    dcc.Store(id="current-league-id-store"),

    # Navigation bar
    create_navbar(),

    # Main content area
    html.Div(id="main-content", className="mt-4"),

    # URL location component for routing
    dcc.Location(id="url", refresh=False),

], fluid=True, className="px-0")


# Import callbacks after layout definition to avoid circular imports
from callbacks.dashboard import register_dashboard_callbacks

# Register all callbacks
register_dashboard_callbacks(app, api_client)


@app.callback(
    dash.dependencies.Output("main-content", "children"),
    [dash.dependencies.Input("url", "pathname")]
)
def display_page(pathname: str) -> Any:
    """Route pages based on URL pathname."""
    if pathname == "/" or pathname == "/dashboard":
        return create_dashboard_layout()
    elif pathname == "/leagues":
        return html.Div([
            html.H2("League Analytics", className="mb-4"),
            html.P("League analytics page coming soon...")
        ])
    elif pathname == "/managers":
        return html.Div([
            html.H2("Manager Analysis", className="mb-4"),
            html.P("Manager analysis page coming soon...")
        ])
    elif pathname == "/comparison":
        return html.Div([
            html.H2("Head-to-Head Comparison", className="mb-4"),
            html.P("Manager comparison page coming soon...")
        ])
    else:
        return html.Div([
            html.H2("404 - Page Not Found", className="text-center mt-5"),
            html.P("The page you're looking for doesn't exist.", className="text-center"),
            dcc.Link("Go back to dashboard", href="/", className="btn btn-primary")
        ])


if __name__ == "__main__":
    debug_mode = os.getenv("DEBUG", "False").lower() == "true"
    app.run_server(
        host="0.0.0.0",
        port=8050,
        debug=debug_mode
    )