import pandas as pd


def compute_kpis(df: pd.DataFrame) -> dict[str, str]:
    return {
        "Total Revenue": f"${df['price'].sum():,.2f}",
        "Transactions": f"{len(df):,}",
        "Date Range": f"{df['date'].min().date()} → {df['date'].max().date()}",
    }


def monthly_revenue_by_category(df: pd.DataFrame) -> pd.DataFrame:
    pivot = (
        df.pivot_table(index="month", columns="category", values="price", aggfunc="sum", fill_value=0)
        .sort_index()
        .round(2)
    )
    return pivot


def top_salespeople(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    top = (
        df.groupby("sales_person", as_index=False)
        .agg(
            transactions=("price", "count"),
            revenue=("price", "sum"),
            avg_sale=("price", "mean"),
        )
        .sort_values("revenue", ascending=True)
        .head(n)
    )
    top["revenue"] = top["revenue"].round(2)
    top["avg_sale"] = top["avg_sale"].round(2)
    return top
