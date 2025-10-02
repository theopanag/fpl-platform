"""
Dashboard callbacks for interactive functionality.

Handles user interactions and updates dashboard components.
"""

from typing import Any

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dash_table, html
from dash.dependencies import Input, Output, State

from utils.api_client import APIClient


def register_dashboard_callbacks(app: dash.Dash, api_client: APIClient) -> None:
    """Register all dashboard-related callbacks."""

    @app.callback(
        [
            Output("league-data-store", "data"),
            Output("league-input-alert", "children"),
            Output("league-input-alert", "color"),
            Output("league-input-alert", "is_open"),
            Output("overview-cards", "style"),
            Output("league-table-card", "style"),
            Output("analytics-section", "style"),
        ],
        [Input("load-league-btn", "n_clicks")],
        [State("league-id-input", "value")],
        prevent_initial_call=True,
    )
    def load_league_data(n_clicks: int, league_id: int) -> tuple[Any, ...]:
        """Load league data when button is clicked."""
        if not league_id:
            return (
                None,
                "Please enter a valid league ID.",
                "warning",
                True,
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )

        # Fetch league data
        league_data = api_client.get_league_standings(league_id)

        if not league_data:
            return (
                None,
                f"Failed to load league {league_id}. Please check the league ID and try again.",
                "danger",
                True,
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )

        return (
            league_data,
            f"Successfully loaded league data!",
            "success",
            True,
            {"display": "block"},
            {"display": "block"},
            {"display": "block"},
        )

    @app.callback(
        [
            Output("total-managers", "children"),
            Output("average-points", "children"),
            Output("highest-points", "children"),
            Output("current-gameweek", "children"),
        ],
        [Input("league-data-store", "data")],
    )
    def update_overview_cards(league_data: dict[str, Any]) -> tuple[str, ...]:
        """Update overview cards with league statistics."""
        if not league_data:
            return "—", "—", "—", "—"

        try:
            standings = league_data.get("standings", {}).get("results", [])

            if not standings:
                return "0", "—", "—", "—"

            total_managers = len(standings)
            points_list = [entry.get("event_total", 0) for entry in standings]
            avg_points = sum(points_list) / len(points_list) if points_list else 0
            highest_points = max(points_list) if points_list else 0

            # Get current gameweek from first entry (assuming all are from same GW)
            current_gw = "—"
            if standings:
                # This would need to be fetched from bootstrap data in a real implementation
                current_gw = "GW 1"  # Placeholder

            return (
                str(total_managers),
                f"{avg_points:.1f}",
                str(highest_points),
                current_gw,
            )

        except Exception:
            return "—", "—", "—", "—"

    @app.callback(
        Output("league-standings-table", "children"),
        [Input("league-data-store", "data")],
    )
    def update_league_table(league_data: dict[str, Any]) -> Any:
        """Update league standings table."""
        if not league_data:
            return html.Div("No data available")

        try:
            standings = league_data.get("standings", {}).get("results", [])

            if not standings:
                return html.Div("No standings data available")

            # Convert to DataFrame for easier handling
            df = pd.DataFrame(standings)

            # Select and rename columns for display
            display_columns = {
                "rank": "Rank",
                "entry_name": "Team Name",
                "player_first_name": "First Name",
                "player_last_name": "Last Name",
                "event_total": "GW Points",
                "total": "Total Points",
            }

            # Filter and rename columns
            df_display = df[list(display_columns.keys())].copy()
            df_display.columns = list(display_columns.values())

            # Create Dash table
            return dash_table.DataTable(
                data=df_display.to_dict("records"),
                columns=[{"name": col, "id": col} for col in df_display.columns],
                style_cell={"textAlign": "left", "padding": "10px"},
                style_header={"backgroundColor": "#f8f9fa", "fontWeight": "bold"},
                style_data={"backgroundColor": "white"},
                style_data_conditional=[
                    {
                        "if": {"row_index": 0},
                        "backgroundColor": "#d4edda",
                        "color": "black",
                    }
                ],
                sort_action="native",
                page_size=20,
            )

        except Exception as e:
            return html.Div(f"Error loading table: {str(e)}")

    @app.callback(
        [
            Output("points-trend-chart", "figure"),
            Output("rank-distribution-chart", "figure"),
            Output("transfer-analysis-chart", "figure"),
        ],
        [Input("league-data-store", "data")],
    )
    def update_analytics_charts(league_data: dict[str, Any]) -> tuple[Any, ...]:
        """Update analytics charts."""
        if not league_data:
            empty_fig = go.Figure().add_annotation(
                text="No data available", xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return empty_fig, empty_fig, empty_fig

        try:
            standings = league_data.get("standings", {}).get("results", [])

            if not standings:
                empty_fig = go.Figure().add_annotation(
                    text="No data available", xref="paper", yref="paper",
                    x=0.5, y=0.5, showarrow=False
                )
                return empty_fig, empty_fig, empty_fig

            df = pd.DataFrame(standings)

            # Points trend chart (placeholder - would need historical data)
            points_fig = px.line(
                title="Points Trend Over Time (Placeholder)",
                labels={"x": "Gameweek", "y": "Points"}
            )
            points_fig.add_annotation(
                text="Historical data needed", xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )

            # Rank distribution
            rank_fig = px.histogram(
                df, x="event_total", nbins=20,
                title="Points Distribution (Current Gameweek)",
                labels={"event_total": "Points", "count": "Number of Managers"}
            )

            # Transfer analysis (placeholder)
            transfer_fig = px.bar(
                title="Transfer Analysis (Placeholder)",
                labels={"x": "Player", "y": "Transfers"}
            )
            transfer_fig.add_annotation(
                text="Transfer data needed", xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )

            return points_fig, rank_fig, transfer_fig

        except Exception as e:
            error_fig = go.Figure().add_annotation(
                text=f"Error: {str(e)}", xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return error_fig, error_fig, error_fig