# ==================================================
# import
# ==================================================
import pytest
from copy import deepcopy

# ==========================
# from modules
# ==========================
from modules.config_validator import validate_tool_config

# ==================================================
# test_data
# ==================================================
test_config = {
    "input": {"data_dir": "data", "data_file": "orders.csv"},
    "database": {"db_dir": "database", "db_file": "orders.db", "table_name": "orders"},
    "thresholds": {"cancellation_threshold": 20},
    "output": {"output_dir": "output", "output_file": "ec_sales_analysis.xlsx"},
}


# ==================================================
# test_tool_with_valid_data
# ==================================================
def test_tool_with_valid_data():

    validate_tool_config(test_config)


# ==================================================
# ttest_tool_raises_type_error
# ==================================================
def test_tool_raises_type_error():

    test_config_for_type_error = deepcopy(test_config)

    test_config_for_type_error["thresholds"]["cancellation_threshold"] = "str"

    with pytest.raises(TypeError):
        validate_tool_config(test_config_for_type_error)


# ==================================================
# ttest_tool_raises_value_error
# ==================================================
def test_tool_raises_value_error():

    test_config_for_value_error = deepcopy(test_config)

    test_config_for_value_error["thresholds"]["cancellation_threshold"] = 101

    with pytest.raises(ValueError):
        validate_tool_config(test_config_for_value_error)
