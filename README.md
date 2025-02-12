<!-- # DatasetExpand
Search images online and record their sources and licenses. Format similar to COCO dataset.

COCO annotations are inside the folder "annotations_COCO2017". The file "image_info_test2017_cut.json" is a shortened version with all necessary info to create a record for new datasets, the file "office_objects_image_info.json" in this folder is used as template to record all collected images information.

The folder "downloads_flickr" contains 8 object categories that are used in the project. In each category, two JSON files are included. For the file "image_info.json", it contains all images that the scraper found on Flickr. For the second file ended with "_filtered.json", e.g. "image_info_filtered.json", it contains images that are manually selected from all images.

The downloaded images were not uploaded onto GitHub due to the size restriction. The dataset with filtered images can be found on Roboflow (https://universe.roboflow.com/creatingmasks/office-objects-cjjon) -->

# DatasetExpand
This repository is designed to search for images online, download them, and record their sources and licenses. The dataset is structured in a format similar to the **COCO dataset**, making it compatible with existing tools and workflows for object detection and image annotation.

---

## Repository Structure and Purpose

### COCO Annotations
The folder `annotations_COCO2017` contains COCO-style annotations:
- `image_info_test2017_cut.json`: A shortened version of the COCO annotations, containing all necessary information to create a record for new datasets.
- `office_objects_image_info.json`: A template file used to record information about all collected images.

### Downloaded Images
The folder `downloads_flickr` contains 8 object categories used in the project. Each category includes:
- `image_info.json`: Contains metadata for all images found on Flickr by the scraper.
- `image_info_filtered.json`: Contains metadata for images that were manually selected from the full set.

**Note**: Due to GitHub's size restrictions, the actual downloaded images are not uploaded to this repository. The filtered dataset can be accessed on **Roboflow**:
- [Office Objects Dataset on Roboflow](https://universe.roboflow.com/creatingmasks/office-objects-cjjon)

---
<!-- # Usage
Run "flickr_scraper_noapi_object_oriented.py", a new folder (mainfolder) will show up at the path location according to variable "download_dir". Every object has its own folder and will be automatically created. In each subfolder (object), the file "image_info.json" records all needed image information. -->

## How to Use
Run `flickr_scraper_noapi_object_oriented.py`. After execution, a new folder named **downloads_flickr** will be created at the path location specified by the `download_dir` variable. Inside this folder, each object will have its own subfolder, which is automatically created. Within each subfolder (object), a file named `image_info.json` is generated, containing all the necessary information about the downloaded images.

---

<!-- "Scraper_Selenium_new.py" and "search_beautifulsoup.py" use  -->
## File Descriptions

### `Scraper_Selenium_new.py`
This script utilizes **Selenium** to automate web browsing and perform image searches on the **VCG website**. It is capable of navigating the website, searching for images, and downloading them. Selenium is used to handle dynamic content and interact with web elements, making it suitable for websites that rely heavily on JavaScript.

**Dependency:**
- **Selenium**: A powerful tool for browser automation and web scraping.

---

### `search_beautifulsoup.py`
This script employs **BeautifulSoup** to parse HTML content and extract image data from **Flickr**. It searches for images based on specified criteria and downloads them. BeautifulSoup is ideal for parsing static HTML content and extracting information efficiently.

**Dependency:**
- **BeautifulSoup**: A Python library for parsing HTML and XML documents, often used for web scraping.

---

### Common Functionality
Both scripts are designed to search for and download images from their respective websites. While `Scraper_Selenium_new.py` is tailored for websites like VCG, `search_beautifulsoup.py` is optimized for contents on Flickr.

## Questions/Future Work
* Is it possible to choose/pick pictures from COCO dataset (91 categories?) and use them in the dirt-objects dataset?
* ImageNet Large Scale Visual Recognition Challenge 2017 (ILSVRC2017)?