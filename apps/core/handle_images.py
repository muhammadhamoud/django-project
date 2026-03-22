# from django.core.files import File
# from io import BytesIO
# from PIL import Image

# def compress_image(image):
#     img = Image.open(image)
#     img_io = BytesIO()
#     if img.mode != "RGB":
#         img = img.convert("RGB")
#     img.save(img_io, format="JPEG", quality=70, optimize=True)
#     new_img = File(img_io, name=image.name)
    
#     return new_img


from django.core.files import File
from io import BytesIO
from PIL import Image
import os

def compress_image(image):
    """
    Compresses and resizes an image to have a maximum width or height of 600 pixels while maintaining its aspect ratio.
    
    Parameters:
        image (FieldFile): The image file object.
    
    Returns:
        File: The compressed and resized image file object.
    """
    try:
        # Open the image using Pillow
        with Image.open(image) as img:
        
            # Resize the image while maintaining aspect ratio
            img.thumbnail((600, 600))
            
            # Ensure the mode is "RGB" for JPEG format
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            # Create an in-memory stream to store the compressed image
            img_io = BytesIO()
            
            # Save the resized image to the in-memory stream with JPEG format and quality
            img.save(img_io, format="JPEG", quality=70, optimize=True)
            
            
            # Create a Django File object from the in-memory stream
            new_img = File(img_io, name=image.name)
           
        
        # Delete the original image file
        try:
            # Close the original image file handle
            image.close()
            os.remove(image.path)
        except OSError as e:
            print(f"Error deleting original image: {e}")
        
        return new_img
    
    except Exception as e:
        # print(f"Error compressing image: {e}")
        return None
