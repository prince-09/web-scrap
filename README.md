# Product Scraper API

This project implements a simple FastAPI-based web scraper for extracting product details from the website [Dental Stall](https://dentalstall.com/shop/). It scrapes product titles, prices, and image URLs from the catalogue and stores them locally in a JSON file. The scraper avoids redundant updates by caching product data in memory, ensuring that products with unchanged prices are not updated.

## Features

- **Scraping Product Data**: Extract product title, price, and image URL from the website.
- **Image Downloading**: Downloads product images and saves them locally.
- **Caching**: Caches product data in-memory and only updates the database (JSON file) if the price changes.
- **Simple Authentication**: Protects the scraping endpoint using a static token.
- **Configurable Scraping**: Allows scraping a specified number of pages.
- **Saving Data**: Stores scraped product data in a local `scraped_products.json` file.

## Requirements

- Python 3.7+
- FastAPI
- Requests
- Pydantic

You can install the required dependencies using the following:

```bash
pip install -r requirements.txt
```

## Setup

1. **Clone the Repository**

   ```bash
   git clone <url>
   cd product-scraper-api
   ```

2. **Install Dependencies**

   Make sure you have all the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the FastAPI Server**

   You can start the FastAPI application using Uvicorn:

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### 1. `/scrape/`
Scrapes product data from the specified number of pages.

#### Method: `GET`

#### Query Parameters:
- `pages`: (Optional) The number of pages to scrape. Default is 5.
- `Authorization`: The static token to authenticate the request. Use the format `Bearer your_static_token_here`.

#### Example Request:

```bash
curl -X 'GET' 'http://127.0.0.1:8000/scrape/?pages=5' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer your_static_token_here'
```

#### Response:

A JSON object containing the list of scraped products:

```json
{
  "products": [
    {
      "product_title": "3M ESPE Restorative Introductory Valux Kit",
      "product_price": 4395.00,
      "path_to_image": "images/3M_ESPE_Restorative_Introductory_Valux_Kit.jpg"
    },
    {
      "product_title": "3M ESPE Relyx Luting Cement",
      "product_price": 3490.00,
      "path_to_image": "images/3M_ESPE_Relyx_Luting_Cement.jpg"
    }
  ]
}
```

#### Caching Behavior:
- **In-memory Cache**: The product data is stored in memory during the session.
- **Price Check**: If the price of a product hasn't changed since the last scrape, it will not be updated or stored again.

### 2. `Authorization Token`

The `Authorization` header is required for all requests to access the `/scrape/` endpoint. Use the following format for the token:

```
Bearer your_static_token_here
```

### Static Token Example:

```bash
Authorization: Bearer your_static_token_here
```

### Scraped Data Storage

- The scraped data is saved in a local `scraped_products.json` file. Example content:

```json
[
  {
    "product_title": "3M ESPE Restorative Introductory Valux Kit",
    "product_price": 4395.00,
    "path_to_image": "images/3M_ESPE_Restorative_Introductory_Valux_Kit.jpg"
  },
  {
    "product_title": "3M ESPE Relyx Luting Cement",
    "product_price": 3490.00,
    "path_to_image": "images/3M_ESPE_Relyx_Luting_Cement.jpg"
  }
]
```

- **Images** are saved in the `images/` directory with filenames derived from the product titles.

## Caching and Scraping Logic

- **Caching Mechanism**: Product details are stored in memory during the scraping session, and if the product's price remains the same, it will not be updated in the file. This prevents redundant updates to products that haven't changed.
- **Scrape Logic**: The product's title, price, and image are scraped from each page of the catalogue. Invalid or placeholder images (such as SVG placeholders) are skipped.

## Troubleshooting

### Common Issues:

1. **Invalid Image URL**: If you see the following message in the logs:
   ```
   Skipping invalid image URL: data:image/svg+xml,...
   ```
   It means the scraper encountered an invalid image URL (often an SVG placeholder). These URLs are skipped automatically.

2. **No Connection to the Website**: Ensure that the website is accessible and that you have internet access. If a page fails to load, the scraper will retry based on the error handling logic.

3. **Unauthorized Access**: Ensure that the `Authorization` token is correctly passed in the request header.
