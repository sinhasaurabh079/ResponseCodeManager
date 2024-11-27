import requests


def fetch_http_dog_data(code):
    """
    Fetch response code details from https://http.dog/{code}.json
    """
    url = f"https://http.dog/{code}.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()  # Return the JSON response as a Python dictionary
        else:
            return None  # Handle non-200 responses gracefully
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for code {code}: {e}")
        return None
