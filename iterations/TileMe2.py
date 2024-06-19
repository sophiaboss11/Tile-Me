from PIL import Image, ImageFilter, ImageChops, ImageOps
# from PIL import *

def make_tileable(image_path, output_path):
    # Open the original image
    # image = Image.open(image_path)
    image = Image.open("C:\\Users\\sophi\\OneDrive\\Desktop\\TileMe\\e14b6a6f2bdb023a3e8a3768bc41d2d7.jpg")
    
    
    # Create mirrored edges
    width, height = image.size
    left = image.crop((0, 0, width // 2, height))
    right = image.crop((width // 2, 0, width, height))
    top = image.crop((0, 0, width, height // 2))
    bottom = image.crop((0, height // 2, width, height))

    # Mirror the edges
    left = ImageOps.mirror(left)
    right = ImageOps.mirror(right)
    top = ImageOps.mirror(top)
    bottom = ImageOps.mirror(bottom)

    # Paste mirrored edges onto the opposite sides of the image
    image.paste(left, (width // 2, 0))
    image.paste(right, (0, 0))
    image.paste(top, (0, height // 2))
    image.paste(bottom, (0, 0))

    # Apply a Gaussian Blur to smooth the seams
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=10))

    # Crop back to the original size
    blurred_image = blurred_image.crop((width // 4, height // 4, width * 3 // 4, height * 3 // 4))
    blurred_image = blurred_image.resize((width, height))

    # Save the tileable image
    blurred_image.save(output_path)

# Usage example
make_tileable('input_image.jpg', 'output_tileable_image.jpg')
