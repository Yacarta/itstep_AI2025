# # # Прочитайте
# # # файл data/lesson9/return_policy.txt
# # # та
# # # напишіть простий чат для відповідей на питання користувачів
# # # стосовно повернення товару.
# # # Діалог завершується коли користувач ввів порожній
# # # рядок.
# # # Модель отримує інструкцію з вмістом файлу та всю
# # # історію спілкування разом з новим повідомленням у форматі
# # # Instruction: …
# # # Human: message1
# # # AI: message2
# # # Human: message3
# # # AI: message4
# # # Human: message5
# # # AI:
# #
# # from langchain_google_genai import GoogleGenerativeAI
# #
# # import dotenv
# # import os
# #
# # # завантажити api ключі з папки .env
# # dotenv.load_dotenv()
# #
# # # отримати сам ключ
# # api_key = os.getenv('GEMINI_API_KEY')
# #
# # with open("data/lesson9/return_policy.txt", "r", encoding="UTF-8") as file:
# #     rulse = file.read()
# #
# # llm = GoogleGenerativeAI(
# #     model='gemini-2.0-flash',  # назва моделі
# #     google_api_key=api_key,    # ваша API
# #     #top_k=10,                  # серед скількох найбільш ймовірних слів обирати нове слово
# #     temperature=0.3,            # температура
# #     #max_output_tokens=10        # максимальна довжина відповіді у токенах
# # )
# #
# # query = f'''Instruction: Ти - чат бот. Твоя задача - дай відповіді щодо правил повернення
# # товару {rulse} користувачеві на основі його питань в віччливій формі.'''
# #
# # while True:
# #     question = input('Ваше питання стосовно повернення товару або Ентер для закінчення. ')
# #
# #     if question == '':
# #         break
# #
# #
# #     query += f'\n HUMAN: {question}\n AI:'
# #
# #     response = llm.invoke(query)
# #     query += response
# #
# #     print(response)
#
# # from langchain_google_genai import GoogleGenerativeAI
# # from langchain.prompts import PromptTemplate
# #
# # import dotenv
# # import os
# #
# # # завантажити api ключі з папки .env
# # dotenv.load_dotenv()
# #
# # # отримати сам ключ
# # api_key = os.getenv('GEMINI_API_KEY')
# #
# # # створення моделі
# # # Велика мовна модель(llm)
# #
# # llm = GoogleGenerativeAI(
# #     model='gemini-2.0-flash',  # назва моделі
# #     google_api_key=api_key,  # ваша API
# # )
# #
# # # запит, prompt(підказка)
# # # prompt engeneering(створення промптів)
# #
# # query = "Ти асистент, твоя задача давати відповіді згідно певного документу {rules}"
# #
# # # створення промпта
# #
# # # складові промпта
# # # Хто ти
# # # базові інструкції(пару речень що треба робити)
# # # додаткова інформація
# # # Деталізація(що робити в певних ситуація)
# # # Приклади
# # # дані від самого користувача
# #
# #
# # prompt = PromptTemplate.from_template(
# #     """
# #     Ти ввічливий асистент. Твоя задача допомогти людині підготуватись до співбесіди.
# #     Ти задаєш питання, користувач відповідає, в кінці співбесіди дай чесний відгук,
# #     вкажити що було добре, а де є помилки.
# #
# #     Використовуй поради з цього документу по проведенню співбесід.
# #     Документ: {document}
# #
# #     ** Якщо користувач починає нервувати коли дає відповіді: **
# #         * Якщо користувач починає запинатися, давати нечіткі відповіді,
# #         використувавати слова-паразити(наприклад 'Еее', 'Типу', 'Короче')
# #         йому потрібно про це вказати та порекомендувати зробити дихальну вправу
# #         аби заспокоїтись.
# #         * В таких ситуація ти **ПОВИНЕН** змінити тему розмови, трохи знизити
# #         емоційне навантаження на користувача, можливо трохи підбадьорити(наприклад
# #         сказати що в нього\неї непогано виходить)
# #
# #     **ПРИКЛАДИ:**
# #
# #     AI: Чому ви обрали нашу компанію?
# #     Користувач: Тому що мені потрібні гроші, а у вас найвища зарплата.
# #
# #     Помилки користувача: компанії важливо знати що її співробітники справді
# #     зацікавленні посадою, модуть запропонувати нові ідеї для комерційних продуктів,
# #     Відповідаючи, що вас цікавлять лише гроші створює враження пасивного та меркантильного кандидата,
# #     який при першій можливості перейде в іншу компанію
# #     Переваги відповіді: переваг немає
# #
# #     ####
# #     Вхідні дані
# #
# #     Користувач: {user_data}
# #     """
# # )
# #
# # document = 'Дуже великий докемнт з порадами'
# # user_data = 'Я тут заради грошей'
# #
# # # так не роблять
# # # # створення конкретного запити за наведеним шаблоном
# # # result = prompt.invoke({
# # #     'document': 'Дуже великий докемнт з порадами',
# # #     'user_data': 'Я тут заради грошей'
# # # })
# # #
# # # print(result)
# #
# # # # роблять ось так
# # #
# # # # створення ланцюга
# # # chain = prompt | llm
# # #
# # # result = chain.invoke({
# # #     'document': 'Дуже великий докемнт з порадами',
# # #     'user_data': 'Я тут заради грошей'
# # # })
# # #
# # # print(result)
# #
# #
# # # Аналіз тональності
# # #
# # # Визнач, чи є тональність тексту позитивною,
# # # негативною чи нейтральною.
# #
# # prompt = PromptTemplate.from_template(
# #     """
# #     Ти класифікатор текстів. Твоя задача віднести текст до
# #     одного з класів: позитивний, негативний, нейтральний.
# #     Текст повинен належати лише одному класу, тому давай відповідь одним словом
# #     з цих трьох
# #
# #     **ПРИКЛАДИ:**
# #     Текст: мені сподобався цей фільм
# #     Клас: позитивний
# #
# #     Текст: шкода витраченого часу
# #     Клас: негативний
# #
# #     Текст: добре провів час, але вдруге на цей фільм не піду
# #     Клас: нейтральний
# #
# #     Текст: {user_input}
# #     Клас:
# #     """
# # )
# #
# # # приклади в промптах називають Few-Shot Prompt
# # # Input:
# # # Output:
#
# # Human:
# # AI:
#
# # Data:
# # Result:
#
# # # створення ланцюга
# # chain = prompt | llm
# #
# # user_data = "Обов'язково порекомендую друзям"
# #
# # response = chain.invoke({
# #     'user_input': user_data
# # })
# # print(response)
#
#
# # print(12*6 - 2)
#
#
# # # chain of thought
# # data = """У магазині продали 12 коробок. У кожній коробці по 6 пляшок, але в одній коробці не вистачало 2 пляшок.
# # Скільки всього пляшок було продано?
# #     Дай коротку відповідь одним числом"""
# #
# # response = llm.invoke(data)
# # print(response)
#
#
# # Термінологія
# # Zero-Shot - промпт без прикладів, лише інструкції
# # Few-Shot  - промпт з прикладами
# # CoT       - chain of thought(ланцюг міркувань). набір кроків щоб розв'язати певну задачу
#
#
# # 3. Прочитайте файл data\lesson10\products.txt з описом
# # послуг СПА. Напишіть промпт для рекомендації послуги
# # виходячи з запиту користувача
# # Вхідні параметри – опис товарів, запит користувача
# # Реалізуйте двома способами:
# #  Zero-shot
# #  Chain of Thoughts
#
# from langchain_google_genai import GoogleGenerativeAI
# from langchain.prompts import PromptTemplate
#
# import dotenv
# import os
#
# # завантажити api ключі з папки .env
# dotenv.load_dotenv()
#
# # отримати сам ключ
# api_key = os.getenv('GEMINI_API_KEY')
#
# # створення моделі
# # Велика мовна модель(llm)
#
# llm = GoogleGenerativeAI(
#     model='gemini-2.0-flash',  # назва моделі
#     google_api_key=api_key,  # ваша API
# )
#
# with open("data\lesson10\products.txt", "r", encoding="UTF-8") as file:
#     SPA = file.read()
#
# promt = PromptTemplate.from_template(""" Ты ассистент по услугам СПА-салону. Твоя задача подобрать услуги
# спа-салону в соответствии с запросами пользователя. Информация по услугам СПА-салона находится в документе.
#
# Документ по услугам СПА-салона: {SPA}
#
# Вопрос: {ask}
#
# """)
# chain = promt | llm
#
# ask = input("запит користувача: ")
#
# result = chain.invoke({'SPA': SPA, 'ask': ask})
#
# print(result)
import json

