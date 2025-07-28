import os
import requests
import json
from langdetect import detect
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

# Load environment variables
import streamlit as st
import os
import requests
from langdetect import detect
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
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
    google_api_key=GEMINI_API_KEY)

# Shop information document
SHOP_INFO = {
    'delivery': {
        'cost': {
            'uk': """Вартість доставки:
Для Боготи та Кундинамарки:
0-1 кг: 18,000 COP
1-2 кг: 28,000 COP
2-3 кг: 38,000 COP
3-4 кг: 111,000 COP
4+ кг: 13,600 COP

Для інших великих міст:
0-1 кг: 116,000 COP
1-2 кг: 116,000 COP
2-3 кг: 116,000 COP
3-4 кг: 176,000 COP
4+ кг: 20,600 COP

Для віддалених міст або авіаперевезень вартість інша.

Безкоштовна доставка (для великих міст):
Для замовлень понад 200,000 COP доставка безкоштовна.

Спеціальна доставка:
Для великих або важких товарів може бути додаткова плата.""",
            'en': """Shipping Costs:
For Bogotá and Cundinamarca:
0-1 kg: 18,000 COP
1-2 kg: 28,000 COP
2-3 kg: 38,000 COP
3-4 kg: 111,000 COP
4+ kg: 13,600 COP

For other major cities:
0-1 kg: 116,000 COP
1-2 kg: 116,000 COP
2-3 kg: 116,000 COP
3-4 kg: 176,000 COP
4+ kg: 20,600 COP

For distant cities or air shipments, costs vary.

FREE Shipping (for major cities):
For orders over 200,000 COP, shipping is free.

Special Shipping:
For large or heavy items, additional fees may apply.""",
            'es': """Gastos de envío:
Para Bogotá y Cundinamarca:
0-1 kg: 18,000 COP
1-2 kg: 28,000 COP
2-3 kg: 38,000 COP
3-4 kg: 111,000 COP
4+ kg: 13,600 COP

Para otras ciudades principales:
0-1 kg: 116,000 COP
1-2 kg: 116,000 COP
2-3 kg: 116,000 COP
3-4 kg: 176,000 COP
4+ kg: 20,600 COP

Para ciudades lejanas o envíos aéreos, el costo es diferente.

Envío GRATUITO (para ciudades principales):
Para compras superiores a $200,000 COP, el envío es gratuito.

Envío especial:
Para artículos grandes o pesados puede haber cargos adicionales."""
        },
        'time': {
            'uk': """Час доставки:
1-3 робочі дні (може бути довше) залежно від місця призначення.
Для замовлень, відправлених у п'ятницю, доставка буде в суботу до 12:00 або в понеділок до 18:00.
Ви можете відстежити своє замовлення на сайті транспортної компанії.""",
            'en': """Delivery Time:
1-3 business days (may take longer) depending on destination.
For orders shipped on Friday, delivery will be attempted on Saturday before 12:00 or Monday before 18:00.
You can track your order on the carrier's website.""",
            'es': """Tiempo de entrega:
1-3 días hábiles (puede demorar más) dependiendo del destino.
Para pedidos enviados el viernes, se intentará entregar el sábado antes de las 12:00 o el lunes antes de las 18:00.
Puedes rastrear tu pedido en la página de la transportadora."""
        },
        'conditions': {
            'uk': """Умови доставки:
Доставка здійснюється за адресою, вказаною клієнтом.
Якщо отримувач відсутній, посилка залишатиметься у вахтера або буде спроба доставки наступного дня.""",
            'en': """Delivery Conditions:
Delivery is made to the address specified by the customer.
If the recipient is absent, the package will be left with the concierge or delivery will be attempted the next day.""",
            'es': """Condiciones de envío:
La entrega se realiza en la dirección especificada por el cliente.
Si el destinatario no está presente, el paquete se dejará en la portería o se intentará entregar al día siguiente."""
        }
    },
    'returns': {
        'policy': {
            'uk': """Політика повернення:
Ви маєте право повернути товар протягом 14 днів після отримання.
Для повернення надішліть електронного листа на info@puroyorganico.com.co з вашими даними та номером замовлення.
Товар має бути невідкритим, повним і без пошкоджень.
Клієнт несе витрати на повернення товару.""",
            'en': """Return Policy:
You have 14 days to return items after receipt.
To return, email info@puroyorganico.com.co with your details and order number.
Items must be unopened, complete, and undamaged.
Customer bears return shipping costs.""",
            'es': """Política de devoluciones:
Tienes 14 días para devolver productos después de recibirlos.
Para devolver, envía un correo a info@puroyorganico.com.co con tus datos y número de pedido.
Los productos deben estar sin abrir, completos y sin daños.
El cliente asume los gastos de devolución."""
        },
        'refund': {
            'uk': """Повернення коштів:
Гроші будуть повернуті тим самим способом, яким була здійснена оплата.
Повернення коштів здійснюється після отримання та перевірки товару.""",
            'en': """Refund Policy:
Money will be refunded using the original payment method.
Refunds are processed after receiving and inspecting the returned items.""",
            'es': """Reembolsos:
El dinero será reembolsado usando el método de pago original.
Los reembolsos se procesan después de recibir e inspeccionar los productos devueltos."""
        }
    },
    'store': {
        'info': {
            'uk': """Інформація про магазин:
Адреса: Богота, Колумбія
Продажі тільки через вебсайт
Доставка по всій Колумбії
Час роботи: Пн-Пт, 9:00-16:00
Телефон: (319) 364-45-50
WhatsApp: (319) 364-45-50
Email: info@puroyorganico.com.co""",
            'en': """Store Information:
Address: Bogotá, Colombia
Online store only
Nationwide shipping
Hours: Mon-Fri, 9:00-16:00
Phone: (319) 364-45-50
WhatsApp: (319) 364-45-50
Email: info@puroyorganico.com.co""",
            'es': """Información de la tienda:
Dirección: Bogotá, Colombia
Venta solo por la página web
Envíos a toda Colombia
Horario: Lun-Vie, 9:00-16:00
Teléfono: (319) 364-45-50
WhatsApp: (319) 364-45-50
Email: info@puroyorganico.com.co"""
        }
    }
}

