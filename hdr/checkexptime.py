from PIL import Image
from PIL.ExifTags import TAGS

def get_exposure_time(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    return exif_data
    # if exif_data is not None:
    #     for tag, value in :
    #         tag_name = TAGS.get(tag, tag)
    #         if tag_name == "ExposureTime":
    #             return value  # Returns the exposure time in seconds (as a fraction)
    return None

# Example usage
base_time = get_exposure_time('image1.jpg')
print("Base exposure time:", base_time)
