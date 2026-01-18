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


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info.
    """

    product_map = {}

    for product in api_products:
        pid = product.get("id")

        # Extract required fields only
        info = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating"),
            "price": product.get("price")
        }

        product_map[pid] = info

    return product_map


