from PIL import Image

def blend_image(image_path):
    # Open the image
    img = Image.open(image_path)
    
    # Get image dimensions
    width, height = img.size
    
    # Split the image into two halves
    half_width = width // 2
    fourth_width = width // 4
    
    # Create a new image with the same dimensions and mode
    blended_img = Image.new(img.mode, img.size)
    
    # Iterate over each pixel and blend the halves
    for x in range(width):


        for y in range(height):
            if x < half_width:
            	blended_img.putpixel((x,y), img.getpixel((x,y)) )

            if x<half_width:
        		print("what")

    		# if x < half_width + fourth_width && x > width - fourth_width:
        		# blended_img.putpixel((x,y), (225,225,225))


			    #     p = x / half_width
			    #     opacity = 1 - p
			    # else:
			    #     p = (x - half_width) / half_width
			    #     opacity = p
            
            	# Get pixel values from both halves
        		# pixel_left = img.getpixel((x, y))
        		# pixel_right = img.getpixel((x - half_width, y))

            
            # Blend pixel values using the opacity function
            # blended_pixel = tuple(int((1 - opacity) * c_left + opacity * c_right) for c_left, c_right in zip(pixel_left, pixel_right))
        		# blended_img.putpixel((x,y), img.getpixel((x, y)) )
        # 	test_pixel = (1,1,1)
        # 	blended_img.putpixel((x,y), test_pixel)
    		# blended_img.putpixel((x, y), test_pixel)

            
            # # Update blended image
            # blended_img.putpixel((x, y), blended_pixel)


    # Save or show the blended image
    blended_img.show()

# Example usage
blend_image("C:\\Users\\sophi\\OneDrive\\Desktop\\TileMe\\Tile-Me\\appa_tiled.jpg")