#from fontTools.ttLib.tables.ttProgram import instructions
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

import json
import dotenv
import os

from sympy.physics.units import temperature

#from Lesson9LLM import response

# завантажити api ключі з папки .env
dotenv.load_dotenv()

# отримати сам ключ
api_key = os.getenv('GEMINI_API_KEY')

# створення моделі
# Велика мовна модель(llm)

llm = GoogleGenerativeAI(
    model='gemini-2.0-flash',  # назва моделі
    google_api_key=api_key,
    temperature = 0.2# ваша API
)

# # Користувач задає питання по книзі
# # Ваша задача:
# # 1. Дати відповідь на питання
# # 2. Порекомендувати схожі книги(на ту саму тему, того ж автора, жанру, ...)
#
# # має назву книги і питання -- хочемо отримати всю інформацію про книгу
# # і відповідь на питання
#
# # маючи інформацію про книгу порекомендувати щось схоже
#
#
# # ------------------------------
#
# # схема для відповідей
# schemas = [
#     ResponseSchema(name='answer', description='відповідь на питання користувача'),
#     ResponseSchema(name='theme', description='головна тема книги'),
#     ResponseSchema(name='author', description='автор книги'),
#     ResponseSchema(name='jaunre', description='жанр книги')
# ]
#
# # створення парсер
# parser = StructuredOutputParser.from_response_schemas(schemas)
#
# # отримати інструкція для llm
# instructions = parser.get_format_instructions()
#
# # print(instructions)
#
# # створення промпта
# prompt = PromptTemplate.from_template(
#     """
#     Ти асистент онлайн книгарні. Твоя задача давати відповіді
#     на питання користувачів. Відповіді мають бути чіткі та інформативні.
#     Загальний стиль спілкування ввічливий, іноді можеш використовувати
#     неформальний стиль.
#     Також ти повинен визначити параметри книжки про яку питає
#     користувач(наприклад жанр, автор, тема, ...)
#
#     Питання: {question}
#
#     Формат відповіді:
#     {instructions}
#     """,
#     partial_variables={"instructions": instructions}
# )
#
# # створення ланцюга
# chain = prompt | llm | parser
#
# response = chain.invoke({
#     "question": "Коли була написана книга 1984",
# })
#
# print(response)
# print(response['theme'])
# print(type(response))
#
# # # збереження у файл
# # with open('response.json', 'w', encoding='UTF-8') as file:
# #     json.dump(response, file)
# #
# # # завантаження з файлу
# # with open('response.json', 'r', encoding='UTF-8') as file:
# #     new_response = json.load(file)
# #
# # print(new_response)
#
#
# # рекомендація схожих книг
# prompt = PromptTemplate.from_template(
#     """
#     Ти асистент онлайн книгарні. Твоя задача давати рекомендації книг
#     користувачам певно жанру, теми та автора. Запропонуй по 3-5 книг по
#     кожному пункту.
#     Загальний стиль спілкування ввічливий, іноді можеш використовувати
#     неформальний стиль.
#
#     Жанр: {jaunre}
#     Автор: {author}
#     Тема: {theme}
#
#     Відповідь дай у вигляді списку, познач які книги до якого
#     пункту відносяться
#     * Книги на схожу тему
#     * Книги того ж автора
#     * Книги того ж жанру
#     """
# )
#
# chain_recommendation = prompt | llm
#
# recommendation = chain_recommendation.invoke({
#     "jaunre": response['jaunre'],
#     "author": response['author'],
#     "theme": response['theme'],
# })
#
# print(recommendation)
#
# # дістати всі назви книг з рекомендації
#
# schemas = [
#     ResponseSchema(name='books', description='список з назвами книг')
# ]
#
# parser = StructuredOutputParser.from_response_schemas(schemas)
# instructions = parser.get_format_instructions()
#
# prompt = PromptTemplate.from_template(
#     """
#     Твоя задача дістати назви усіх книг з тексту.
#
#     Текст: {text}
#
#     Формат відповіді:
#     {instructions}
#     """,
#     partial_variables={"instructions": instructions}
# )
#
# chain_book_selector = prompt | llm | parser
#
# response = chain_book_selector.invoke({
#     "text": recommendation
# })
#
# print(response)
#
# for book in response['books']:
#     print(book)

