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
        Output("bootstrap-data-store", "data"),
        [Input("url", "pathname")],
        prevent_initial_call=False,
    )
    def load_bootstrap_data(pathname: str) -> Any:
        """Load bootstrap data on page load."""
        print("\n=== BOOTSTRAP CALLBACK TRIGGERED ===")
        print(f"pathname: {pathname}")
        bootstrap_data = api_client.get_bootstrap()
        print(f"Bootstrap data received: {bootstrap_data is not None}")
        if bootstrap_data and 'events' in bootstrap_data:
            print(f"Number of events in bootstrap: {len(bootstrap_data['events'])}")
        return bootstrap_data if bootstrap_data else None

    @app.callback(
        [
            Output("league-data-store", "data"),
            Output("current-league-id-store", "data"),
            Output("gameweek-selector", "options"),
            Output("gameweek-selector", "value"),
            Output("gameweek-selector", "style"),
            Output("league-input-alert", "children"),
            Output("league-input-alert", "color"),
            Output("league-input-alert", "is_open"),
            Output("overview-cards", "style"),
            Output("league-table-card", "style"),
            Output("analytics-section", "style"),
        ],
        [Input("load-league-btn", "n_clicks")],
        [State("league-id-input", "value"), State("bootstrap-data-store", "data")],
        prevent_initial_call=True,
    )
    def load_league_data(n_clicks: int, league_id: int, bootstrap_data: dict) -> tuple[Any, ...]:
        """Load league data when button is clicked."""
        print("\n=== LOAD LEAGUE CALLBACK TRIGGERED ===")
        print(f"n_clicks: {n_clicks}")
        print(f"league_id: {league_id}")
        print(f"bootstrap_data exists: {bootstrap_data is not None}")
        if bootstrap_data:
            print(f"bootstrap_data has events: {'events' in bootstrap_data}")
            if 'events' in bootstrap_data:
                print(f"Number of events: {len(bootstrap_data['events'])}")
        
        # Validate league ID
        if not league_id:
            print("ERROR: No league ID provided")
            return (
                dash.no_update,
                dash.no_update,
                [],
                None,
                {"display": "none"},
                "Please enter a valid league ID.",
                "warning",
                True,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )

        # Get current gameweek from bootstrap data
        if not bootstrap_data or "events" not in bootstrap_data:
            print("ERROR: No bootstrap data or events")
            return (
                dash.no_update,
                dash.no_update,
                [],
                None,
                {"display": "none"},
                "Failed to load game data. Please try again.",
                "danger",
                True,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )

        events = bootstrap_data.get("events", [])
        gameweek_options = [
            {"label": f"GW {event['id']}", "value": event['id']}
            for event in events
        ]
        
        current_gw = next(
            (event['id'] for event in events if event.get('is_current')),
            1
        )
        
        print(f"Current gameweek: {current_gw}")
        print(f"Gameweek options count: {len(gameweek_options)}")

        # Fetch league data for current gameweek
        print(f"Fetching league data for league {league_id}, GW {current_gw}")
        league_data = api_client.get_league_standings(league_id, current_gw)
        print(f"League data received: {league_data is not None}")

        if not league_data:
            print("ERROR: Failed to fetch league data")
            return (
                None,
                dash.no_update,
                [],
                None,
                {"display": "none"},
                f"Failed to load league {league_id}. Please check the league ID and try again.",
                "danger",
                True,
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )

        print(f"SUCCESS: Returning league data with {len(league_data.get('standings', {}).get('results', []))} managers")
        return (
            league_data,
            league_id,
            gameweek_options,
            current_gw,
            {"display": "block", "min-width": "120px"},
            f"Successfully loaded league data for GW {current_gw}!",
            "success",
            True,
            {"display": "block"},
            {"display": "block"},
            {"display": "block"},
        )

    @app.callback(
        Output("league-data-store", "data", allow_duplicate=True),
        [Input("gameweek-selector", "value")],
        [State("current-league-id-store", "data")],
        prevent_initial_call=True,
    )
    def change_gameweek(gameweek: int, league_id: int) -> Any:
        """Update league data when gameweek selector changes."""
        print("\n=== GAMEWEEK CHANGE CALLBACK TRIGGERED ===", flush=True)
        print(f"Selected gameweek: {gameweek}", flush=True)
        print(f"Current league_id: {league_id}", flush=True)
        
        if not league_id or not gameweek:
            print("ERROR: Missing league_id or gameweek")
            return dash.no_update
        
        # Fetch league data for selected gameweek
        print(f"Fetching league data for league {league_id}, GW {gameweek}")
        league_data = api_client.get_league_standings(league_id, gameweek)
        print(f"League data received: {league_data is not None}")
        
        if league_data:
            print(f"Returning data with {len(league_data.get('standings', {}).get('results', []))} managers")
        
        return league_data if league_data else dash.no_update

    @app.callback(
        [
            Output("total-managers", "children"),
            Output("average-points", "children"),
            Output("highest-points", "children"),
            Output("current-gameweek", "children"),
        ],
        [Input("league-data-store", "data"), Input("gameweek-selector", "value")],
    )
    def update_overview_cards(league_data: dict[str, Any], selected_gw: int) -> tuple[str, ...]:
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

            # Show selected gameweek
            current_gw = f"GW {selected_gw}" if selected_gw else "—"

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
        print("\n=== UPDATE TABLE CALLBACK TRIGGERED ===", flush=True)
        print(f"league_data exists: {league_data is not None}", flush=True)
        if league_data:
            print(f"Number of managers in data: {len(league_data.get('standings', {}).get('results', []))}", flush=True)
        
        if not league_data:
            print("No league data, returning 'No data available'", flush=True)
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
                "player_name": "Manager",
                "event_total": "GW Points",
                "total": "Total Points",
            }

            # Filter and rename columns
            df_display = df[list(display_columns.keys())].copy()
            df_display.columns = list(display_columns.values())
            
            # Log sample data for debugging
            print(f"Table data - First row: Rank={df_display.iloc[0]['Rank']}, GW Points={df_display.iloc[0]['GW Points']}", flush=True)
            print(f"Table has {len(df_display)} rows", flush=True)

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