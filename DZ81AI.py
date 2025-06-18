# Прочитайте
# файл data/lesson9/return_policy.txt
# та
# напишіть простий чат для відповідей на питання користувачів
# стосовно повернення товару.
# Діалог завершується коли користувач ввів порожній
# рядок.
# Модель отримує інструкцію з вмістом файлу та всю
# історію спілкування разом з новим повідомленням у форматі
# Instruction: …
# Human: message1
# AI: message2
# Human: message3
# AI: message4
# Human: message5
# AI:
from langchain_google_genai import GoogleGenerativeAI

import dotenv
import os

# завантажити api ключі з папки .env
dotenv.load_dotenv()

# отримати сам ключ
api_key = os.getenv('GEMINI_API_KEY')

with open("data/lesson9/return_policy.txt", "r", encoding="UTF-8") as file:
    ruls = file.read()

llm = GoogleGenerativeAI(
    model='gemini-2.0-flash',  # назва моделі
    google_api_key=api_key,    # ваша API
    #top_k=10,                  # серед скількох найбільш ймовірних слів обирати нове слово
    temperature=0.3,            # температура
    #max_output_tokens=10        # максимальна довжина відповіді у токенах
)
while True:
    question = input('Ваше питання по політиці повернення товару або Ентер для закінчення. ')

    if question == '':
        break

    query = f"""
        В тебе є інструкція - {ruls}.
        Дай відповідь на питання {question}.
    """


    response = llm.invoke(query)
    query += response

    print(response)