# ==================================================
# import
# ==================================================
import pandas as pd
import numpy as np


# ==================================================
# add_kpis_to_dataframe
# ==================================================
def add_kpis_to_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    df_added_kpi = df.copy()

    df_added_kpi["completed_order_count"] = (
        df_added_kpi["order_count"] - df_added_kpi["cancelled_order_count"]
    )

    df_added_kpi["avg_order_value"] = np.where(
        df_added_kpi["completed_order_count"] != 0,
        df_added_kpi["total_sales"] / df_added_kpi["completed_order_count"],
        0,
    ).round(1)

    df_added_kpi["cancellation_rate"] = np.where(
        df_added_kpi["order_count"] != 0,
        df_added_kpi["cancelled_order_count"] / df_added_kpi["order_count"] * 100,
        0,
    ).round(1)

    return df_added_kpi
