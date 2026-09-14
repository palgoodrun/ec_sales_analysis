# ==================================================
# import
# ==================================================
import pandas as pd

# --------------------------
# from_modules
# --------------------------
from modules.database_manager import save_dataframe_to_sqlite
from modules.pandas_aggregator import aggregate_orders
from modules.sql_aggregator import build_kpi_dataframe

# ==================================================
# testデータ
# ==================================================
test_raw_df = pd.DataFrame(
    {
        "order_id": ["O0001", "O0002", "O0003", "O0004", "O0005", "O0006"],
        "order_date": [
            "2026-01-05",
            "2026-01-05",
            "2026-02-05",
            "2026-02-05",
            "2026-02-05",
            "2026-02-05",
        ],
        "customer_id": ["C001", "C002", "C003", "C004", "C005", "C006"],
        "category": [
            "Water Server",
            "Cosmetics",
            "Water Server",
            "Food",
            "Food",
            "Cosmetics",
        ],
        "sales_channel": ["EC", "Amazon", "Rakuten", "EC", "Rakuten", "EC"],
        "region": ["East", "West", "East", "Central", "West", "East"],
        "quantity": [1, 2, 1, 3, 1, 1],
        "sales_amount": [4000, 5000, 4000, 2000, 3000, 6000],
        "is_cancelled": [0, 0, 1, 0, 1, 1],
    }
)


# ==================================================
# pytest
# ==================================================
# --------------------------
# カテゴリー別
# --------------------------
def test_summary_by_category(tmp_path):

    # ==================================================
    # pandas版DF
    # ==================================================
    summary_by_category_from_pandas = aggregate_orders(test_raw_df, ["category"])

    # NOTE
    # テスト失敗確認用 値変更
    #
    # summary_by_category_from_pandas.loc[
    #     summary_by_category_from_pandas["category"] == "Food", "order_count"
    # ] = 100

    print(summary_by_category_from_pandas)

    # ==================================================
    # SQL版DF
    # ==================================================
    # --------------------------
    # database用フォルダ作成
    # --------------------------
    db_path = tmp_path / "test.db"

    # --------------------------
    # database保存
    # --------------------------
    save_dataframe_to_sqlite(db_path, test_raw_df, "test")

    # --------------------------
    # データフレーム作成
    # --------------------------

    summary_by_category_from_sql = build_kpi_dataframe(
        "sql_by_category_for_test", db_path, ["category"]
    )

    print(summary_by_category_from_sql)

    pd.testing.assert_frame_equal(
        summary_by_category_from_pandas, summary_by_category_from_sql
    )


# --------------------------
# 販売チャンネル別
# --------------------------
def test_summary_by_sales_channel(tmp_path):

    # ==================================================
    # pandas版DF
    # ==================================================
    summary_by_sales_channel_from_pandas = aggregate_orders(
        test_raw_df, ["sales_channel"]
    )

    # # NOTE
    # # テスト失敗確認用 値変更
    # #
    # summary_by_sales_channel_from_pandas.loc[
    #     summary_by_sales_channel_from_pandas["sales_channel"] == "Amazon", "order_count"
    # ] = 100

    print(summary_by_sales_channel_from_pandas)

    # ==================================================
    # SQL版DF
    # ==================================================
    # --------------------------
    # database用フォルダ作成
    # --------------------------
    db_path = tmp_path / "test.db"

    # --------------------------
    # database保存
    # --------------------------
    save_dataframe_to_sqlite(db_path, test_raw_df, "test")

    # --------------------------
    # データフレーム作成
    # --------------------------

    summary_by_sales_channel_from_sql = build_kpi_dataframe(
        "sql_by_sales_channel_for_test", db_path, ["sales_channel"]
    )

    print(summary_by_sales_channel_from_sql)

    pd.testing.assert_frame_equal(
        summary_by_sales_channel_from_pandas, summary_by_sales_channel_from_sql
    )


# --------------------------
# 月別チャンネル別
# --------------------------
def test_summary_by_month(tmp_path):

    # ==================================================
    # pandas版DF
    # ==================================================

    test_raw_df_with_month = test_raw_df.copy()

    test_raw_df_with_month["order_date"] = pd.to_datetime(
        test_raw_df_with_month["order_date"]
    )

    test_raw_df_with_month["month"] = test_raw_df_with_month["order_date"].dt.to_period(
        "M"
    )

    summary_by_month_from_pandas = aggregate_orders(test_raw_df_with_month, ["month"])
    summary_by_month_from_pandas["month"] = summary_by_month_from_pandas[
        "month"
    ].astype("str")

    # # NOTE
    # # テスト失敗確認用 値変更
    # #
    # summary_by_month_from_pandas.loc[
    #     summary_by_month_from_pandas["month"] == "2026-01", "order_count"
    # ] = 100

    print(summary_by_month_from_pandas)

    # ==================================================
    # SQL版DF
    # ==================================================
    # --------------------------
    # database用フォルダ作成
    # --------------------------
    db_path = tmp_path / "test.db"

    # --------------------------
    # database保存
    # --------------------------
    save_dataframe_to_sqlite(db_path, test_raw_df, "test")

    # --------------------------
    # データフレーム作成
    # --------------------------

    summary_by_month_from_sql = build_kpi_dataframe(
        "sql_by_month_for_test", db_path, ["month"]
    )

    print(summary_by_month_from_sql)

    pd.testing.assert_frame_equal(
        summary_by_month_from_pandas, summary_by_month_from_sql
    )


# --------------------------
# 月×カテゴリー別
# --------------------------
def test_summary_by_month_and_category(tmp_path):

    # ==================================================
    # pandas版DF
    # ==================================================

    test_raw_df_with_month = test_raw_df.copy()

    test_raw_df_with_month["order_date"] = pd.to_datetime(
        test_raw_df_with_month["order_date"]
    )

    test_raw_df_with_month["month"] = test_raw_df_with_month["order_date"].dt.to_period(
        "M"
    )

    summary_by_month_and_category_from_pandas = aggregate_orders(
        test_raw_df_with_month, ["month", "category"]
    )
    summary_by_month_and_category_from_pandas["month"] = (
        summary_by_month_and_category_from_pandas["month"].astype("str")
    )

    # # NOTE
    # # テスト失敗確認用 値変更
    # #
    # summary_by_month_and_category_from_pandas.loc[
    #     summary_by_month_and_category_from_pandas["month"] == "2026-01", "order_count"
    # ] = 100

    print(summary_by_month_and_category_from_pandas)

    # ==================================================
    # SQL版DF
    # ==================================================
    # --------------------------
    # database用フォルダ作成
    # --------------------------
    db_path = tmp_path / "test.db"

    # --------------------------
    # database保存
    # --------------------------
    save_dataframe_to_sqlite(db_path, test_raw_df, "test")

    # --------------------------
    # データフレーム作成
    # --------------------------

    summary_by_month_and_category_from_sql = build_kpi_dataframe(
        "sql_by_month_and_category_for_test", db_path, ["month", "category"]
    )

    print(summary_by_month_and_category_from_pandas)

    pd.testing.assert_frame_equal(
        summary_by_month_and_category_from_pandas,
        summary_by_month_and_category_from_sql,
    )
