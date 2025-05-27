import click
from llm_interface_gpt import generate_sql
from query_handler import execute_query


@click.command()
@click.argument("question")
def ask(question):
    print("Генерация SQL-запроса...")
    query = generate_sql(question)

    print("Выполнение запроса...")
    result = execute_query(query)
    print(f"Результат:\n{result}")


if __name__ == "__main__":
    ask()

# python app/cli.py "Какой самый популярный способ оплаты?"

# python app/cli.py "What is the most popular payment?"
# sql_query SELECT Payment_Method, COUNT(*) AS Frequency
# FROM freelancer_earnings
# GROUP BY Payment_Method
# ORDER BY Frequency DESC
# LIMIT 1; DB_PATH /home/dmitriy/projects/FreelancerAnalysis/app/freelancer_earnings.db
# Результат:
# Payment_Method  Frequency
#         Crypto        514

# python app/cli.py "what is the maximum experience level?"
# sql_query SELECT MAX(Experience_Level) AS Maximum_Experience_Level FROM freelancer_earnings;
# DB_PATH /home/dmitriy/projects/FreelancerAnalysis/app/freelancer_earnings.db
# Результат:
# Maximum_Experience_Level
#             Intermediate

# python app/cli.py "how many people are involved in Customer Support?"
# sql_query SELECT COUNT(*) FROM freelancer_earnings WHERE Job_Category = 'Customer Support';
# DB_PATH /home/dmitriy/projects/FreelancerAnalysis/app/freelancer_earnings.db
# Результат:
#  COUNT(*)
#       244
