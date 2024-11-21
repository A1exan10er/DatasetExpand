import urllib.request
import os
import numpy as np

urls = [] # List to store image URLs
license_list = [] # List to store license info

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
results = [i for i in range(len(str)) if str.startswith("_b.jpg", i)] # results type: list, store the index of "_b.jpg"
# print(results)
# license_index_list = [i for i in range(len(str)) if str.startswith("license", i)]
# print(license_index_list)
# license_list = []
# for i in license_index_list:
#     license_list.append(str[i + 9 : i + 10])
# print(license_list)
# print(len(results), len(license_list))
# if len(results) == len(license_index_list):
#     print(len(results), len(license_index_list))
# else:
#     print("Error: len(results) != len(license_index_list)")
#     print(len(results), len(license_index_list))

last_image_url = None
for i in results:
    # Example key-value pair: "displayUrl":"\/\/live.staticflickr.com\/4664\/39077172375_dcb060fbda_b.jpg"
    # A second key-value pair: "url":"\/\/live.staticflickr.com\/4664\/39077172375_dcb060fbda_b.jpg"
    image_url = "https://" + str[i - 70 : i + 6].replace("\\", "").split("//")[-1] # "i - 70" is the start of the key-value pair and "i + 6" is the end of the key-value pair
    if image_url != last_image_url:
        urls.append(image_url)
        last_image_url = image_url
        
        # Add license info
        license_index = str.rfind("license", 0, i) # Find the last occurrence of "license" before the image URL
        license_list.append(str[license_index + 9 : license_index + 10]) # "license" is 7 characters long, so the license number is at index "license_index + 9"
        # Problem: license saved twice for the same image
        # Solution: save license only if the image URL is different from the last image URL

        # Write license and image URL to a json file
        with open("image_info.json", "a") as f:
            f.write(f"{{\"license\":{str[license_index + 9 : license_index + 10]},\"url\":\"{image_url}\"}},\n")
        

urls = list(np.unique(np.array(urls)))
print(len(urls), urls)
print(len(license_list), license_list)


# # Download images
# download_dir = "/home/tianyu/Projects/DatasetExpand/downloads"
# os.makedirs(download_dir, exist_ok=True)

# for url in urls:
#     try:
#         image_name = os.path.join(download_dir, url.split("/")[-1])
#         if os.path.exists(image_name):
#             print(f"Image already exists: {image_name}")
#             continue
#         urllib.request.urlretrieve(url, image_name)
#         print(f"Downloaded {image_name}")
#     except Exception as e:
#         print(f"Failed to download {url}: {e}")