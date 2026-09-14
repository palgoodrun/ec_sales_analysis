# ==================================================
# カテゴリー別
# ==================================================
sql_by_category = """
SELECT
    category,
    COUNT(*) AS order_count,
    SUM(is_cancelled) AS cancelled_order_count,
    SUM(quantity) AS total_quantity,
    SUM(sales_amount) AS total_sales
FROM orders
GROUP BY category
ORDER BY category
"""

# ==================================================
# 販売チャネル別
# ==================================================
sql_by_sales_channel = """
SELECT
    sales_channel,
    COUNT(*) AS order_count,
    SUM(is_cancelled) AS cancelled_order_count,
    SUM(quantity) AS total_quantity,
    SUM(sales_amount) AS total_sales
FROM orders
GROUP BY sales_channel
ORDER BY sales_channel
"""

# ==================================================
# 月別
# ==================================================
sql_by_month = """
SELECT
    strftime('%Y-%m', order_date) AS month,
    COUNT(*) AS order_count,
    SUM(is_cancelled) AS cancelled_order_count,
    SUM(quantity) AS total_quantity,
    SUM(sales_amount) AS total_sales
FROM orders
GROUP BY month
ORDER BY month
"""

# ==================================================
# 月×カテゴリー別
# ==================================================
sql_by_month_and_category = """
SELECT
    strftime('%Y-%m', order_date) AS month,
    category,
    COUNT(*) AS order_count,
    SUM(is_cancelled) AS cancelled_order_count,
    SUM(quantity) AS total_quantity,
    SUM(sales_amount) AS total_sales
FROM orders
GROUP BY month, category
ORDER BY month, category
"""

# ==================================================
# test用
# ==================================================
# --------------------------
# カテゴリー別
# --------------------------
sql_by_category_for_test = """
SELECT
    category,
    COUNT(*) AS order_count,
    SUM(is_cancelled) AS cancelled_order_count,
    SUM(quantity) AS total_quantity,
    SUM(sales_amount) AS total_sales
FROM test
GROUP BY category
ORDER BY category
"""
# --------------------------
# 販売チャンネル別
# --------------------------
sql_by_sales_channel_for_test = """
SELECT
    sales_channel,
    COUNT(*) AS order_count,
    SUM(is_cancelled) AS cancelled_order_count,
    SUM(quantity) AS total_quantity,
    SUM(sales_amount) AS total_sales
FROM test
GROUP BY sales_channel
ORDER BY sales_channel
"""
# --------------------------
# 月別
# --------------------------
sql_by_month_for_test = """
SELECT
    strftime('%Y-%m', order_date) AS month,
    COUNT(*) AS order_count,
    SUM(is_cancelled) AS cancelled_order_count,
    SUM(quantity) AS total_quantity,
    SUM(sales_amount) AS total_sales
FROM test
GROUP BY month
ORDER BY month
"""

# --------------------------
# 月×カテゴリー別
# --------------------------
sql_by_month_and_category_for_test = """
SELECT
    strftime('%Y-%m', order_date) AS month,
    category,
    COUNT(*) AS order_count,
    SUM(is_cancelled) AS cancelled_order_count,
    SUM(quantity) AS total_quantity,
    SUM(sales_amount) AS total_sales
FROM test
GROUP BY month,category
ORDER BY month,category
"""
