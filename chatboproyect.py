import os
import requests
import json
from langdetect import detect
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize Wix API settings
WIX_SITE_URL = "https://www.puroyorganico.com.co"
base_url = WIX_SITE_URL.rstrip('/') + '/_functions'
headers = {"Content-Type": "application/json"}

# Initialize Gemini AI
llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash',
    google_api_key=GEMINI_API_KEY    )

# Language-specific system messages
LANGUAGE_PROMPTS = {
'uk': """
Ти ввічливий асистент магазину Puro y Organico. Відповідаєш на питання користувачів про магазин та умови доставки
Коли тебе питають про продукт, шукай його через get_products_by_keyword_hybrid, і відповідай зрозуміло, з назвами та цінами.
. Вебсайт на іспанській мові але ти перекладай та відповідай на українській
""",
#     'en': """
# You are a helpful assistant for Puro y Organico store.
# When asked about products, search via get_products_by_keyword_hybrid and respond clearly with names and prices.
# Always respond in English.
# """,
#     'es': """
# Eres un asistente amable de la tienda Puro y Organico.
# Cuando te pregunten por productos, búscalos a través de  get_products_by_keyword_hybrid y responde claramente con nombres y precios.
# Responde siempre en español.
# """

}

DEFAULT_LANGUAGE = 'uk'  # Default to Ukrainian if detection fails


def detect_language(text):
    """Detect input language with fallback to default"""
    try:
        lang = detect(text)
        return lang if lang in LANGUAGE_PROMPTS else DEFAULT_LANGUAGE
    except:
        return DEFAULT_LANGUAGE


def get_system_message(language):
    """Get appropriate system message based on language"""
    return SystemMessage(content=LANGUAGE_PROMPTS.get(language, LANGUAGE_PROMPTS[DEFAULT_LANGUAGE]))


def get_all_products():
    """Fetch all products from Wix with improved error handling."""
    try:
        response = requests.get(
            f"{base_url}/products",
            headers=headers,
            timeout=15
        )
        response.raise_for_status()
        data = response.json()
        return data.get("products", [])
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching products: {str(e)}")
        return []


def search_product(query, max_results=5):
    """Search products with hybrid approach"""
    # First try exact match
    exact_match = get_product_by_name(query, search_locally=True)
    if exact_match:
        return [exact_match]

    # Then try hybrid search
    keyword_results = get_products_by_keyword_hybrid(query, max_local_results=max_results)
    return keyword_results[:max_results]


def get_product_by_name(name, search_locally=True):
    """Get product by exact name match."""
    products = get_all_products()
    if not products:
        return None

    name_lower = name.lower()
    for product in products:
        if product.get("name", "").lower() == name_lower:
            return product
    return None


def get_products_by_keyword_hybrid(keyword, max_local_results=20):
    """Optimized hybrid search with relevance scoring"""
    try:
        response = requests.get(
            f"{base_url}/products/search",
            params={'keyword': keyword, 'limit': max_local_results},
            headers=headers,
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        products = data.get("products", [])
        if not products:
            return []

        keyword_lower = keyword.lower()
        scored_products = []

        for product in products:
            name = product.get("name", "").lower()
            description = product.get("description", "").lower()

            score = 0
            if keyword_lower in name:
                score += 3 + name.count(keyword_lower)
            if keyword_lower in description:
                score += 1 + description.count(keyword_lower)

            if score > 0:
                product['relevance_score'] = score
                scored_products.append(product)

        scored_products.sort(key=lambda x: (-x['relevance_score'], x['name']))
        return scored_products

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Search error: {str(e)}")
        return []


def format_product_info(products, lang='uk'):
    """Format product information in the detected language"""
    if not products:
        return {
            'en': "Sorry, no products found.",
            'es': "Lo siento, no se encontraron productos.",
            'uk': "На жаль, товари не знайдені."
        }.get(lang, "No products found")

    formatted = []
    for idx, product in enumerate(products[:5], 1):
        name = product.get('name', {
            'en': 'Unknown product',
            'es': 'Producto desconocido',
            'uk': 'Невідомий продукт'
        }.get(lang))

        price = product.get('price', {}).get('formatted', {
            'en': 'Price not available',
            'es': 'Precio no disponible',
            'uk': 'Ціна не вказана'
        }.get(lang))

        formatted.append(f"{idx}. {name} - {price}")

    return "\n".join(formatted)


# Language-specific greetings
GREETINGS = {
    'en': "🤖 Welcome to Puro y Organico! How can I help you today?",
    'es': "🤖 ¡Bienvenido a Puro y Organico! ¿Cómo puedo ayudarte hoy?",
    'uk': "🤖 Вітаю в магазині Puro y Organico! Чим можу допомогти?"
}

GOODBYES = {
    'en': "🤖 Goodbye! Have a great day!",
    'es': "🤖 ¡Adiós! ¡Que tengas un buen día!",
    'uk': "🤖 До побачення! Гарного дня!"
}
print("\n--- Hybrid Product Search ---")
keyword = "lavanda"
results = get_products_by_keyword_hybrid(keyword)

if results:
    print(f"\nTop {len(results)} matches for '{keyword}':")
    for i, product in enumerate(results, 1):
        print(f"{i}. {product.get('name')} (ID: {product.get('_id')})")
# Main chat loop
if __name__ == "__main__":
    # Initial language detection
    print(GREETINGS['uk'])  # Default greeting
    current_lang = 'uk'

    while True:
        try:
            user_input = input("\n🧑 You: ").strip()
            if not user_input:
                continue

            # Detect language change
            new_lang = detect_language(user_input)
            if new_lang != current_lang:
                current_lang = new_lang
                language_switch_messages = {
                    'en': 'Switched to English',
                    'es': 'Cambiado a español',
                    'uk': 'Перейшов на українську'
                }
                print(f"\n🤖 {language_switch_messages.get(current_lang, 'Language changed')}")

            # Exit conditions in all languages
            if user_input.lower() in {'exit', 'quit', 'вийти', 'salir'}:
                print(f"\n{GOODBYES[current_lang]}")
                break

            # Search for products
            found_products = search_product(user_input)
            products_info = format_product_info(found_products, current_lang)

            # Prepare AI context
            context = (
                f"User asked ({current_lang}): {user_input}\n"
                f"Available products:\n{products_info}"
            )

            # Get AI response with proper language instruction
            system_msg = get_system_message(current_lang)
            response = llm.invoke([system_msg, HumanMessage(content=context)])

            print(f"\n🤖 Assistant: {response.content}")

        except KeyboardInterrupt:
            print(f"\n{GOODBYES.get(current_lang, GOODBYES['uk'])}")
            break
        except Exception as e:
            error_msg = {
                'en': f"⚠️ An error occurred: {str(e)}",
                'es': f"⚠️ Ocurrió un error: {str(e)}",
                'uk': f"⚠️ Сталася помилка: {str(e)}"
            }
            print(error_msg.get(current_lang, str(e)))