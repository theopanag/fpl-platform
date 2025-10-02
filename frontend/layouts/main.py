"""
Main layout components and structures.

Common layout patterns and page structures.
"""

import dash_bootstrap_components as dbc
from dash import html


def create_page_header(title: str, subtitle: str = "") -> html.Div:
    """Create a standard page header."""
    header_content = [html.H1(title, className="mb-2")]

    if subtitle:
        header_content.append(
            html.P(subtitle, className="lead text-muted")
        )

    return html.Div(header_content, className="mb-4")


def create_main_layout(content: html.Div, title: str = "", subtitle: str = "") -> html.Div:
    """Create main page layout wrapper."""
    layout_components = []

    if title:
        layout_components.append(create_page_header(title, subtitle))

    layout_components.append(content)

    return html.Div(layout_components)


def create_error_message(title: str, message: str, show_home_link: bool = True) -> html.Div:
    """Create a standardized error message component."""
    components = [
        html.H3(title, className="text-danger mb-3"),
        html.P(message, className="mb-4")
    ]

    if show_home_link:
        components.append(
            dbc.Button(
                "Go to Dashboard",
                href="/",
                external_link=True,
                color="primary"
            )
        )

    return dbc.Alert(components, color="light", className="text-center p-5")


def create_loading_placeholder(text: str = "Loading...") -> html.Div:
    """Create a loading placeholder component."""
    return html.Div([
        dbc.Spinner(html.Div(id="loading-content"), size="lg"),
        html.P(text, className="text-center mt-3 text-muted")
    ], className="text-center py-5")


def create_card_grid(cards: list[dbc.Card], cols_per_row: int = 3) -> html.Div:
    """Create a responsive grid of cards."""
    if cols_per_row == 2:
        col_size = 6
    elif cols_per_row == 3:
        col_size = 4
    elif cols_per_row == 4:
        col_size = 3
    else:
        col_size = 12

    rows = []
    for i in range(0, len(cards), cols_per_row):
        row_cards = cards[i:i + cols_per_row]
        cols = [dbc.Col(card, md=col_size, className="mb-4") for card in row_cards]
        rows.append(dbc.Row(cols))

    return html.Div(rows)