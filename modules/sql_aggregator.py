# ==================================================
# import
# ==================================================
import pandas as pd
from pathlib import Path
import logging

# --------------------------
# logger
# --------------------------
logger = logging.getLogger(__name__)

# --------------------------
# from_modules
# --------------------------
from modules import sql_queries
from modules.database_manager import load_dataframe_from_sql
from modules.kpi_calculator import add_kpis_to_dataframe
from modules.dataframe_formatter import format_kpi_columns


# ==================================================
# build_kpi_dataframe
# ==================================================
def build_kpi_dataframe(
    sql_query_name: str,
    db_path: Path,
    keys: list[str],
) -> pd.DataFrame:

    # ==========================
    # SQL読み込み
    # ==========================
    sql_query = getattr(sql_queries, sql_query_name)

    try:

        kpi_df = load_dataframe_from_sql(db_path, sql_query)

    except Exception as e:
        logger.error(f"SQLクエリの読み込みに失敗しました SQLクエリ名: {sql_query_name}")
        raise

    # ==========================
    # KPI追加
    # ==========================

    kpi_df = add_kpis_to_dataframe(kpi_df)

    # ==========================
    # 指定列順へ並び替え
    # ==========================

    kpi_df = format_kpi_columns(kpi_df, keys)

    logger.info(f"{' & '.join(keys)} 集計完了")

    return kpi_df
