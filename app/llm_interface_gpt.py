import os
from openai import OpenAI
from query_handler import execute_query

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = " You are well tuned mechanism for generating SQLite queries from user questions." \
                " At the output, only a request is needed, which will be immediately passed to the program. " \
                " The response should not contain characters that are not related to the request, for example ```sql" \
                " Table name: freelancer_earnings" \
                " The table contains columns: Freelancer_ID, Job_Category, Platform, Experience_Level," \
                " Client_Region, Payment_Method, Job_Completed, Earnings_USD, Hourly_Rate," \
                " Job_Success_Rate, Client_Rating, Job_Duration_Days, Project_Type, Rehire_Rate, Marketing_Spend." \
                ' Some columns contain categories:' \
                '- `Job_Category` (object, 8 unique): Web Development, App Development, Data Entry, Digital Marketing,' \
                'Customer Support, Content Writing, Graphic Design, SEO' \
                '- `Platform` (object, 5 unique): Fiverr, PeoplePerHour,Upwork, Toptal, Freelancer' \
                '- `Experience_Level` (object, 3 unique): Beginner, Intermediate, Expert' \
                '- `Client_Region` (object, 7 unique): Asia, Australia, UK, Europe, USA, Middle East, Canada' \
                '- `Payment_Method` (object, 4 unique): Mobile Banking, Crypto, Bank Transfer, PayPal' \
                '- `Project_Type` (object, 2 unique): Fixed, Hourly' \
                " Example request:" \
                " SELECT Payment_Method, COUNT(*) AS count" \
                " FROM freelancer_earnings" \
                " GROUP BY Payment_Method" \
                " ORDER BY count DESC" \
                " LIMIT 1;"


def generate_sql(prompt: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return completion.choices[0].message.content


if __name__ == '__main__':
    sql_query = generate_sql("Выведи самый распространенный тип оплаты ")
    result = execute_query(sql_query)
    print(result)
