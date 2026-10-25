
from core.database import execute_sql_query

table_schema = execute_sql_query(
    "SELECT sql FROM sqlite_master WHERE type='table' AND name='products'"
)[0][0]

sample_rows = execute_sql_query("SELECT * FROM products GROUP BY product_type")

vendors = [row[0] for row in execute_sql_query("SELECT DISTINCT vendor FROM products")]
