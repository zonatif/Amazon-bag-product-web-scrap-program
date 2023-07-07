import requests
import csv
from bs4 import BeautifulSoup

base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
num_pages = 20

data = []  # List to store the scraped data

# Iterate over the desired number of pages
for page in range(1, num_pages + 1):
    url = base_url + str(page)

    # Send HTTP GET request
    response = requests.get(url)

    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all product elements
    product_elements = soup.find_all('div', {'class': 'sg-col-inner'})

    # Iterate over product elements and extract required data
    for product_element in product_elements:
        # Extract product URL
        url_element = product_element.find('a', {'class': 'a-link-normal'})
        product_url = "https://www.amazon.in" + url_element['href'] if url_element else 'N/A'

        # Extract product name
        title_element = product_element.find('span', {'class': 'a-size-base-plus'})
        product_name = title_element.text.strip() if title_element else 'N/A'

        # Extract product price
        price_element = product_element.find('span', {'class': 'a-offscreen'})
        product_price = price_element.text.strip() if price_element else 'N/A'

        # Extract product rating
        rating_element = product_element.find('span', {'class': 'a-icon-alt'})
        product_rating = rating_element.text.strip() if rating_element else 'N/A'

        # Extract number of reviews
        reviews_element = product_element.find('span', {'class': 'a-size-base'})
        num_reviews = reviews_element.text.strip() if reviews_element else 'N/A'

        # Store the scraped data as a dictionary
        product_data = {
            'Product URL': product_url,
            'Product Name': product_name,
            'Product Price': product_price,
            'Rating': product_rating,
            'Number of Reviews': num_reviews
        }

        # Append the data to the list
        data.append(product_data)

# Save the data to a CSV file
csv_file = 'products-part1-assigment.csv'
csv_columns = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews']

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=csv_columns)
    writer.writeheader()
    writer.writerows(data)

print('Data saved to products-part1-assigment.csv file.')