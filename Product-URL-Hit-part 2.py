#Product URL received in the above case, hit each URL, and add below items:
#Description
# ASIN
# Product Description
# Manufacturer
#Need to hit around 200 product URL’s and fetch various information.
import requests
import csv
from bs4 import BeautifulSoup

base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
num_pages = 10
num_urls_per_page = 20

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

        # Store the scraped data as a dictionary
        product_data = {
            'Product URL': product_url
        }

        # Append the data to the list
        data.append(product_data)

# Iterate over the list of product URLs and fetch additional information
for product in data:
    url = product['Product URL']
    if url != 'N/A':
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract additional information
        description_element = soup.find('div', {'id': 'productDescription'})
        description = description_element.text.strip() if description_element else 'N/A'

        asin_element = soup.find('th', text='ASIN')
        asin = asin_element.find_next('td').text.strip() if asin_element else 'N/A'

        product_description_element = soup.find('div', {'id': 'productDescription_feature_div'})
        product_description = product_description_element.text.strip() if product_description_element else 'N/A'

        manufacturer_element = soup.find('a', {'id': 'bylineInfo'})
        manufacturer = manufacturer_element.text.strip() if manufacturer_element else 'N/A'

        # Update the product dictionary with additional information
        product.update({
            'Description': description,
            'ASIN': asin,
            'Product Description': product_description,
            'Manufacturer': manufacturer
        })

# Save the data to a CSV file
csv_file = 'asignment-part2-products-url-hit.csv'
csv_columns = ['Product URL', 'Description', 'ASIN', 'Product Description', 'Manufacturer']

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=csv_columns)
    writer.writeheader()
    writer.writerows(data)

print('Data saved to asignment-part2-products-url-hit.csv file.')
