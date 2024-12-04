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

    def scrape_page(self, page): # Scrape a single page and extract image info
        url = f"https://www.flickr.com/search?text={self.search_text}&structured=yes&page={page}"
        file_pointer = urllib.request.urlopen(url)
        page_content = file_pointer.read().decode("utf8")
        file_pointer.close()
        self.extract_image_info(page_content)
    
    def scrape_start_end_page(self, start_page, end_page):
        for page in range(start_page, end_page + 1):
            self.scrape_page(page)
        self.download_images()

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


        # self.remove_invalid_url_and_update_file()


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
                try:
                    image_info_line = json.loads(line.strip().rstrip(','))
                    url = image_info_line["url"]
                    if url in urls_in_file:
                        print(f"Duplicate URL found: {url}")
                        duplicate_flag = True
                    else:
                        urls_in_file.add(url)
                except json.JSONDecodeError as e:
                    print(f"Failed to parse JSON line: {line}. Error: {e}")
            if duplicate_flag:
                print("Removing duplicate image info")
                self.remove_duplicate_image_info()
            else:
                print("No duplicate URLs found")
                print(f"Total URLs: {len(urls_in_file)}")

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
        unique_image_info_line_list = []
        
        for line in lines:
            try:
                # Remove trailing commas and ensure each line is a valid JSON object
                line = line.strip().rstrip(',')
                image_info_line = json.loads(line)
                entry = (
                    image_info_line["license"],
                    image_info_line["file_name"],
                    image_info_line["height"],
                    image_info_line["width"],
                    image_info_line["url"]
                )
                if entry not in unique_entries:
                    unique_entries.add(entry)
                    unique_image_info_line_list.append(image_info)
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON line: {line}. Error: {e}")
        
        # Write back only the unique entries to the file
        with open(os.path.join(self.download_dir, "image_info.json"), "w") as f:
            for image_info in unique_image_info_line_list:
                json.dump(image_info, f)
                f.write("\n")
        
        print(f"Removed duplicates. Total unique entries: {len(unique_image_info_line_list)}")
    
    def remove_invalid_url_and_update_file(self):
        # Read all lines from "image_info.json"
        with open(os.path.join(self.download_dir, "image_info.json"), "r") as f:
            lines = f.readlines()
        
        valid_lines = []
        for line in lines:
            # Split the line by newline to handle multiple JSON objects in a single line
            json_objects = line.strip().split('\n')
            for json_object in json_objects:
                try:
                    image_info_line = json.loads(json_object)
                    if "https://live.staticflickr.com/" in image_info_line["url"]:
                        valid_lines.append(json.dumps(image_info_line) + '\n')
                    else:
                        print(f"Invalid URL: {image_info_line['url']}")
                except json.JSONDecodeError as e:
                    print(f"Remove invalid url. Failed to parse JSON line: {json_object}. Error: {e}")
        
        # Write back the updated entries to the file
        with open(os.path.join(self.download_dir, "image_info.json"), "w") as f:
            for line in valid_lines:
                f.write(line)
        
        print("Removed invalid URLs and updated the file.")

    def image_info_id_check(self):
        # Check if the "id" field in "image_info.json" is continuous
        with open(os.path.join(self.download_dir, "image_info.json"), "r") as f:
            lines = f.readlines()
        
        image_info_list = []
        for line in lines:
            try:
                # Remove trailing commas and ensure each line is a valid JSON object
                line = line.strip().rstrip(',')
                image_info_line = json.loads(line)
                image_info_list.append(image_info_line)
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON line: {line}. Error: {e}")
        
        # Ensure "id" is continuous
        current_id = 1
        for image_info_line in image_info_list:
            if image_info_line["id"] != current_id:
                image_info_line["id"] = current_id
            current_id += 1
        
        # Write back the updated entries to the file
        with open(os.path.join(self.download_dir, "image_info.json"), "w") as f:
            for image_info_line in image_info_list:
                json.dump(image_info_line, f)
                f.write("\n")
        
        print(f"Checked and updated IDs. Total entries: {len(image_info_list)}")


if __name__ == "__main__":
    search_text = "usb+stick"
    download_dir = f"/home/tianyu/Projects/DatasetExpand/downloads_flickr/{search_text}"
    pages = 50 # Number of pages to scrape
    scraper = FlickrScraper(download_dir, search_text, pages)
    # scraper.scrape()
    # scraper.scrape_start_end_page(51, 52)
    scraper.duplicate_image_info_check_and_remove()
    scraper.image_info_id_check()