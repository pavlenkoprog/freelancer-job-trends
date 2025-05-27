import os

import ollama
import requests

from query_handler import execute_query

MODEL_NAME = "sqlcoder"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_FILE = os.path.join(BASE_DIR, "../data/prompt.md")
METADATA_FILE = os.path.join(BASE_DIR, "../data/metadata.sql")

OLLAMA_URL = "http://localhost:11434"


def adjust_sql_for_sqlite(sql_query):
    """Adjusts an SQL query to be more compatible with SQLite."""
    adjusted_query = sql_query.replace("ILIKE", "LIKE")
    adjusted_query = adjusted_query.replace("TRUE", "1").replace("FALSE", "0")
    return adjusted_query


def generate_prompt(question):
    """Формирует финальный текст промпта из шаблона и метаданных"""
    with open(PROMPT_FILE, "r") as f:
        prompt_template = f.read()
    with open(METADATA_FILE, "r") as f:
        metadata = f.read()
    return prompt_template.format(user_question=question, table_metadata_string=metadata)


def generate_sql(question: str) -> str:
    """Отправляет промпт к Ollama и получает SQL"""
    prompt = generate_prompt(question)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        prompt = generate_prompt(question)  # prompt — это строка
        response = ollama.generate(model='defog_sqlcoder-7b-2:F16', prompt=prompt)
        generated_text = response["response"]
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при обращении к Ollama: {e}")
        return ""

    adjusted_sql_query = adjust_sql_for_sqlite(generated_text)

    sql_query = (
        generated_text.split(";")[0]
        .split("```")[0]
        .strip()
        + ";"
    )

    return sql_query


if __name__ == '__main__':
    sql_query = generate_sql("Выведи самый распространенный тип оплаты ")
    result = execute_query(sql_query)
    print(result)

