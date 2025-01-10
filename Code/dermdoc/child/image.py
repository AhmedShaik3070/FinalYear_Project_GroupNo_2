import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configuration       
cloudinary.config( 
    cloud_name = "dikgjuxny", 
    api_key = "374913428412357", 
    api_secret = "eGUU5evaHGFJZ1Aghra2ZHbM0UU", 
    secure=True
)

# Upload an image
def upload(image):
    upload_result = cloudinary.uploader.upload(image)
    return str(upload_result["secure_url"])
    # Optimize delivery by resizing and applying auto-format and auto-quality
    # optimize_url, _ = cloudinary_url("shoes", fetch_format="auto", quality="auto")
    # print(optimize_url)

# Transform the image: auto-crop to square aspect_ratio
# auto_crop_url, _ = cloudinary_url("shoes", width=500, height=500, crop="auto", gravity="auto")
# print(auto_crop_url)