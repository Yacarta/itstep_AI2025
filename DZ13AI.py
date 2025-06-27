
# Напишіть чат бота, з інструментом по рекомендації  ресторанів.
# Для цього скористайтесь
# GoogleSerperAPIWrapper(type="places")
# Інструмент повинен отримувати запит для пошуку та
# повертати таку інформацію про ресторани:
#  назва
#  посилання на сайт(якщо є)
#  рейтинг

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)
import dotenv
import os


dotenv.load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
serper_key = os.getenv("SERPER_API_KEY")


llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash',
    google_api_key=gemini_key
)


searcher = GoogleSerperAPIWrapper(api_key_serper=serper_key, type="places")


def search_restaurants(query: str) -> str:
    result = searcher.results(query)
    response = []

    for r in result.get("places", [])[:5]:  # обмежимо до 5 результатів
        name = r.get("title", "Невідомо")
        website = r.get("website", "Сайт відсутній")
        rating = r.get("rating", "Немає оцінки")
        response.append(f"-- {name}\n-- {website}\n-- Рейтинг: {rating}")

    return "\n\n".join(response) if response else "Не знайдено жодного ресторану."


restaurant_tool = Tool(
    name="RestaurantFinder",
    description="Знаходить ресторани у вказаному місті. Приклад запиту: 'піца у Львові'",
    func=search_restaurants
)


agent = create_react_agent(
    model=llm,
    tools=[restaurant_tool]
)

messages = {
    "messages": [
        SystemMessage("""
        Ти ввічливий чат-бот, що рекомендує ресторани.
        Коли користувач просить знайти ресторан, скористайся інструментом пошуку.
        Формат виводу:
        -- Назва
        -- Посилання на сайт (якщо є)
        -- Рейтинг
        Виведи до 5 ресторанів.
        """)
    ]
}


while True:
    user_input = input("Ви: ")

    if user_input.strip() == "":
        break

    messages["messages"].append(HumanMessage(user_input))
    messages = agent.invoke(messages)
    print("Бот:", messages["messages"][-1].content)
