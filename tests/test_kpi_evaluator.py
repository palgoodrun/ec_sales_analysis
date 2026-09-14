# ==================================================
# import
# ==================================================
import pandas as pd

# ==========================
# from_modules
# ==========================
from modules.kpi_evaluator import evaluate_cancellation_rate

# ==================================================
# test_data
# ==================================================
test_category_df = pd.DataFrame(
    {
        "category": ["Cosmetics", "Food", "Water Server"],
        "order_count": [3, 5, 8],
        "completed_order_count": [2, 4, 7],
        "cancelled_order_count": [1, 1, 1],
        "total_quantity": [100, 200, 300],
        "total_sales": [600, 800, 7000],
        "avg_order_value": [300, 200, 1000],
        "cancellation_rate": [33.3, 20.0, 10.0],
    }
)


# ==================================================
# pytest
# ==================================================
# ==========================
# test_cancellation_status_by_threshold
# ==========================
def test_cancellation_status_by_threshold():

    result_df = evaluate_cancellation_rate(test_category_df, 20.0)

    result = result_df["cancellation_rate_status"]

    expected = pd.Series(
        ["warning", "warning", "normal"],
        name="cancellation_rate_status",
    )

    pd.testing.assert_series_equal(result, expected)


# ==========================
# test_cancellation_status_column_exists
# ==========================
def test_cancellation_status_column_exists():

    result_df = evaluate_cancellation_rate(test_category_df, 20.0)

    added_columns = result_df.columns.difference(test_category_df.columns)

    assert added_columns.tolist() == ["cancellation_rate_status"]
