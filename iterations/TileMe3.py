from PIL import Image, ImageFilter

def make_tileable(image_path, output):
    # Open the original image
    # image = Image.open("C:\\Users\\sophi\\OneDrive\\Desktop\\TileMe\\bark.jpg")
    image = Image.open("C:\\Users\\sophi\\OneDrive\\Desktop\\TileMe\\concept.jpg")
    # image = Image.open("C:\\Users\\sophi\\OneDrive\\Desktop\\TileMe\\appa.jpg")
    

    # def crop_and_make_canvas():
        # Create a new image with double the width and height of the original. Make sure the image is a square.
    width, height = image.size
    if(width < height):
        new_image = Image.new('RGB', (width * 2, width * 2))
        # im1 = im.crop((left, top, right, bottom))
        image = image.crop((0 , (height-width)//2 ,width , height - (height-width)//2 ))
        # image.show()
        height = width
    elif(width > height):
        new_image = Image.new('RGB', (height * 2, height * 2))
        # im1 = im.crop((left, top, right, bottom))
        image = image.crop((  (width - height)//2 , 0 , width - ((width - height)//2), height  ))
        # image.show()
        width = height
    elif(width == height):
        new_image = Image.new('RGB', (width * 2, height * 2))
            
    # make n

    
    # Place the original image at the four corners of the new image
    
    new_image.paste(image, (0, 0))
    new_image.paste(image, (width - 100, 0))
    new_image.paste(image, (0, height))
    new_image.paste(image, (width, height))
    
    # Crop the new image back to the original size
    new_image = new_image.crop((width//2, height//2, width//2 + width, height//2 + height))
    
    # Save the tileable image
    new_image.save(output)

# Usage example
# crop_and_make_canvas()
make_tileable('input_image.jpg', 'output_tileable_image.jpg')

