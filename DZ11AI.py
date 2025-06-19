# дання 1
# Напишіть модель для генерації персонального плану
# тренувань з двох ланцюгів:
#  Перший ланцюг отримує мету тренування(схуднення,
# набір м’язів, тощо) та повертає список вправ
#  Другий ланцюг отримує список вправ, рівень
# підготовки
# користувача(низький,
# середній,
# професіонал) та кількість часу на тиждень(в годинах)
# і повертає план тренувань

from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

import os
import dotenv

dotenv.load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

llm = GoogleGenerativeAI(
    model='gemini-2.0-flash',
    google_api_key=api_key,
)


schemas = [ResponseSchema(name='Content', description='список вправ')]
parser = StructuredOutputParser.from_response_schemas(schemas)
instructions = parser.get_format_instructions()


prompt_exercises = PromptTemplate.from_template(
    """
    Твоя задача — скласти список вправ відповідно до мети тренування.

    Мета: {goal}

    Дай 5-8 вправ, які найбільше відповідають цій меті. Вивід має відповідати формату: {instructions}
    """,
    partial_variables={"instructions": instructions}
)


exercise_chain = prompt_exercises | llm | parser


goal = input("Ваша ціль тренування (наприклад: схуднення, набір м’язів): ")
response = exercise_chain.invoke({"goal": goal})
exercise_list = response["Content"]

print("\n📋 Згенеровані вправи:")
print(exercise_list)


prompt_plan = PromptTemplate.from_template(
    """
    Твоя задача — використовуючи список вправ, рівень підготовки користувача та кількість часу на тиждень (в годинах),
    скласти детальний план тренувань на тиждень.

    Вправи: {exercises}
    Рівень підготовки: {level}
    Кількість часу на тиждень: {time}

    Зроби детальний план по днях (наприклад, Пн — Присідання, 3 підходи по 12 разів).
    Балансуй навантаження з урахуванням рівня. Не перевищуй вказану кількість годин.
    """
)


plan_chain = prompt_plan | llm

level = input("\nВаш рівень підготовки (низький, середній, професіонал): ")
time = input("Скільки годин на тиждень ви готові тренуватись?: ")

training_plan = plan_chain.invoke({
    "exercises": exercise_list,
    "level": level,
    "time": time
})

print("\n📅 Персональний план тренувань:")
print(training_plan)


