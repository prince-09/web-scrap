import requests
import time

def retry_request(url, proxy=None, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy} if proxy else None)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e
