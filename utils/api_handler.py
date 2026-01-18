import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API.
    """

    url = "https://dummyjson.com/products?limit=100&skip=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raises HTTPError for bad responses

        data = response.json()

        # Extract product list
        products = data.get("products", [])
        print(f"Successfully fetched {len(products)} products from API.")

        return products

    except Exception as e:
        print("Failed to fetch products from API.")
        print("Error:", e)
        return []


