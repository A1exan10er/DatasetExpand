import json
import urllib.request
import os
import datetime

class FlickrScraper:
    def __init__(self, download_dir, search_text, pages):
        self.download_dir = download_dir
        self.search_text = search_text
        self.pages = pages
        self.urls = []
        os.makedirs(download_dir, exist_ok=True) # Create download directory, if it doesn't exist
        self.image_id = len(os.listdir(download_dir)) + 1
        self.last_image_info = None

    def scrape(self):
        for page in range(1, self.pages + 1):
            self.scrape_page(page)
        self.download_images()

    def scrape_page(self, page):
        url = f"https://www.flickr.com/search?text={self.search_text}&structured=yes&page={page}"
        file_pointer = urllib.request.urlopen(url)
        page_content = file_pointer.read().decode("utf8")
        file_pointer.close()
        self.extract_image_info(page_content)

    def extract_image_info(self, page_content):
        url_index_results = [index for index in range(len(page_content)) if page_content.startswith("_b.jpg", index)]
        last_image_url = None
        for i in url_index_results:
            image_url = "https://" + page_content[i - 70 : i + 6].replace("\\", "").split("//")[-1]
            if image_url != last_image_url:
                self.urls.append(image_url)
                last_image_url = image_url
                license_index = page_content.rfind("license", 0, i)
                # license_number = page_content[license_index + 9 : page_content.find(",", license_index)] # This line doesn't give the fixed length of the license, so it will sometimes grab too many characters
                license_number = page_content[license_index + 9 : license_index + 10]
                if not license_number.isdigit(): # Skip invalid license numbers (e.g., "license":E)
                    print(f"Invalid license number: {license_number}")
                    continue
                file_name = image_url.split("/")[-1]
                height_index = page_content.find("height", i)
                height = page_content[height_index + 8 : page_content.find(",", height_index)]
                width_index = page_content.find("width", i)
                width = page_content[width_index + 7 : page_content.find(",", width_index)]
                date_captured = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                image_info = f"{{\"license\":{license_number},\"file_name\":\"{file_name}\",\"height\":{height},\"width\":{width},\"url\":\"{image_url}\",\"date_captured\":\"{date_captured}\",\"id\":{self.image_id}}},"
                self.image_id += 1
                self.save_image_info(image_info)

    def save_image_info(self, image_info):
        with open(os.path.join(self.download_dir, "image_info.json"), "a") as f:
            if image_info != self.last_image_info:
                f.write(image_info + "\n")
                self.last_image_info = image_info
    
    # def create_download_dir(self):
    #     os.makedirs(self.download_dir, exist_ok=True)

    def download_images(self):
        for url in self.urls:
            try:
                image_name = os.path.join(self.download_dir, url.split("/")[-1])
                if os.path.exists(image_name):
                    print(f"Image already exists: {image_name}")
                    continue
                urllib.request.urlretrieve(url, image_name)
                print(f"Downloaded {image_name}")
            except Exception as e:
                print(f"Failed to download {url}: {e}")

    def duplicate_image_info_check_and_remove(self): # Check if duplicate image info is saved in "image_info.json"
        # "url" in "image_info.json" should be unique, if not, means the image info is duplicated
        with open(os.path.join(self.download_dir, "image_info.json"), "r") as f:
            image_info_file = f.read()
            urls_in_file = set() # Type: set, store unique URLs
            duplicate_flag = False
            for line in image_info_file.splitlines():
                if "\"url\":" in line: # Check if the line contains the key "url"
                    url_start = line.find("\"url\":") + 7 # +7 to skip the key '"url":'
                    url_end = line.find("\",", url_start) # "\", " is the end of the URL
                    url = line[url_start:url_end]
                    # print(url)
                    if url in urls_in_file:
                        print(f"Duplicate URL found: {url}")
                        duplicate_flag = True
                    else:
                        urls_in_file.add(url)
            if not duplicate_flag:
                print("No duplicate URLs found")
                print(f"Total URLs: {len(urls_in_file)}")
            else:
                # TODO: Remove duplicated image info from "image_info.json" and save the id of removed image info 
                print("Removing duplicate image info")
                self.remove_duplicate_image_info()

    # def remove_duplicate_image_info(self):
    #     # First, save all lines read from "image_info.json" to somewhere                
    #     # Second, only save the lines that are not duplicated, np.unique() can be used
    #     # Third, save the unique lines back to the file
    #     pass

    def remove_duplicate_image_info(self):
        # Read all lines from "image_info.json"
        with open(os.path.join(self.download_dir, "image_info.json"), "r") as f:
            lines = f.readlines()
        
        # Use a set to keep track of unique entries based on the specified fields
        unique_entries = set()
        unique_image_info_list = []
        
        for line in lines:
            try:
                # Remove trailing commas and ensure each line is a valid JSON object
                line = line.strip().rstrip(',')
                image_info = json.loads(line)
                entry = (
                    image_info["license"],
                    image_info["file_name"],
                    image_info["height"],
                    image_info["width"],
                    image_info["url"]
                )
                if entry not in unique_entries:
                    unique_entries.add(entry)
                    unique_image_info_list.append(image_info)
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON line: {line}. Error: {e}")
        
        # Write back only the unique entries to the file
        with open(os.path.join(self.download_dir, "image_info.json"), "w") as f:
            for image_info in unique_image_info_list:
                json.dump(image_info, f)
                f.write("\n")
        
        print(f"Removed duplicates. Total unique entries: {len(unique_image_info_list)}")

if __name__ == "__main__":
    search_text = "usb+stick"
    download_dir = f"/home/tianyu/Projects/DatasetExpand/downloads_flickr/{search_text}"
    pages = 6 # Number of pages to scrape
    scraper = FlickrScraper(download_dir, search_text, pages)
    scraper.scrape()
    scraper.duplicate_image_info_check_and_remove()
    # scraper.remove_duplicate_image_info()
