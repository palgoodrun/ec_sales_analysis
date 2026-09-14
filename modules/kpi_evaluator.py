# ==================================================
# import
# ==================================================
import pandas as pd
import logging

# --------------------------
# logger
# --------------------------
logger = logging.getLogger(__name__)


# ==================================================
# evaluate_cancellation_rate
# ==================================================
def evaluate_cancellation_rate(df: pd.DataFrame, threshold: float) -> pd.DataFrame:

    df = df.copy()

    mask = df["cancellation_rate"] >= threshold

    df["cancellation_rate_status"] = "normal"

    df.loc[mask, "cancellation_rate_status"] = "warning"

    return df


# ==================================================
# evaluate_all_cancellation_rates
# ==================================================
def evaluate_all_cancellation_rates(
    key_df_pairs: dict[str, pd.DataFrame], threshold: float
) -> dict[str, pd.DataFrame]:

    logger.info(
        f"KPI「キャンセル率」評価完了 処理データフレーム数: {len(key_df_pairs)}"
    )

    return {
        key: evaluate_cancellation_rate(df, threshold)
        for key, df in key_df_pairs.items()
    }
