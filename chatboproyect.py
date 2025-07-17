import os
import dotenv
import requests
import json

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

dotenv.load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WIX_API_KEY = os.getenv("WIX_API_KEY")
SITE_ID = os.getenv("SITE_ID")


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GEMINI_API_KEY
)


messages = [
    SystemMessage(content="""
Ти ввічливий асистент магазину Puro y Organico. 
Коли тебе питають про продукт, шукай його через API WIX, і відповідай зрозуміло, з назвами та цінами.
""")
]


def search_product(search: str):
    search = search.strip()
    if not search or len(search) < 2:
        print(" Запит порожній або занадто короткий.")
        return []

    url = "https://www.wixapis.com/stores/v1/products/query"

    headers = {

        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Authorization": WIX_API_KEY,
        "wix-site-id": SITE_ID
    }

    payload = {
      "query": {
        "filter": "{\"paymentStatus\":\"PAID\"}",
        "sort": "{\"number\": \"desc\"}",
        "paging": {
          "limit": "50"
        }
      }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raises exception for 4XX/5XX errors
        return response.json().get("products", [])
    except requests.exceptions.RequestException as e:
        print(f" Wix API error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response content: {e.response.text}")
        return []

# Основний цикл чату
while True:
    user_input = input("🧑 Ви: ").strip()
    if not user_input:
        break


    productos = search_product(user_input)

    if productos:
        listado = "\n".join([
            f"- {p['name']}: {p['price']['formatted']}"
            for p in productos
        ])
        user_content = f"Користувач питає: {user_input}\nОсь товари які ти можеш використати для відповіді:\n{listado}"
    else:
        user_content = f"Користувач питає: {user_input}\nНа жаль, товари не знайдено в базі Wix."


    messages.append(HumanMessage(content=user_content))

    respuesta = llm.invoke(messages)
    messages.append(respuesta)

    print(f"🤖 AI: {respuesta.content}")