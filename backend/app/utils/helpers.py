"""
Utility functions and helpers for the backend application.

Common utility functions used across the application.
"""

from typing import Any


def calculate_percentage(value: float, total: float) -> float:
    """Calculate percentage with division by zero protection."""
    if total == 0:
        return 0.0
    return round((value / total) * 100, 2)


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers with default value for zero division."""
    if denominator == 0:
        return default
    return numerator / denominator


def format_currency(value: float, currency: str = "£") -> str:
    """Format value as currency string."""
    return f"{currency}{value:.1f}m"


def clean_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Remove None values from dictionary."""
    return {k: v for k, v in data.items() if v is not None}


def chunk_list(lst: list[Any], chunk_size: int) -> list[list[Any]]:
    """Split a list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]