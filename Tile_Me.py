import maya.api.OpenMaya as om
import maya.cmds as cmds
import os, stat, sys


print(sys.executable)
# -- TODO -- make the install location automatic
# run a shell script??
# sys.path.append( 'C:/Users/sophi/AppData/Local/Programs/Python/Python37/Lib/site-packages' )
print(sys.path)
try:
    from PIL import Image
    print("import succeeded")
except:
    print("import failed")



def calculate_opacity(r1, r2, p):
    """
    Calculate the opacity of two pixels based on the formula f((1-p)R + p(R))R1.
    """
    opacity = tuple(int((1 - p) * c1 + p * c2) for c1, c2 in zip(r1, r2))
    return opacity

def blend_image(tiled_image):
    # Open the image
    # img = Image.open(image_path)

    img = tiled_image
    # Get image dimensions
    width, height = img.size
    
    # Split the image into two halves
    half_width = width // 2
    fourth_width = width // 4
    half_height = height // 2
    fourth_height = height // 4
    print("image width: " + str(width))

    stretch_area = half_width * height
    # print(stretch_area)
    # stretch_area_heig = half_width * height
    
    
    # Create a new image with the same dimensions and mode
    blended_img = Image.new(img.mode, img.size)
    blended_img2 = Image.new(img.mode, img.size)
    blended_img3 = Image.new(img.mode, img.size)
    blended_img4 = Image.new(img.mode, img.size)
    
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
    
    print("stretched x right: " + str(stretched_x))
    print(x)
    # print(stretch_area)

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
      
    count = 0

    # bottom to top stretch
    for x in range(width):
        # print(x)
        for y in range(height):
            if y > half_height:
                blended_img3.putpixel((x,y), blended_img.getpixel((x,y)))
            # stretch image
            if y > fourth_height and y < height - fourth_height:
                # print(count)
                # stretched_y = int( y * (1 + (count/ 150000))) 
                # sa = 64261    50219
                stretched_y = int( (y) / (1 + (count / (stretch_area )))) 

                # print(stretched_y)
                # getPixel = blended_img.getpixel((x , stretched_y ))
                blended_img3.putpixel((x,y), getPixel )
                count += 1
    
    
    # print(stretch_area)
    print("stretched y bottom: " + str(stretched_y))
    print(y)
    blended_img3.show()
    return blended_img

def make_tileable(image_path): 
    folder = image_path.rsplit("/", 1)[0]

    # os.makedirs(os.path.dirname(image_path), exist_ok=True)
    os.makedirs(os.path.dirname(folder), exist_ok=True)

    #TODO: check to make sure its an image 
    image = Image.open(image_path)

    # Create a new image with double the width and height of the original. Make sure the image is a square.
    width, height = image.size
    if(width < height):
        new_image = Image.new('RGB', (width * 2, width * 2))
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
    
    # Place the original image at the four corners of the new image
    
    new_image.paste(image, (0, 0))
    new_image.paste(image, (width, 0))
    new_image.paste(image, (0, height))
    new_image.paste(image, (width, height))
    
    # Crop the new image back to the original size
    new_image = new_image.crop((width//2, height//2, width//2 + width, height//2 + height))
    # image = Image.new('RGB', (width, height), color)



    
    # Save the tileable image
    # newDir = 'C:/Users/sophi/OneDrive/Desktop/TileMe/Tile-Me/out.png'
    # image.save("retry.jpg")
    # TODO -- MAKE SURE SAME EXTENSION
    new_image = blend_image(new_image)
    out_name = "/tiled_" + image_path.rsplit("/", 1)[1] 
    print(out_name)
    new_image.save(folder + out_name)  
    # new_image.show()



def maya_useNewAPI():
    pass


class TileMe(om.MPxCommand):
    COMMAND_NAME = "tileme"

    def __init__(self):
        super(TileMe, self).__init__()


    def doIt(self, args):

        # get file location of selected image > get all selected
        selected = cmds.ls(sl=True,long=True) or []
        print("selected objects: " + str(selected[0]))
        attribute = selected[0]
        print("attribute: " + str(attribute))
        # works for pcone object
        # attribute = attribute + ".translateX"
        # location = cmds.getAttr(attribute)

        # get Mobject? check Mimage.writeToFile

        attribute = attribute + ".fileTextureName"
        location = cmds.getAttr(attribute)

        # print("attribute list: " + str(cmds.listAttr( r=True, s=True )))
           # TODO fix for all file types

        print( "selected attribute location: " + str(location))
        folder = location.rsplit("/", 1)
        folder = folder[0] 
        print(folder)
        os.makedirs(os.path.dirname(folder), exist_ok=True)

        # Example usage
        file_location = 'C:/Users/sophi/OneDrive/Desktop/TileMe/Tile-Me/empty_image.png'
        image_width = 800
        image_height = 600
        # create_empty_image(file_location, image_width, image_height)

        make_tileable( location )

    @classmethod 
    def creator(cls):
        return TileMe()


def initializePlugin(plugin):
    print("---TileMe plugin initialized---")
    vendor = "SB"
    version = "1.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)

    try:
        plugin_fn.registerCommand(TileMe.COMMAND_NAME, TileMe.creator)
    except:
        om.MGLobal.displayError("Failed to register command".format(TileMe))




def uninitializePlugin(plugin):
    # pass
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(TileMe.COMMAND_NAME)
    except:
        om.MGLobal.displayError("failed to deregister".format(TileMe))

if __name__ == "__main__":
    plugin_name = "Tile_Me.py"

    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.aloadPlugin("{0}")'.format(plugin_name))