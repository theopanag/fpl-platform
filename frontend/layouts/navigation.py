"""
Navigation components for the application.

Creates the main navigation bar and routing elements.
"""

import dash_bootstrap_components as dbc
from dash import dcc, html


def create_navbar() -> dbc.Navbar:
    """Create the main navigation bar."""
    return dbc.Navbar(
        dbc.Container([
            # Brand/Logo
            dbc.Row([
                dbc.Col([
                    html.A(
                        dbc.Row([
                            dbc.Col(html.I(className="fas fa-futbol fa-lg")),
                            dbc.Col(dbc.NavbarBrand("FPL Analytics", className="ms-2")),
                        ], align="center", className="g-0"),
                        href="/",
                        style={"textDecoration": "none"}
                    )
                ], width="auto"),
            ]),

            # Navigation items
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Dashboard", href="/", id="nav-dashboard")),
                    dbc.NavItem(dbc.NavLink("Leagues", href="/leagues", id="nav-leagues")),
                    dbc.NavItem(dbc.NavLink("Managers", href="/managers", id="nav-managers")),
                    dbc.NavItem(dbc.NavLink("Comparison", href="/comparison", id="nav-comparison")),
                ], className="ms-auto", navbar=True),
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ], fluid=True),
        color="primary",
        dark=True,
        sticky="top",
    )


def create_breadcrumb(items: list[dict[str, str]]) -> dbc.Breadcrumb:
    """Create breadcrumb navigation."""
    breadcrumb_items = [
        dbc.BreadcrumbItem(item["text"], href=item.get("href"), active=item.get("active", False))
        for item in items
    ]
    return dbc.Breadcrumb(breadcrumb_items, className="mb-3")


def create_sidebar() -> html.Div:
    """Create sidebar navigation (for future use)."""
    return html.Div([
        html.H5("Quick Links", className="mb-3"),
        dbc.Nav([
            dbc.NavLink("League Overview", href="/", active="exact"),
            dbc.NavLink("Manager Analysis", href="/managers", active="exact"),
            dbc.NavLink("Transfer Trends", href="/transfers", active="exact"),
            dbc.NavLink("Captaincy Stats", href="/captaincy", active="exact"),
        ], vertical=True, pills=True),
    ], className="p-3 border-end", style={"minHeight": "100vh"})