LANGUAGE_PROMPTS = {
    'uk': f"""
Ти ввічливий асистент магазину Puro y Organico. Ось інформація про магазин:

Доставка:
{SHOP_INFO['delivery']['cost']['uk']}

Час доставки:
{SHOP_INFO['delivery']['time']['uk']}

Умови доставки:
{SHOP_INFO['delivery']['conditions']['uk']}

Повернення:
{SHOP_INFO['returns']['policy']['uk']}

Повернення коштів:
{SHOP_INFO['returns']['refund']['uk']}

Інформація про магазин:
{SHOP_INFO['store']['info']['uk']}

Коли тебе питають про продукт, шукай його через get_products_by_keyword.
У відповіді обов'язково вказуй:
- Назву продукту
- Ціну
- Посилання на продукт
- Фото продукту (якщо є)
Форматуй відповідь у вигляді списку.
""",
    'en': f"""
You are a helpful assistant for Puro y Organico store. Here's shop information:

Shipping Costs:
{SHOP_INFO['delivery']['cost']['en']}

Delivery Time:
{SHOP_INFO['delivery']['time']['en']}

Delivery Conditions:
{SHOP_INFO['delivery']['conditions']['en']}

Return Policy:
{SHOP_INFO['returns']['policy']['en']}

Refund Policy:
{SHOP_INFO['returns']['refund']['en']}

Store Information:
{SHOP_INFO['store']['info']['en']}

When asked about products, search via get_products_by_keyword.
In your response always include:
- Product name
- Price
- Product URL
- Product image (if available)
Format the response as a list.
""",
    'es': f"""
Eres un asistente amable de la tienda Puro y Organico. Aquí está la información de la tienda:

Gastos de envío:
{SHOP_INFO['delivery']['cost']['es']}

Tiempo de entrega:
{SHOP_INFO['delivery']['time']['es']}

Condiciones de envío:
{SHOP_INFO['delivery']['conditions']['es']}

Política de devoluciones:
{SHOP_INFO['returns']['policy']['es']}

Política de reembolsos:
{SHOP_INFO['returns']['refund']['es']}

Información de la tienda:
{SHOP_INFO['store']['info']['es']}

Cuando te pregunten por productos, búscalos a través de get_products_by_keyword.
En tu respuesta siempre incluye:
- Nombre del producto
- Precio
- URL del producto
- Imagen del producto (si está disponible)
Formatea la respuesta como una lista.
"""
}

DEFAULT_LANGUAGE = 'es'


def detect_language(text):
    try:
        lang = detect(text)
        return lang if lang in LANGUAGE_PROMPTS else DEFAULT_LANGUAGE
    except:
        return DEFAULT_LANGUAGE


def get_system_message(language):
    return SystemMessage(content=LANGUAGE_PROMPTS.get(language, LANGUAGE_PROMPTS[DEFAULT_LANGUAGE]))


def get_all_products():
    """Get all products from the store"""
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
        st.error(f"Error fetching products: {str(e)}")
        return []


def get_product_by_name(name):
    """Get product by exact name match"""
    products = get_all_products()
    if not products:
        return None

    name_lower = name.lower()
    for product in products:
        if product.get("name", "").lower() == name_lower:
            return product
    return None


def search_product(query, max_results=5):
    """Search products with hybrid approach"""
    # First try exact match
    exact_match = get_product_by_name(query)
    if exact_match:
        return [exact_match]

    # Then try keyword search
    keyword_results = get_products_by_keyword(query, max_results)
    return keyword_results[:max_results] if keyword_results else None


