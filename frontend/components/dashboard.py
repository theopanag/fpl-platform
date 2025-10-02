"""
Dashboard components for the main overview page.

Creates the dashboard layout with league input and overview cards.
"""

import dash_bootstrap_components as dbc
from dash import dcc, html


def create_league_input_section() -> dbc.Card:
    """Create league input section."""
    return dbc.Card([
        dbc.CardBody([
            html.H5("Enter League Information", className="card-title"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("League ID:", html_for="league-id-input"),
                    dbc.Input(
                        id="league-id-input",
                        type="number",
                        placeholder="Enter your FPL league ID",
                        className="mb-3"
                    ),
                ], md=8),
                dbc.Col([
                    dbc.Label("Action:", html_for="load-league-btn"),
                    html.Br(),
                    dbc.Button(
                        "Load League",
                        id="load-league-btn",
                        color="primary",
                        className="w-100"
                    ),
                ], md=4),
            ]),
            dbc.Alert(
                id="league-input-alert",
                is_open=False,
                dismissable=True,
                className="mt-3"
            ),
        ])
    ], className="mb-4")


def create_overview_cards() -> html.Div:
    """Create overview cards for league statistics."""
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id="total-managers", className="text-primary"),
                        html.P("Total Managers", className="card-text"),
                    ])
                ])
            ], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id="average-points", className="text-success"),
                        html.P("Average Points (GW)", className="card-text"),
                    ])
                ])
            ], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id="highest-points", className="text-warning"),
                        html.P("Highest Points (GW)", className="card-text"),
                    ])
                ])
            ], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id="current-gameweek", className="text-info"),
                        html.P("Current Gameweek", className="card-text"),
                    ])
                ])
            ], md=3),
        ], className="mb-4"),
    ], id="overview-cards", style={"display": "none"})


def create_league_table() -> dbc.Card:
    """Create league standings table."""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("League Standings", className="mb-0")
        ]),
        dbc.CardBody([
            html.Div(id="league-standings-table")
        ])
    ], id="league-table-card", style={"display": "none"})


def create_analytics_section() -> dbc.Card:
    """Create analytics charts section."""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("League Analytics", className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="points-trend-chart")
                ], md=6),
                dbc.Col([
                    dcc.Graph(id="rank-distribution-chart")
                ], md=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="transfer-analysis-chart")
                ], md=12),
            ], className="mt-3"),
        ])
    ], id="analytics-section", style={"display": "none"})


def create_dashboard_layout() -> html.Div:
    """Create the main dashboard layout."""
    return html.Div([
        html.H1("FPL Analytics Dashboard", className="mb-4 text-center"),
        html.P(
            "Enter your FPL league ID to get started with detailed analytics and insights.",
            className="text-center text-muted mb-4"
        ),

        # League input section
        create_league_input_section(),

        # Overview cards
        create_overview_cards(),

        # League standings table
        create_league_table(),

        # Analytics charts
        create_analytics_section(),

        # Loading spinner
        dcc.Loading(
            id="loading-spinner",
            type="default",
            children=html.Div(id="loading-output")
        ),
    ])