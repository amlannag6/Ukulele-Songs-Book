import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# URLs of the webpages with the links to PDFs
urls = [
    "https://ukuleleorchestraofkamloops.com/our-music/songs-a-i",
    "https://ukuleleorchestraofkamloops.com/our-music/songs-j-z"
]

# Directory where you want to save the downloaded PDFs
output_directory = "songs"

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Iterate through the URLs
for url in urls:
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the links on the webpage
    links = soup.find_all('a')

    # Iterate through the links
    for link in links:
        href = link.get('href')
        if href and href.endswith('.pdf'):
            # Join the URL of the webpage with the PDF link
            pdf_url = urljoin(url, href)

            # Extract the PDF filename
            pdf_filename = os.path.join(output_directory, os.path.basename(pdf_url))

            # Download the PDF
            with open(pdf_filename, 'wb') as pdf_file:
                pdf_response = requests.get(pdf_url)
                pdf_file.write(pdf_response.content)
                print(f"Downloaded: {pdf_filename}")