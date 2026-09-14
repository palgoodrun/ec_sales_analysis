# ==================================================
# Template
# ==================================================
# setting_logging.py

# 用途：
# ・コンソール出力
# ・ログファイル出力

# 使用例：
# logger = setup_logging(config["log"])

# 主な変更ポイント：
# ・ログレベル
# ・ログ保存先
# ・ログフォーマット
# ・エンコーディング
# ・ログローテーション
# ・型ヒント追加

# 更新日：
# 2026-07-15

# ==================================================
# import
# ==================================================
import logging
from pathlib import Path
from typing import TypedDict


# ==================================================
# class
# ==================================================
class LogConfig(TypedDict, total=False):
    level: str
    file_path: str


# ==================================================
# setup_logging
# ==================================================
def setup_logging(log_config: LogConfig) -> logging.Logger:

    # ==================================================
    # 設定変更メモ
    # ==================================================
    # ■ ログレベル
    # log_config["level"]
    #
    # INFO
    # WARNING
    # ERROR
    # DEBUG
    #
    # --------------------------
    # ■ ログ保存先
    # log_config["file_path"]
    #
    # 例
    # logs/app.log
    # logs/debug.log
    #
    # --------------------------
    # ■ ログフォーマット
    # formatter
    #
    # よく追加する項目
    # %(filename)s
    # %(funcName)s
    # %(lineno)d
    #
    # --------------------------
    # ■ エンコーディング
    #
    # utf-8
    # utf-8-sig
    #
    # Excel用途なら
    # utf-8-sigを検討
    #
    # --------------------------
    # ■ ログローテーション
    #
    # ログ肥大化した場合
    #
    # FileHandler
    # ↓
    # RotatingFileHandler
    #
    # へ変更
    #
    # ==================================================

    # --------------------------
    # root logger取得
    # --------------------------
    logger = logging.getLogger()

    # --------------------------
    # ログレベル
    # --------------------------
    level = getattr(
        logging,
        log_config.get("level", "INFO"),
    )
    logger.setLevel(level)

    # --------------------------
    # ログフォーマット
    # --------------------------
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # --------------------------
    # コンソール出力
    # --------------------------
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    # --------------------------
    # ログフォルダ作成
    # --------------------------
    log_path = Path(log_config.get("file_path", "logs/ec_sales_analysis.log"))
    log_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------
    # ファイル出力
    # --------------------------
    file = logging.FileHandler(
        log_path,
        mode="a",
        encoding="utf-8",
    )
    file.setFormatter(formatter)

    # --------------------------
    # Handler重複防止
    # --------------------------
    if not logger.handlers:
        logger.addHandler(console)
        logger.addHandler(file)

    return logger
