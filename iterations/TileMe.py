from PIL import Image, ImageFilter

def make_tileable(image_path, output_name):
    # Open the original image
    image = Image.open("C:\\Users\\sophi\\OneDrive\\Desktop\\TileMe\\e14b6a6f2bdb023a3e8a3768bc41d2d7.jpg")
    
    # Create a new image with double the width and height of the original
    width, height = image.size
    new_image = Image.new('RGB', (width * 2, height * 2))
    
    # Place the original image at the four corners of the new image
    print("width: " + str(width))
    new_image.paste(image, (0, 0))
    new_image.paste(image, (width - 100, 0))
    new_image.paste(image, (0, height))
    new_image.paste(image, (width, height))
    
    # Crop the new image back to the original size
    new_image = new_image.crop((width//2, height//2, width//2 + width, height//2 + height))
    
    # Save the tileable image
    new_image.save(output_name)

# Usage example
make_tileable('input_image.jpg', 'output_tileable_image.jpg')
 
