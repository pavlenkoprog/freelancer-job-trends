# Анализ данных и генерация SQL-запросов с использованием LLM

## Использованные технологии
 - Click для создания cli интерфейса, для обеспечения масштабируемости проекта, и ...
 - SQLlight для хранения данных и их выполнения SQL запросов обеспечивает необходимый функционал без излишеств, что подходит для прототипа
 - Pandas для первичного анализа данных и определения информации о колонках которые содержат категории
 - в качестве LLM применялось 2 модели gpt-4o и SQLight:

### GPT-4o через OpenAI API
gpt-4o через API Openai обеспечивает качественную обработку запроса пользователя работает с русским языком и плохой грамматикой, выдает более универсальный набор SQL запросов, но требует обращения к API и соответственно платный.

python app/cli.py "Как много людей работает в поддержке пользователей?"  
Выполнение запроса...  
sql_query SELECT COUNT(*) FROM freelancer_earnings WHERE Job_Category = 'Customer Support'; DB_PATH E:\python_science\freelancer-job-trends-main\app\freelancer_earnings.db
Результат:  
 COUNT(*)  
      244

python app/cli.py "Какая работа самая высокооплачиваемая ?"  
Выполнение запроса...  
sql_query SELECT Job_Category, AVG(Earnings_USD) AS average_earnings FROM freelancer_earnings GROUP BY Job_Category ORDER BY average_earnings DESC LIMIT 1; DB_PATH E:\python_science\freelancer-job-trends-main\app\freelancer_earnings
.db  
Результат:  
   Job_Category  average_earnings  
App Development       5201.447581

python app/cli.py "how many people are involved in Customer Support?"  
Генерация SQL-запроса...  
Выполнение запроса...  
sql_query SELECT COUNT(DISTINCT Freelancer_ID) FROM freelancer_earnings WHERE Job_Category = 'Customer Support';  
Результат:  
 COUNT(DISTINCT Freelancer_ID)  
                           244

python app/cli.py "what is the maximum experience level?"   
Генерация SQL-запроса...  
Выполнение запроса...  
sql_query SELECT Experience_Level FROM freelancer_earnings ORDER BY CASE WHEN Experience_Level = 'Expert' THEN 3 WHEN Experience_Level = 'Intermediate' THEN 2 WHEN Experience_Level = 'Beginner' THEN 1 END DESC LIMIT 1;  
Результат:  
Experience_Level  
          Expert

### Sqlcoder через Ollama (локально)

Как альтернативу API Openai я применил модель defog_sqlcoder-7b-2:F16 запущенную локально через сервис Ollama
Данная модель является одной из вариаций sqlcoder и по заверению разработчиков превосходит gpt-4 поэтому была выбрана для данной задачи
при использовании GPU время на генирацию запросов почти не отличается от времени генерации через API Openai.
Поскольку работает локально она бесплатна, но для ее нормальной работы необходимо минимум 16Gb GPU

python app/cli.py "какая работа самая высокооплачиваемая ?"  
Генерация SQL-запроса...  
Выполнение запроса...  
sql_query SELECT we.job_category, SUM(we.earnings_usd) AS total_earnings FROM freelancer_earnings we GROUP BY we.job_category ORDER BY total_earnings DESC LIMIT 1;  
Результат:  
  Job_Category  total_earnings  
Graphic Design         1361271  

python app/cli.py "how many people are involved in Customer Support?"  
Генерация SQL-запроса...  
Выполнение запроса...  
sql_query SELECT COUNT(DISTINCT CASE WHEN f.Job_Category = 'Customer Support' THEN f.Freelancer_ID END) AS customer_support_freelancers FROM freelancer_earnings f;  
Результат:  
 customer_support_freelancers  
                          244

python app/cli.py "what is the maximum experience level?"  
Генерация SQL-запроса...  
Выполнение запроса...  
sql_query SELECT MAX(f.Experience_Level) FROM freelancer_earnings f;  
Результат:  
MAX(f.Experience_Level)  
           Intermediate  

## Результаты тестирования моделей на примерах

Одним из тестов я проверял насколько правлено модели будут решать не очевидные задачи
"какая работа самая высокооплачеваемая ?"
gpt-4o выполнил правильно с точки зрения пользователя  выдал запрос для average_earnings в то время как sqlcoder  выдал запрос для total_earnings
"what is the maximum experience level?" 
sqlcoder выдал запрос для нахождения максимального значение по алфавиту, 
хотя обоим моделям я передал значеня категорий в промпте, gpt-4o справился с задачей своеобразно но корректно
В целом заметно что sqlcoder выдает более громозткие не оптимальные запросы которые хуже читаются хотя в некоторых случаях могут быть более универсальными 



