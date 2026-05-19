from pathlib import Path

import pandas as pd


def load_sales_data(csv_path: Path) -> pd.DataFrame:
    """Load and normalize sales data for dashboard usage."""
    df = pd.read_csv(csv_path)

    required_columns = {"sales_person", "product", "category", "price", "date"}
    missing = required_columns.difference(df.columns)
    if missing:
        missing_str = ", ".join(sorted(missing))
        raise ValueError(f"Missing required columns: {missing_str}")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    if df["date"].isna().any() or df["price"].isna().any():
        raise ValueError("Input data contains invalid date or price values.")

    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df
