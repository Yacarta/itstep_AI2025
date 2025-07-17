

import requests
import os

WIX_API_KEY = os.getenv("WIX_API_KEY")
SITE_ID = os.getenv("SITE_ID")

url = 'https://www.wixapis.com/stores/v1/products/query'

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Authorization': WIX_API_KEY,
    'wix-site-id': SITE_ID
}

data = {
    "query": {
        "filter": "{\"paymentStatus\":\"PAID\"}",
        "sort": "{\"number\": \"desc\"}",
        "paging": {
            "limit": "50"
        }
    }
}

response = requests.post(url, headers=headers, json=data)

# Check if the request was successful
if response.status_code == 200:
    print("Request successful!")
    print(response.json())
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)