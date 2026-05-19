from pathlib import Path

from nicegui import ui

from analytics import compute_kpis, monthly_revenue_by_category, top_salespeople
from data_loader import load_sales_data
from ui_components import (
	render_kpis,
	render_monthly_line_chart,
	render_monthly_stacked_chart,
	render_top_salespeople_table,
)


def build_dashboard() -> None:
	data_path = Path(__file__).resolve().parent / "sales_data.csv"
	df = load_sales_data(data_path)

	kpis = compute_kpis(df)
	monthly_pivot = monthly_revenue_by_category(df)
	top_10 = top_salespeople(df, n=10)

	ui.page_title("Sales Dashboard")

	with ui.column().classes("w-full max-w-[1400px] mx-auto p-6 gap-6"):
		ui.label("Sales Dashboard").classes("text-3xl font-bold")
		ui.label("Monthly revenue by category and top salespeople performance.").classes("text-gray-600")

		render_kpis(kpis)
		render_monthly_stacked_chart(monthly_pivot)
		render_monthly_line_chart(monthly_pivot)
		render_top_salespeople_table(top_10)


def main() -> None:
	build_dashboard()
	ui.run(title="Sales Dashboard")


if __name__ in {"__main__", "__mp_main__"}:
	main()
