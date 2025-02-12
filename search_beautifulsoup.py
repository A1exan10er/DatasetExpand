import requests
from bs4 import BeautifulSoup
import os
import urllib.request

def download_image(url, folder):
    """Download an image from a URL and save it to the specified folder."""
    if not os.path.exists(folder):
        os.makedirs(folder)
    image_name = os.path.join(folder, url.split("/")[-1])
    urllib.request.urlretrieve(url, image_name)
    print(f"Downloaded {image_name}")

def fetch_search_page(search_text, page):
    """Fetch the search results page for the given search text and page number."""
    search_url = f'https://www.flickr.com/search?text={search_text}&structured=yes&page={page}'
    print(f"Fetching search URL: {search_url}")
    response = requests.get(search_url)
    if response.status_code != 200:
        print(f"Failed to fetch search URL: {response.status_code}")
        return None
    return response.text

def save_html(content, filename):
    """Save the HTML content to a file."""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def extract_image_urls(soup):
    """Extract image URLs from the BeautifulSoup object."""
    img_tags = soup.find_all('img', attrs={'loading': 'lazy'})
    print(f"Found {len(img_tags)} image tags")
    img_urls = []
    for img in img_tags:
        img_url = img.get('src')
        if img_url:
            if img_url.startswith("//"):
                img_url = "https:" + img_url
            img_urls.append(img_url)
        else:
            print("No image URL found")
    return img_urls

def search_and_download_images(search_text, num_pages):
    """Search for images and download them."""
    folder = search_text.replace(' ', '_')
    if not os.path.exists(folder):
        os.makedirs(folder)

    for page in range(1, num_pages + 1):
        page_content = fetch_search_page(search_text, page)
        if not page_content:
            continue

        soup = BeautifulSoup(page_content, 'html.parser')
        save_html(soup.prettify(), f'output_page_{page}.html')
        
        img_urls = extract_image_urls(soup)
        for img_url in img_urls:
            print(f"Found image URL: {img_url}")
            download_image(img_url, folder)

# Search settings
search_text = 'usb stick'  # Object name for image search
num_pages = 3  # Number of pages to scrape
search_and_download_images(search_text, num_pages)