# Завдання 2
# Напишіть модель для генерації листа:
#  Перший ланцюг отримує короткий опис листа та
# генерує основний зміст
#  Другий ланцюг отримує основний зміст та стиль
# листа(формальний, неформальний, тощо) та генерує
# лист
shemas = [
    ResponseSchema(name='Content', description='основні пункти листа')
]

parser = StructuredOutputParser.from_response_schemas(shemas)

instructions = parser.get_format_instructions()

prompt = PromptTemplate.from_template(
    """
    Ти помічник в написанні листа. Твоя задача використовуючи опис генерувати основні пункти листа  з 3-5 пунктів. 
    
    Приклад:
    Опис: Звернення в посольство по отриманню документів.
    Пункти:  Привітання
    Інформація про себе
    Основний запит ( отримання документів)
    Контактна інформація
    
    Опис: Запит на прийняття на роботу.
    Пункти:  Привітання
    Інформація про себе(досвід роботи, навички)
    Очікування ( очікувана зарплата, умови праці)
    Чому необхідно обрати мене
    Контактна інформація
    
    
    
    Опис: {desc}
    
    Формат відповіді :{instractions}
    """,
    partial_variables={"instractions": instructions}
)

#print(prompt.get_prompts())
chain_list = prompt | llm | parser
desc = "Прохання про підвищення зарплати "
response = chain_list.invoke({"desc": desc})
print(response)
#  Другий ланцюг отримує основний зміст та стиль
# листа(формальний, неформальний, тощо) та генерує
# лист
llm = GoogleGenerativeAI(
    model='gemini-2.0-flash',  # назва моделі
    google_api_key=api_key,
    temperature = 0.7# ваша API
)


prompt = PromptTemplate.from_template(
    """
    Ти помічник в написанні листа. Твоя задача використовуючи  основні пункти листа написати лист в певному стилі 

    Пункти: {points}
    Стиль: {style}
    """
)
style = "Офіційний"
chain_letter_creator = prompt | llm
letter = chain_letter_creator.invoke({
    "points":response["Content"],
    "style": style
})

print(letter)



# Завдання 3
# Напишіть модель для генерації резюме:
#  Перший ланцюг отримує опис вакансії та повертає
# основні навички, які необхідні
#  Другий ланцюг отримує основні навички та опис
# кандидата і генерує резюме

