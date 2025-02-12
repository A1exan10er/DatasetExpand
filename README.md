# DatasetExpand
Search images online and record their sources and licenses. Format similar to COCO dataset.

COCO annotations are inside the folder "annotations_COCO2017". The file "image_info_test2017_cut.json" is a shortened version with all necessary info to create a record for new datasets, the file "office_objects_image_info.json" in this folder is used as template to record all collected images information.

The folder "downloads_flickr" contains 8 object categories that are used in the project. In each category, two JSON files are included. For the file "image_info.json", it contains all images that the scraper found on Flickr. For the second file ended with "_filtered.json", e.g. "image_info_filtered.json", it contains images that are manually selected from all images.

The downloaded images were not uploaded onto GitHub due to the size restriction. The dataset with filtered images can be found on Roboflow (https://universe.roboflow.com/creatingmasks/office-objects-cjjon)

# Usage
Run "flickr_scraper_noapi_object_oriented.py", a new folder (mainfolder) will show up at the path location according to variable "download_dir". Every object has its own folder and will be automatically created. In each subfolder (object), the file "image_info.json" records all needed image information.

# Questions/Future Work
* Is it possible to choose/pick pictures from COCO dataset (91 categories?) and use them in the dirt-objects dataset?
* ImageNet Large Scale Visual Recognition Challenge 2017 (ILSVRC2017)?