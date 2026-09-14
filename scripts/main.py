# ==================================================
# import
# ==================================================
import pandas as pd
from pathlib import Path

# ==========================
# from_modules
# ==========================
from modules.config_loader import load_config
from modules.config_validator import validate_log_config, validate_tool_config
from modules.database_manager import save_dataframe_to_sqlite
from modules.sql_aggregator import build_kpi_dataframe
from modules.kpi_evaluator import evaluate_all_cancellation_rates
from modules.result_exporter import export_analysis_results_to_excel
from modules.logger_setup import setup_logging


# ==================================================
# main
# ==================================================
def main() -> None:

    # ==========================
    # config読み込み
    # ==========================
    config = load_config(config_path="config/config.json")
    validate_tool_config(config)

    input_config = config["input"]
    database_config = config["database"]
    threshold_config = config["thresholds"]
    output_config = config["output"]

    # ==========================
    # CSV読み込み
    # ==========================

    raw_data_path = Path(input_config["data_dir"]) / input_config["data_file"]

    try:
        raw_df = pd.read_csv(raw_data_path, parse_dates=["order_date"])
        logger.info(f"CSV読み込み完了 ファイル: {raw_data_path}")

    except FileNotFoundError:
        logger.error(f"CSVファイルが見つかりません: {raw_data_path}")
        raise

    # ==========================
    # database用フォルダ作成
    # ==========================

    db_path = Path(database_config["db_dir"]) / database_config["db_file"]

    # ==========================
    # database保存
    # ==========================

    save_dataframe_to_sqlite(db_path, raw_df, database_config["table_name"])

    # ==========================
    # データフレーム作成 from SQL
    # ==========================

    # カテゴリー別 --------------------

    summary_by_category = build_kpi_dataframe("sql_by_category", db_path, ["category"])

    # 販売チャネル別 --------------------

    summary_by_sales_channel = build_kpi_dataframe(
        "sql_by_sales_channel", db_path, ["sales_channel"]
    )

    # 月別 --------------------

    summary_by_month = build_kpi_dataframe("sql_by_month", db_path, ["month"])

    # 月×カテゴリー別 --------------------

    summary_by_month_and_category = build_kpi_dataframe(
        "sql_by_month_and_category", db_path, ["month", "category"]
    )

    # ==========================
    # KPI評価
    # ==========================

    summary_dfs = {
        "category": summary_by_category,
        "sales_channel": summary_by_sales_channel,
        "month": summary_by_month,
        "month_category": summary_by_month_and_category,
    }

    evaluated_summary_dfs = evaluate_all_cancellation_rates(
        summary_dfs, threshold_config["cancellation_threshold"]
    )

    # ==========================
    # Excel出力
    # ==========================
    output_path = Path(output_config["output_dir"]) / output_config["output_file"]

    export_analysis_results_to_excel(output_path, evaluated_summary_dfs)


# ==================================================
# entrypoint
# ==================================================
if __name__ == "__main__":
    # ==========================
    # logger設定
    # ==========================
    try:
        log_config = load_config(config_path="config/log_config.json")
        validate_log_config(log_config)

        log_setting = log_config["log"]
        logger = setup_logging(log_setting)
        logger.info("logger設定完了")

    except Exception as e:
        print(f"logger設定エラー: {e}")
        raise

    # ==========================
    # start
    # ==========================

    logger.info("【EC売上分析ツール 開始】")

    # ==========================
    # main
    # ==========================
    try:
        main()

    except Exception:
        logger.exception("【EC売上分析ツール 異常終了】")
        raise

    # ==========================
    # end
    # ==========================

    logger.info("【EC売上分析ツール 正常終了】")
