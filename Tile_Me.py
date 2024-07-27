
import maya.api.OpenMaya as om
import maya.cmds as cmds
import os, time, sys


'''
-- TODO -- make the install location automatic
ERROR handling. make lists selectable
make the import statement not repeat
run a shell script??
'''
# add in constructor and then deconstruct
sys.path.append( 'C:/Users/sophi/AppData/Local/Programs/Python/Python37/Lib/site-packages' )


try:
    from PIL import Image
    # print("import succeeded")
except:
    print("import failed")


def calculate_opacity(r1, r2, p):
    """
    Calculate the opacity of two pixels based on the formula f((1-p)R + p(R))R1.
    """
    opacity = tuple(int((1 - p) * c1 + p * c2) for c1, c2 in zip(r1, r2))
    return opacity


def import_texture(file_path, texture_name=None):
    """
    Imports a texture into the Maya project.

    :param file_path: The file path of the texture.
    :param texture_name: The name to assign to the texture node. If None, the file name will be used.
    """
    if not file_path:
        raise ValueError("File path cannot be empty")
    
    # Extract the file name without extension if texture_name is not provided
    if not texture_name:
        texture_name = file_path.split('/')[-1].split('.')[0]

    # Create a file texture node
    texture_node = cmds.shadingNode('file', asTexture=True, name=texture_name)

    # Set the file path to the texture node
    cmds.setAttr(f"{texture_node}.fileTextureName", file_path, type="string")

    # Create a shading group and assign the texture to it
    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{texture_name}_SG")
    shader = cmds.shadingNode('lambert', asShader=True, name=f"{texture_name}_shader")
    cmds.connectAttr(f"{shader}.outColor", f"{shading_group}.surfaceShader", force=True)
    cmds.connectAttr(f"{texture_node}.outColor", f"{shader}.color", force=True)

    print(f"Texture '{file_path}' imported and assigned to shader '{shader}'")


def blend_seam(img1, img2, xy):
    width, height = img1.size #get dimensions
    new_width = int(width * 1.5)
    new_height = int(height * 1.5)

    count = 0
    
    if xy == True:
        new_img = Image.new(img1.mode, (new_width, height)) #make new image 1.5 X size
        stretch_area = (width//2) * height

        for x in range(new_width):
            p= count/stretch_area #set opacity

            for y in range(height):
                if (x > new_width - width and x < width) : #check if value is within the range
                    count += 1

                    pixel1 = img1.getpixel((x , y))
                    pixel2 = img2.getpixel((x - (width/2), y))

                    featherpixel = calculate_opacity(pixel1, pixel2, p)

                    new_img.putpixel( (x, y), featherpixel)

                elif x <= width/2 :
                    new_img.putpixel((x,y), img1.getpixel((x , y)))
                else:
                    new_img.putpixel((x,y), img2.getpixel((x - (width/2) , y)))


    if xy == False:

        new_img = Image.new(img1.mode, (width, new_height)) #make new image 1.5 X size
        stretch_area = height//2


        for x in range(width):
            count = 0
        
            for y in range(new_height):

                if y > height//2 and y < new_height - (height // 2): #1-0 or 0-1
                    p= count/ stretch_area #set opacity
                    
                    pixel1 = img1.getpixel((x , y))
                    pixel2 = img2.getpixel((x, y - (height/2)))
                    featherpixel = calculate_opacity(pixel1, pixel2, p)

                    new_img.putpixel( (x, y), featherpixel)

                    count += 1

                elif y <= height//2:
                    new_img.putpixel( (x,y), img1.getpixel( (x,y) ) )
                elif y >= height :
                    new_img.putpixel( (x,y) ,img2.getpixel((x, y - (height/2))))
            

    return new_img
    

def make_tileable(image_path): 
    folder = image_path.rsplit("/", 1)[0]
 
    # os.makedirs(os.path.dirname(image_path), exist_ok=True)
    os.makedirs(os.path.dirname(folder), exist_ok=True)

    #TODO: check to make sure its an image 
    image = Image.open(image_path)

    # Create a new image with double the width and height of the original. Make sure the image is a square.
    width, height = image.size
    if(width < height):
        new_image = Image.new('RGB', (width , width ))
        height = width
    elif(width > height):
        new_image = Image.new('RGB', (height , height ))
        width = height
    elif(width == height):
        new_image = Image.new('RGB', (width , height ))
    
    # Place the original image at the four corners of the new image
    scale = int(width * 1.25)
    half_scale = scale//2

    image = image.resize((scale, scale))

    # get corners   ((left, top, right, bottom))
    left_top = image.crop((half_scale, half_scale, scale, scale))
    right_top = image.crop((0, half_scale, half_scale, scale))
    left_bottom = image.crop((half_scale, 0, scale, half_scale))
    right_bottom = image.crop((0, 0, half_scale, half_scale))

    # --- blend seams ---
    top_half = blend_seam(left_top, right_top, True)
    bottom_half = blend_seam(left_bottom, right_bottom, True)
    new_image = blend_seam(top_half, bottom_half, False)


    # new_image.show()


    out_name = "/tiled_" + image_path.rsplit("/", 1)[1] 
    # print(out_name)
    new_image.save(folder + out_name)

    return folder + out_name #for getting the import  


def maya_useNewAPI():
    pass


class TileMe(om.MPxCommand):
    COMMAND_NAME = "tileme"

    def __init__(self):
        super(TileMe, self).__init__()


    def doIt(self, args):

        # get file location of selected image > get all selected
        selected = cmds.ls(sl=True,long=True) or []
        # print("selected objects: " + str(selected))
            
        for i in selected:
            attribute = i

            # print( "attribute" + str(attribute))
            attribute = attribute + ".fileTextureName"
            location = cmds.getAttr(attribute)

            # print("attribute list: " + str(cmds.listAttr( r=True, s=True )))
            # TODO fix for all file types

            # print( "selected attribute location: " + location)

            folder = location.rsplit("/", 1)
            folder = folder[0] 
            os.makedirs(os.path.dirname(folder), exist_ok=True)

            tiled_texture = make_tileable( location )
            import_texture( tiled_texture )



    @classmethod 
    def creator(cls):
        return TileMe()


def initializePlugin(plugin):
    # print("---TileMe plugin initialized---")
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
    sys.path.remove( 'C:/Users/sophi/AppData/Local/Programs/Python/Python37/Lib/site-packages' )
    # print(sys.path)
    try:
        plugin_fn.deregisterCommand(TileMe.COMMAND_NAME)
    except:
        om.MGLobal.displayError("failed to deregister".format(TileMe))

if __name__ == "__main__":
    plugin_name = "Tile_Me.py"

    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.aloadPlugin("{0}")'.format(plugin_name))


