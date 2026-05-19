from typing import Any

import pandas as pd
from nicegui import ui


def render_kpis(kpis: dict[str, str]) -> None:
    with ui.row().classes("w-full gap-4"):
        for title, value in kpis.items():
            with ui.card().classes("min-w-[230px] flex-1"):
                ui.label(title).classes("text-sm text-gray-600")
                ui.label(value).classes("text-2xl font-bold")


def _series_from_pivot(pivot_df: pd.DataFrame) -> list[dict[str, Any]]:
    series = []
    for category in pivot_df.columns:
        series.append(
            {
                "name": str(category),
                "type": "bar",
                "stack": "total",
                "emphasis": {"focus": "series"},
                "data": pivot_df[category].round(2).tolist(),
            }
        )
    return series


def render_monthly_stacked_chart(pivot_df: pd.DataFrame) -> None:
    options = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {"top": 0},
        "grid": {
            "left": "3%",
            "right": "4%",
            "top": 56,
            "bottom": "3%",
            "containLabel": True,
        },
        "xAxis": {"type": "category", "data": pivot_df.index.tolist()},
        "yAxis": {"type": "value", "name": "Revenue"},
        "series": _series_from_pivot(pivot_df),
    }
    with ui.column().classes("w-full gap-2"):
        ui.label("Monthly Revenue by Category (Stacked)").classes("text-2xl font-semibold")
        ui.echart(options).classes("w-full h-96")


def render_monthly_line_chart(pivot_df: pd.DataFrame) -> None:
    series = []
    for category in pivot_df.columns:
        series.append(
            {
                "name": str(category),
                "type": "line",
                "smooth": True,
                "data": pivot_df[category].round(2).tolist(),
            }
        )

    options = {
        "tooltip": {"trigger": "axis"},
        "legend": {"top": 0},
        "grid": {
            "left": "3%",
            "right": "4%",
            "top": 56,
            "bottom": "3%",
            "containLabel": True,
        },
        "xAxis": {"type": "category", "data": pivot_df.index.tolist()},
        "yAxis": {"type": "value", "name": "Revenue"},
        "series": series,
    }
    with ui.column().classes("w-full gap-2"):
        ui.label("Monthly Revenue by Category (Trend)").classes("text-2xl font-semibold")
        ui.echart(options).classes("w-full h-96")


def render_top_salespeople_table(top_df: pd.DataFrame) -> None:
    ui.label("Top 10 Salespeople by Revenue").classes("text-xl font-semibold mt-4")
    rows = top_df.to_dict("records")
    columns = [
        {"name": "sales_person", "label": "Salesperson", "field": "sales_person", "align": "left"},
        {"name": "transactions", "label": "Transactions", "field": "transactions", "align": "right"},
        {"name": "revenue", "label": "Revenue", "field": "revenue", "align": "right"},
        {"name": "avg_sale", "label": "Avg Sale", "field": "avg_sale", "align": "right"},
    ]
    ui.table(columns=columns, rows=rows, row_key="sales_person").classes("w-full")
