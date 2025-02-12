from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time


# Set up the Selenium webdriver with a specific user-agent
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

# URL template
# base_url = "https://www.vcg.com/creative-image/jiandao/?page={}" # Scissors
# base_url = 'https://www.vcg.com/creative-image/6780904/?page={}' # Rulers
# base_url = 'https://www.vcg.com/creative-image/bi/?page={}' # Pens
# base_url = 'https://www.vcg.com/creative-image/6493716/?page={}' # Paper and Notebooks
# base_url = 'https://www.vcg.com/creative-image/yaochi/?page={}' # Keys
# base_url = 'https://www.vcg.com/creative-image/mingpian/?page={}' # Business Cards
base_url = 'https://www.vcg.com/creative-image/bangongyongpin/?page={}' # Office Supplies

# Number of pages to scrape (changed to 18)
num_pages = 30

# Main directory to save the downloaded images
# main_directory = "Scissors_Images"
main_directory = "Office_Supplies_Images"

# Create the main directory if it doesn't exist
if not os.path.exists(main_directory):
    os.makedirs(main_directory)

'''
# Function to download images from a given URL
def download_images(url, page_number):
    driver.get(url)
    time.sleep(2)  # Give the page some time to load

    # Attempt to handle the login window (close it if it appears)
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'iconfont.passport-close'))
        )
        close_button.click()  # Click on the close button
        print("Login window closed.")
    except:
        pass

    # Simulate scrolling to trigger lazy-loading
    for _ in range(3):  # Adjust the number of scrolls as needed
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)  # Adjust the sleep time between scrolls as needed

    # Wait for lazy-loaded images to be fully loaded
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'lazyload_hk.ll_loaded'))
        )
    except Exception as e:
        print(f"Timed out waiting for elements to load on page {page_number}. Error: {e}")
        return False  # Return False to indicate that the download was not successful

    # Find all image elements on the page using the By.TAG_NAME method
    images = driver.find_elements(By.TAG_NAME, 'img')

    # Create a subdirectory for each page
    page_directory = os.path.join(main_directory, f"page_{page_number}")

    if not os.path.exists(page_directory):
        os.makedirs(page_directory)

    for i, image in enumerate(images):
        # Get the source URL of the image
        image_url = image.get_attribute('src')

        # Download the image into the subdirectory
        response = requests.get(image_url)
        if not os.path.exists(os.path.join(page_directory, f"image_{i+1}.jpg")):
            with open(os.path.join(page_directory, f"image_{i+1}.jpg"), "wb") as file:
                file.write(response.content)

    return True  # Return True to indicate a successful download
'''

# Function to download images from a given URL
def download_images(url, page_number):
    driver.get(url)
    time.sleep(2)  # Give the page some time to load

    # Attempt to handle the login window (close it if it appears)
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'iconfont.passport-close'))
        )
        close_button.click()  # Click on the close button
        print("Login window closed.")
        time.sleep(3)
        print("Waited for 3 seconds for the page to load.")
    except:
        pass

    # Simulate scrolling to trigger lazy-loading
    for _ in range(3):  # Adjust the number of scrolls as needed
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

    # Wait for lazy-loaded images to be fully loaded
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'lazyload_hk.ll_loaded'))
        )
    except Exception as e:
        print(f"Timed out waiting for elements to load on page {page_number}. Error: {e}")
        return False  # Return False to indicate that the download was not successful

    # Find all image elements on the page using the By.TAG_NAME method
    images = driver.find_elements(By.TAG_NAME, 'img')

    # Create a subdirectory for each page
    page_directory = os.path.join(main_directory, f"page_{page_number}")

    if not os.path.exists(page_directory):
        os.makedirs(page_directory)

    for i, image in enumerate(images):
        # Get the source URL of the image
        image_url = image.get_attribute('src')

        # Construct the filename for the image
        image_filename = f"image_{i+1}.jpg"

        # Check if the image file already exists
        if not os.path.exists(os.path.join(page_directory, image_filename)):
            # Download the image into the subdirectory
            response = requests.get(image_url)
            
            print(image_url)
            
            with open(os.path.join(page_directory, image_filename), "wb") as file:
                file.write(response.content)
            
            print(f"Downloaded: {image_filename}")
        else:
            print(f"Skipped (Already Exists): {image_filename}")

    return True  # Return True to indicate a successful download

# Keep track of the last successfully processed page
last_successful_page = 0

# Loop through each page and download images
for page in range(1, num_pages + 1):
    url = base_url.format(page)
    success = download_images(url, page)

    if success:
        last_successful_page = page
        print(f"Page {page} successfully processed.")
        download_percentage = page / num_pages * 100
        print(f"Download percentage: {download_percentage:.2f}%")
    else:
        print(f"Resuming from the last successful page: {last_successful_page}")
        break

# Close the webdriver
driver.quit()
