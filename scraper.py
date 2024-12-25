import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
from typing import List
import json
from utils import retry_request
from models import Product
import os

# In-memory cache to store scraped product data
scraped_data_cache = {}

# Create the images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')


class Scraper:
    def __init__(self, settings):
        self.settings = settings
        self.products = []
        self.base_url = "https://dentalstall.com/shop/page/"
        self.output_file = "scraped_products.json"
        
    def get_product_info(self, product_card):
        try:
            # Extract product title
            title_tag = product_card.find('h2', class_='woo-loop-product__title')
            title = title_tag.get_text(strip=True) if title_tag else "Unknown Product"
            
            # Extract product price (Handling the symbol and commas)
            price_tag = product_card.find('span', class_='woocommerce-Price-amount')
            price = price_tag.get_text(strip=True).replace('₹', '').replace(',', '').strip() if price_tag else '0'
            price = float(price) if price else 0
            
            # Extract product image URL
            img_tag = product_card.find('img', class_='attachment-woocommerce_thumbnail')
            image_url = img_tag['data-lazy-src'] if img_tag and 'data-lazy-src' in img_tag.attrs else None
            print("IMG-", image_url)
            return title, price, image_url
        except Exception as e:
            print(f"Error extracting product info: {e}")
            return None

    def scrape_page(self, page_num):
        # Correct pagination URL format
        url = f"{self.base_url}{page_num}/"
        print(f"Scraping page {page_num}...")
        try:
            response = retry_request(url, proxy=self.settings.proxy)
            soup = BeautifulSoup(response.text, 'html.parser')
            product_cards = soup.find_all('li', class_='product')
            for card in product_cards:
                product_info = self.get_product_info(card)
                if product_info:
                    title, price, image_url = product_info
                    # If product exists in cache and price is same, skip it
                    if title in scraped_data_cache and scraped_data_cache[title]['product_price'] == price:
                        print(f"Skipping {title} (price not changed)")
                        continue

                    # Add or update the product in the cache
                    scraped_data_cache[title] = {
                        "product_price": price
                    }

                    # Skip products with invalid or missing images
                    if image_url and not image_url.startswith("data:image/svg+xml"):
                        image_path = self.download_image(image_url, title)
                    else:
                        image_path = None
                    
                    self.products.append(Product(product_title=title, product_price=price, path_to_image=image_path))
        except Exception as e:
            print(f"Error scraping page {page_num}: {e}")

    def scrape(self):
        for page_num in range(1, self.settings.pages_to_scrape + 1):
            self.scrape_page(page_num)
        
        self.save_to_json()

    def save_to_json(self):
        # Save products to a JSON file
        with open(self.output_file, 'w') as json_file:
            json.dump([product.dict() for product in self.products], json_file, indent=4)
        print(f"Scraped {len(self.products)} products and saved to {self.output_file}.")

    def download_image(self, image_url, product_title):
        try:
            # Sanitize the product title to make it a valid filename
            filename = re.sub(r'[^\w\s-]', '', product_title).strip().replace(' ', '_') + ".jpg"
            file_path = os.path.join('images', filename)
            
            # Skip invalid image URLs (e.g., placeholders)
            if image_url and 'data:image' not in image_url:
                response = requests.get(image_url, stream=True, timeout=10)
                if response.status_code == 200:
                    with open(file_path, 'wb') as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    print(f"Downloaded image for {product_title} to {file_path}")
                    return file_path
                else:
                    print(f"Error downloading image: {response.status_code}")
            else:
                print(f"Skipping invalid image URL: {image_url}")
            return None
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None
