import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL to scrape
url = "https://www.fpg.taipei/en/about/other-company"

# Fetch the webpage content
response = requests.get(url)
response.raise_for_status()  # Check for errors

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Lists to store data
company_names = []
products = []
addresses = []
websites = []
businesses = []

# Find all company sections
company_sections = soup.find_all("li", class_="list-othergroup")

# Loop through each section
for section in company_sections:
    # Extract company name
    name = section.find("h4", class_="fz-h4").get_text(strip=True) if section.find("h4", class_="fz-h4") else "N/A"

    # Extract product
    product_span = section.find("span", string=lambda x: x and "Product" in x)
    product = product_span.find_next("p").get_text(strip=True) if product_span else "N/A"

    # Extract address
    address_span = section.find("span", string=lambda x: x and "Address" in x)
    address = address_span.find_next("p").get_text(strip=True) if address_span else "N/A"

    # Extract website
    website_span = section.find("span", string=lambda x: x and "Website" in x)
    website = website_span.find_next("a", href=True)["href"] if website_span else "N/A"

    # Extract business
    business_span = section.find("span", string=lambda x: x and "Business" in x)
    business = business_span.find_next("p").get_text(strip=True) if business_span else "N/A"

    # Append data to lists
    company_names.append(name)
    products.append(product)
    addresses.append(address)
    websites.append(website)
    businesses.append(business)

# Create a DataFrame
data = pd.DataFrame({
    "Company Name": company_names,
    "Product": products,
    "Address": addresses,
    "Website": websites,
    "Business": businesses
})

# Save to Excel
output_file = "company_details.xlsx"
data.to_excel(output_file, index=False)
print(f"Data saved successfully to {output_file}")
