# Description: This script is used to adjust and clean the image info into the formal format.
# 1. Clean image info file: Remove the image info that does not have the corresponding image
# 2. (Optional) Check the image info id continuity: Ensure the "id" field in "image_info.json" is continuous
# 3. Adjust the image info to the formal format (COCO)


import os
import json

class DataFormat:
    def __init__(self, download_dir):
        self.download_dir = download_dir

    # Filter out the image info that does not have the corresponding image
    def filter_image_info(self):
        # Read the image info
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
        
        # Filter out the image info that does not have the corresponding image
        image_info_list_filtered = []
        for image_info_line in image_info_list:
            image_path = os.path.join(self.download_dir, f"{image_info_line['file_name']}")
            if os.path.exists(image_path):
                image_info_list_filtered.append(image_info_line)
            else:
                print(f"Image not found for : {image_info_line['file_name']}")
        
        # Write back the filtered entries to a new file
        with open(os.path.join(self.download_dir, "image_info_filtered.json"), "w") as f:
            for image_info_line in image_info_list_filtered:
                json.dump(image_info_line, f)
                f.write("\n")
        
        print(f"Filtered out image info. Total entries: {len(image_info_list_filtered)}")
        # Filtered image info id is not continuous because the id comes from the image info file that contains all the images
    
    # Image info id continuity check is done in the scraper itself. 
    # The image info file that contains all images (before filtering) should have continuous ids.
'''    def image_info_id_check(self):
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
        
        print(f"Checked and updated IDs. Total entries: {len(image_info_list)}")'''

if __name__ == "__main__":
    search_text = input("Enter the search text: ")
    download_dir = f"/home/tianyu/Projects/DatasetExpand/downloads_flickr/{search_text}"
    corrector = DataFormat(download_dir)
    corrector.filter_image_info()
    # TODO: Add more functions to adjust the image info according to needs