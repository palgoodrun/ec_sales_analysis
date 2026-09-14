# ==================================================
# import
# ==================================================
import pandas as pd


# ==================================================
# format_kpi_columns
# ==================================================
def format_kpi_columns(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:

    ordered_columns = keys + [
        "order_count",
        "completed_order_count",
        "cancelled_order_count",
        "total_quantity",
        "total_sales",
        "avg_order_value",
        "cancellation_rate",
    ]

    if df.empty:
        return pd.DataFrame(columns=ordered_columns)

    formatted_df = df[ordered_columns]

    return formatted_df
