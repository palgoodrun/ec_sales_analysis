# ==================================================
# import
# ==================================================
import pandas as pd

# --------------------------
# from_modules
# --------------------------
from modules.dataframe_formatter import format_kpi_columns
from modules.kpi_calculator import add_kpis_to_dataframe


# ==================================================
# aggregate_orders
# ==================================================
def aggregate_orders(df: pd.DataFrame, group_keys: list[str]) -> pd.DataFrame:

    if df.empty:
        summary = format_kpi_columns(df, group_keys)

        return summary

    summary = (
        df.groupby(group_keys)
        .agg(
            order_count=("order_id", "size"),
            cancelled_order_count=("is_cancelled", "sum"),
            total_quantity=("quantity", "sum"),
            total_sales=("sales_amount", "sum"),
        )
        .reset_index()
    )

    summary = add_kpis_to_dataframe(summary)

    summary = summary.sort_values(group_keys, ascending=True)

    summary = format_kpi_columns(summary, group_keys)

    return summary
