import urllib.request
import os
import numpy as np

urls = [] # List to store image URLs

# Example page number
page = 2

file_pointer = urllib.request.urlopen(f"https://www.flickr.com/search?text=usb+stick&structured=yes&page={page}")
str = file_pointer.read().decode("utf8")
file_pointer.close()

res = [i for i in range(len(str)) if str.startswith("_b.jpg", i)] # Find all image URLs
for i in res:
    s = "https://" + str[i - 70 : i + 6].replace("\\", "").split("//")[-1]
    urls.append(s)

urls = list(np.unique(np.array(urls)))
print(len(urls), urls)

# Download images
download_dir = "/home/tianyu/Projects/DatasetExpand/downloads"
os.makedirs(download_dir, exist_ok=True)

for url in urls:
    try:
        image_name = os.path.join(download_dir, url.split("/")[-1])
        if os.path.exists(image_name):
            print(f"Image already exists: {image_name}")
            continue
        urllib.request.urlretrieve(url, image_name)
        print(f"Downloaded {image_name}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")