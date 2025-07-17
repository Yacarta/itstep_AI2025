# import requests
# import json

# # документи АРІ https://dev.wix.com/docs/rest/articles/get-started/api-keys
# # Define the API endpoint
# url = 'https://www.wixapis.com/stores/v1/products/query'
#
# WIX_API_KEY = os.getenv("WIX_API_KEY")
# SITE_ID = os.getenv("SITE_ID")
# headers = {
#     'Authorization': WIX_API_KEY,
#     'wix-site-id':SITE_ID,
#     'Content-Type': 'application/json'
# }
#
# # Define the body of the request
# body = {
#     "query": {
#         "filter": json.dumps({"price": {"$gt": 0}}),
#         "paging": {
#             "limit": 10,
#             "offset": 0
#         },
#         "sort": json.dumps({"_id": 1})
#     }
# }
#
# # Send the POST request
# response = requests.post(url, headers=headers, data=json.dumps(body))
#
# # Check if the request was successful
# if response.status_code == 200:
#     # Parse the JSON response
#     data = response.json()
#     print(data)
# else:
#     print(f"Failed to retrieve data: {response.status_code}")
#     print(response.text)

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