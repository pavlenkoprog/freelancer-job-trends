import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "freelancer_earnings.db")


def execute_query(sql_query: str) -> str:
    try:
        print(f"sql_query {sql_query}")
        conn = sqlite3.connect(DB_PATH)
        result = pd.read_sql_query(sql_query, conn)
        conn.close()
        return result.head(10).to_string(index=False)
    except Exception as e:
        return f"Ошибка при выполнении запроса: {e}"


if __name__ == '__main__':
    query = """
    SELECT Payment_Method, COUNT(*) AS count
    FROM freelancer_earnings
    GROUP BY Payment_Method
    ORDER BY count DESC
    LIMIT 1;
    """
    print(execute_query(query))