def get_products_by_keyword(keyword, max_results=20, timeout=15):
    """Search products by keyword and return formatted product information"""
    try:
        response = requests.get(
            f"{base_url}/products/search",
            params={'keyword': keyword, 'limit': max_results},
            headers=headers,
            timeout=timeout
        )
        response.raise_for_status()
        data = response.json()

        products = data.get("products", [])
        if not products:
            return None

        formatted_products = []
        for product in products:
            product_info = {
                'name': product.get('name', 'No name available'),
                'price': product.get('price', 'Price not available'),
                'url': f"{WIX_SITE_URL}/product/{product.get('slug', '')}",
                'image': product.get('mainImage', {}).get('url', 'No image available')
            }
            formatted_products.append(product_info)

        return formatted_products

    except requests.exceptions.RequestException as e:
        st.error(f"Search error: {str(e)}")
        return None


def format_product_response(products, language):
    """Format product information based on language"""
    if not products:
        return {
            'uk': "Товари не знайдено.",
            'en': "No products found.",
            'es': "No se encontraron productos."
        }.get(language, "No products found.")

    if language == 'uk':
        response_text = "Знайдені товари:\n\n"
        for item in products:
            response_text += (
                f"📌 Назва: {item['name']}\n"
                f"💵 Ціна: {item['price']}\n"
                f"🔗 Посилання: {item['url']}\n"
                f"🖼️ Зображення: {item['image']}\n\n"
            )
    elif language == 'es':
        response_text = "Productos encontrados:\n\n"
        for item in products:
            response_text += (
                f"📌 Nombre: {item['name']}\n"
                f"💵 Precio: {item['price']}\n"
                f"🔗 Enlace: {item['url']}\n"
                f"🖼️ Imagen: {item['image']}\n\n"
            )
    else:  # English by default
        response_text = "Found products:\n\n"
        for item in products:
            response_text += (
                f"📌 Name: {item['name']}\n"
                f"💵 Price: {item['price']}\n"
                f"🔗 URL: {item['url']}\n"
                f"🖼️ Image: {item['image']}\n\n"
            )

    return response_text


def handle_general_question(query, language):
    """Handle general questions about the store"""
    query_lower = query.lower()

    # Delivery questions
    if any(word in query_lower for word in ['доставк', 'deliver', 'envío', 'shipping']):
        if 'варт' in query_lower or 'cost' in query_lower or 'costo' in query_lower:
            return SHOP_INFO['delivery']['cost'][language]
        elif 'час' in query_lower or 'time' in query_lower or 'tiempo' in query_lower:
            return SHOP_INFO['delivery']['time'][language]
        else:
            return f"{SHOP_INFO['delivery']['cost'][language]}\n\n{SHOP_INFO['delivery']['time'][language]}"

    # Returns questions
    elif any(word in query_lower for word in ['повернен', 'return', 'devoluc']):
        return f"{SHOP_INFO['returns']['policy'][language]}\n\n{SHOP_INFO['returns']['refund'][language]}"

    # Payment questions
    elif any(word in query_lower for word in ['оплат', 'payment', 'pago']):
        return SHOP_INFO['payment'].get(language, "Payment information not available")

    # Contact questions
    elif any(word in query_lower for word in ['контакт', 'contact', 'contacto']):
        return SHOP_INFO['store']['info'][language]

    return None


# Initialize the chatbot
def initialize_chatbot():
    if 'messages' not in st.session_state:
        st.session_state.messages = [get_system_message(DEFAULT_LANGUAGE)]

    if 'agent' not in st.session_state:
        st.session_state.agent = create_react_agent(
            model=llm,
            tools=[get_products_by_keyword, get_product_by_name, get_all_products, search_product],
        )


# Streamlit app
def main():
    st.set_page_config(page_title="Puro y Organico Chatbot", page_icon="🛒")
    st.title("🤖 Puro y Organico Assistant")
    st.caption("Your personal shopping assistant for Puro y Organico store")

    # Initialize chatbot
    initialize_chatbot()

    # Display chat messages
    for message in st.session_state.messages[1:]:  # Skip system message
        with st.chat_message("user" if isinstance(message, HumanMessage) else "assistant"):
            st.markdown(message.content)

    # Chat input
    if prompt := st.chat_input("How can I help you today?"):
        # Add user message to chat history
        st.session_state.messages.append(HumanMessage(content=prompt))

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Detect language
        lang = detect_language(prompt)
        st.session_state.messages[0] = get_system_message(lang)

        # Check for general questions first
        general_response = handle_general_question(prompt, lang)
        if general_response:
            with st.chat_message("assistant"):
                st.markdown(general_response)
            st.session_state.messages.append(SystemMessage(content=general_response))
            return

        # Get AI response
        response = st.session_state.agent.invoke({"messages": st.session_state.messages})
        ai_message = response["messages"][-1]

        # Handle no products found case
        if "no products found" in ai_message.content.lower():
            ai_message.content = {
                'uk': "Вибачте, я не знайшов товарів за вашим запитом. Можете уточнити назву або задати інше питання про наш магазин.",
                'en': "Sorry, I couldn't find products matching your query. Please try a different search term or ask about our shop.",
                'es': "Lo siento, no encontré productos que coincidan con tu búsqueda. Prueba con otro término o pregunta sobre nuestra tienda."
            }.get(lang, "No products found.")

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(ai_message.content)

        # Add AI message to chat history
        st.session_state.messages.append(ai_message)




if __name__ == "__main__":
    main()