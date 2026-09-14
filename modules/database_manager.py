# ==================================================
# import
# ==================================================
import sqlite3
from pathlib import Path
import pandas as pd
import logging

# ==========================
# logger
# ==========================
logger = logging.getLogger(__name__)


# ==================================================
# save_dataframe_to_sqlite
# ==================================================
def save_dataframe_to_sqlite(
    db_path: Path,
    df: pd.DataFrame,
    table_name: str,
) -> None:

    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)

    try:
        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False,
        )

        logger.info(f"データベース保存完了 保存先: {db_path} テーブル名: {table_name}")

    except Exception as e:
        raise RuntimeError("データベースの保存に失敗しました") from e

    finally:
        conn.close()


# ==================================================
# load_dataframe_from_sql
# ==================================================
def load_dataframe_from_sql(db_path: Path, sql_query: str) -> pd.DataFrame:

    conn = sqlite3.connect(db_path)

    try:
        df = pd.read_sql(
            sql_query,
            conn,
        )

        return df

    except Exception as e:
        raise RuntimeError("データベースの読み取りに失敗しました") from e

    finally:
        conn.close()
