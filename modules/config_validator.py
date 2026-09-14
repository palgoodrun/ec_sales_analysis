# ==================================================
# validate_log_config
# ==================================================
def validate_log_config(config: dict) -> None:

    # ==========================
    # 必須キー確認
    # ==========================

    required_keys = {
        "log": {
            "level",
            "file_path",
        },
    }

    for section, keys in required_keys.items():

        if section not in config:
            raise KeyError(f"{section} がconfigに登録されていません")

        missing_keys = keys - config[section].keys()

        if missing_keys:
            raise KeyError(f"config: {section} に {missing_keys} が登録されていません")

    # ==========================
    # 型確認
    # ==========================

    expected_types = {
        "log": {
            "level": str,
            "file_path": str,
        },
    }

    for section, types in expected_types.items():
        for key, expected_type in types.items():

            if not isinstance(config[section][key], expected_type):
                raise TypeError(
                    f"config: {section} - {key} は {expected_type} で設定する必要があります\n"
                    f"現在の設定: {type(config[section][key]).__name__}"
                )


# ==================================================
# validate_tool_config
# ==================================================
def validate_tool_config(config: dict) -> None:

    # ==========================
    # 必須キー確認
    # ==========================

    required_keys = {
        "input": {
            "data_dir",
            "data_file",
        },
        "database": {
            "db_dir",
            "db_file",
            "table_name",
        },
        "thresholds": {
            "cancellation_threshold",
        },
        "output": {
            "output_dir",
            "output_file",
        },
    }

    for section, keys in required_keys.items():

        if section not in config:
            raise KeyError(f"{section} がconfigに登録されていません")

        missing_keys = keys - config[section].keys()

        if missing_keys:
            raise KeyError(f"config: {section} に {missing_keys} が登録されていません")

    # ==========================
    # 型確認
    # ==========================

    expected_types = {
        "thresholds": {
            "cancellation_threshold": int | float,
        }
    }

    for section, types in expected_types.items():
        for key, expected_type in types.items():

            if not isinstance(config[section][key], expected_type):
                raise TypeError(
                    f"config: {section} - {key} は {expected_type} で設定する必要があります\n"
                    f"現在の設定: {type(config[section][key]).__name__}"
                )

    # ==========================
    # 値確認
    # ==========================

    value_constraints = {
        "thresholds": {
            "cancellation_threshold": {
                "min": 0,
                "max": 100,
            }
        }
    }

    for section, constraints in value_constraints.items():
        for key, constraint in constraints.items():

            min_value = constraint["min"]
            max_value = constraint["max"]

            value = config[section][key]

            if not min_value <= value <= max_value:
                raise ValueError(
                    f"config: {section} - {key} は 「{min_value} 以上、{max_value} 以下」で設定する必要があります\n"
                    f"現在の設定: {value}"
                )
