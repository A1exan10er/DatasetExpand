from flickrapi import FlickrAPI

from api_keys import flickr_keys

key, secret = flickr_keys.values()

flickr = FlickrAPI(
                key, 
                secret, 
                format='parsed-json'
                )


# All the extra data that I want to have
extras='owner_name,license,geo,description,url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'

images = flickr.photos.search(
    text='USB sticks', # Search term
    per_page=5, # Number of results per page
    license='4,5,6,7,8,9,10',  # Attribution Licenses
    extras=extras, 
    privacy_filter=1, #public photos
    safe_search=1 # is safe
    )

print(images)