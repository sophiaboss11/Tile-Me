from PIL import Image
def calculate_opacity(r1, r2, p):
    """
    Calculate the opacity of two pixels based on the formula f((1-p)R + p(R))R1.
    """
    opacity = tuple(int((1 - p) * c1 + p * c2) for c1, c2 in zip(r1, r2))
    return opacity

def blend_image(image_path):
    # Open the image
    img = Image.open(image_path)
    
    # Get image dimensions
    width, height = img.size
    
    # Split the image into two halves
    half_width = width // 2
    fourth_width = width // 4

    stretch_area = half_width * height
    
    
    # Create a new image with the same dimensions and mode
    blended_img = Image.new(img.mode, img.size)
    blended_img2 = Image.new(img.mode, img.size)
    
    count = 0

    # Right to left stretch
    for x in reversed(range(width)):
        # print(x)
        for y in range(height):
            if x > half_width:
                blended_img2.putpixel((x,y), img.getpixel((x,y)))
            # stretch image
            if x > fourth_width and x < width - fourth_width:
                # stretched_x = int(x - ((count/stretch_area) * stretch_area))
                stretched_x = int((x ) * ((1 + (count/stretch_area))))

                getPixel = img.getpixel((stretched_x , y))
                blended_img2.putpixel((x,y), getPixel)
                count += 1
    count = 0
    # Left to right stretch
    for x in range(width):
        for y in range(height):

            getPixel = img.getpixel(( x , y))
            if x < half_width:
                blended_img.putpixel((x,y), img.getpixel((x,y)))
                p=0
            # stretch image
            if x > fourth_width and x < width - fourth_width:
                stretched_x = int(x / ((1 + (count/stretch_area))))
                # stretched_x = int(x * (count/stretch_area))
                
                count += 1

                getPixel = img.getpixel(( stretched_x , y))

                p= count/stretch_area
            # set opacity to 1 on the right side of the image
            elif x > width - fourth_width:
                p= 1
            # print(p)
            right_pixel = blended_img2.getpixel((x,y))
            featherPixel = calculate_opacity(getPixel, right_pixel, p )
            # featherPixel = calculate_opacity((225,225,225), (0,0,0), 0.5)

            blended_img.putpixel((x,y), featherPixel)
            # blended_img.putpixel((x,y), getPixel)
            # Reset count for the next loop
            # count = 0

            
            # calculate_opacity

    # blend image 1 and image 2 using calculate_opacity
    # for x in range(width):
    #     for y in range(height):
    #         p = x / width
    #         blended_img.putpixel((x,y), calculate_opacity(blended_img.getpixel((x,y)), blended_img2.getpixel((x,y)), p))


    blended_img.show()

blend_image("C:\\Users\\sophi\\OneDrive\\Desktop\\TileMe\\Tile-Me\\appa_tiled.jpg")
