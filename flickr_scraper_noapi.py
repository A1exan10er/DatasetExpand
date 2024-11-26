import urllib.request
import os
import numpy as np
import datetime

# Make directory to store downloaded images
download_dir = "/home/tianyu/Projects/DatasetExpand/downloads"
os.makedirs(download_dir, exist_ok=True)
urls = [] # List to store image URLs
image_id = len(os.listdir(download_dir)) + 1 # ID for each image
last_image_info = None # Store the last image info to avoid saving duplicate information for the same image

# TODO: Add a loop to scrape multiple pages
# Example page number
page = 2

file_pointer = urllib.request.urlopen(f"https://www.flickr.com/search?text=usb+stick&structured=yes&page={page}")
str = file_pointer.read().decode("utf8") # decode the byte string to a normal string
file_pointer.close()

# # Save str to a file for debugging
# with open("flickr_search.html", "w") as f:
#     f.write(str)

# Example key-value pair
# {"data":{"_flickrModelRegistry":"photo-lite-models","pathAlias":"osde-info","username":"osde8info","ownerNsid":"8764442@N07","title":"google usb stick","description":"google usb stick","license":5,"sizes":{"data":{"sq":{"data":{"displayUrl":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_s.jpg","width":75,"height":75,"url":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_s.jpg"},"exportMetaType":"pojo"},"q":{"data":{"displayUrl":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_q.jpg","width":150,"height":150,"url":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_q.jpg"},"exportMetaType":"pojo"},"t":{"data":{"displayUrl":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_t.jpg","width":100,"height":75,"url":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_t.jpg"},"exportMetaType":"pojo"},"s":{"data":{"displayUrl":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_m.jpg","width":240,"height":180,"url":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_m.jpg"},"exportMetaType":"pojo"},"n":{"data":{"displayUrl":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_n.jpg","width":320,"height":240,"url":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_n.jpg"},"exportMetaType":"pojo"},"w":{"data":{"displayUrl":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_w.jpg","width":400,"height":300,"url":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_w.jpg"},"exportMetaType":"pojo"},"m":{"data":{"displayUrl":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2.jpg","width":500,"height":375,"url":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2.jpg"},"exportMetaType":"pojo"},"z":{"data":{"displayUrl":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_z.jpg","width":640,"height":480,"url":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_z.jpg"},"exportMetaType":"pojo"},"c":{"data":{"displayUrl":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_c.jpg","width":800,"height":600,"url":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_c.jpg"},"exportMetaType":"pojo"},"l":{"data":{"displayUrl":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_b.jpg","width":1024,"height":768,"url":"\/\/live.staticflickr.com\/2258\/2264029202_a8f87bced2_b.jpg"},"exportMetaType":"pojo"}},"exportMetaType":"pojo"},"canComment":false,"isPublic":true,"reactions":{"data":{"like":{"data":{"id":"like","count":5,"didViewerReact":false,"canReact":true},"exportMetaType":"pojo"},"someOtherReaction":{"data":{"id":"someOtherReaction","count":3,"didViewerReact":false,"canReact":true},"exportMetaType":"pojo"}},"exportMetaType":"pojo"},"id":"2264029202"},"exportMetaType":"model"}, ...

# Find all image URLs
url_index_results = [index for index in range(len(str)) if str.startswith("_b.jpg", index)] # url_index_results type: list, store the index of "_b.jpg"
# print(url_index_results)

last_image_url = None
for i in url_index_results:
    # Example key-value pair: "displayUrl":"\/\/live.staticflickr.com\/4664\/39077172375_dcb060fbda_b.jpg"
    # A second key-value pair: "url":"\/\/live.staticflickr.com\/4664\/39077172375_dcb060fbda_b.jpg"
    image_url = "https://" + str[i - 70 : i + 6].replace("\\", "").split("//")[-1] # "i - 70" is the start of the key-value pair and "i + 6" is the end of the key-value pair
                                                                                   # replace("\\", ""): remove the backslash
                                                                                   # split("//")[-1]: get the second part of the split string
    # Problem: license saved twice for the same image
    # Solution: save license only if the image URL is different from the last image URL
    if image_url != last_image_url: # Check if the image URL is different from the last image URL
                                    # Purpose: avoid saving duplicate information for the same image
        urls.append(image_url)
        last_image_url = image_url
        
        # Add license info
        license_index = str.rfind("license", 0, i) # Find the last occurrence of "license" before the image URL
        license_number = str[license_index + 9 : str.find(",", license_index)] # "license" is 7 characters long, so the license number is at index "license_index + 9"

        # Link example: \/\/live.staticflickr.com\/65535\/51825930028_f35ff417d2_b.jpg
        file_name = image_url.split("/")[-1] # Get the file name from the image URL, which is the last part of the URL
        height_index = str.find("height", i) # Find the index of "height" after the image URL
        height = str[height_index + 8 : str.find(",", height_index)] # "height" is 6 characters long, so the height number is at index "height_index + 8"
        width_index = str.find("width", i) # Find the index of "width" after the image URL
        width = str[width_index + 7 : str.find(",", width_index)] # "width" is 5 characters long, so the width number is at index "width_index + 7"

        # date_captured example: "date_captured": "2013-11-14 11:04:33", system date and time
        date_captured = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        image_info = f"{{\"license\":{license_number},\"file_name\":\"{file_name}\",\"height\":{height},\"width\":{width},\"url\":\"{image_url}\",\"date_captured\":\"{date_captured}\",\"id\":{image_id}}},"
        # Example: "id": 308929
        image_id += 1

    # # Write license, file name, height, width, image URL, date_captured, id to a JSON file
    # with open("image_info.json", "a") as f:
    #     f.write(f"{{\"license\":{license_number},\"file_name\":\"{file_name}\",\"height\":{height},\"width\":{width},\"url\":\"{image_url}\",\"date_captured\":\"{date_captured}\",\"id\":{image_id}}},\n")
    # Write image_info to a JSON file
    with open(os.path.join(download_dir, "image_info.json"), "a") as f:
        if image_info != last_image_info:
            f.write(image_info + "\n")
            last_image_info = image_info

# urls = list(np.unique(np.array(urls)))
# print(len(urls), urls)
print(len(urls))

# Download images
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