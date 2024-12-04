# Description: This script is used to adjust and clean the image info to the formal format.
# 1. Downloaded images number should be the same as the stored image info.
# Adjust the image info to the formal format


import os
import json

class DataFormat:
    def __init__(self, download_dir):
        self.download_dir = download_dir

    # Image info id continuity check is done in the scraper itself
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
    # TODO: Add more functions to adjust the image info