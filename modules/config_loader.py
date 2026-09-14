# ==================================================
# Template
# load_config.py
#
# 用途：
# JSON設定ファイル読込
#
# 使用例：
# config = load_config(config_path)
#
# 主な変更ポイント：
# ・encoding
# ・例外処理
# ・validation追加

# ==================================================
# import
# ==================================================
import json

# ==================================================
# load_config
# ==================================================
def load_config(config_path: str) -> dict:

    with open(
        config_path,
        mode="r",
        encoding="utf-8",
    ) as f:
        config = json.load(f)

    return config