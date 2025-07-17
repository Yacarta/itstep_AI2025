import os
import requests

API_KEY = os.getenv("WIX_API_KEY")
SITE_ID = os.getenv("SITE_ID")
BASE_URL = f'https://www.wixapis.com/stores/v1/products'

headers = {
    'Authorization': API_KEY,
    'Content-Type': 'application/json',
}

def search_products(query):
    params = {
        'query': query
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.status_code, 'message': response.text}

# Example usage
products = search_products('Lavanda')
print(products)