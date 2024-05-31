import maya.api.OpenMaya as om
import maya.cmds as cmds
import os 

# import sys sys.path.append( 'c:\\users\\sophi\\appdata\\local\\programs\\python\\python310\\lib\\site-packages' )
import sys sys.path.append( 'c:\\users\\sophi\\appdata\\local\\programs\\python\\python310\\lib\\site-packages' )
# from PIL import Image, ImageFilter



def maya_useNewAPI():
	pass

# def make_tileable(image_path, output):
# 	print("hello")

class TileMe(om.MPxCommand):
	COMMAND_NAME = "tileme"

	def __init__(self):
		super(TileMe, self).__init__()

    # @staticmethod
	# def make_tileable(image_path, output):	    
	# #     # image = Image.open(image_path)
	  	# print("hello")
	#     # Create a new image with double the width and height of the original. Make sure the image is a square.
	#     width, height = image.size
	#     if(width < height):
	#         new_image = Image.new('RGB', (width * 2, width * 2))
	#         image = image.crop((0 , (height-width)//2 ,width , height - (height-width)//2 ))
	#         # image.show()
	#         height = width
	#     elif(width > height):
	#         new_image = Image.new('RGB', (height * 2, height * 2))
	#         # im1 = im.crop((left, top, right, bottom))
	#         image = image.crop((  (width - height)//2 , 0 , width - ((width - height)//2), height  ))
	#         # image.show()
	#         width = height
	#     elif(width == height):
	#         new_image = Image.new('RGB', (width * 2, height * 2))
	    
	#     # Place the original image at the four corners of the new image
	    
	#     new_image.paste(image, (0, 0))
	#     new_image.paste(image, (width - 100, 0))
	#     new_image.paste(image, (0, height))
	#     new_image.paste(image, (width, height))
	    
	#     # Crop the new image back to the original size
	#     new_image = new_image.crop((width//2, height//2, width//2 + width, height//2 + height))
	    
	#     # Save the tileable image
	#     new_image.save(output)	



	def doIt(self, args):
		print("tileme recognized")

		# get file location of selected image
		selected = cmds.ls(sl=True,long=True) or []
		print(selected[0])
		attribute = selected[0] + ".filename"
		location = os.path.abspath(selected[0])
		print( "selected attribute location: " + str(location))


		# TileMe.make_tileable( location, 'out.jpg' )




	@classmethod 
	def creator(cls):
		return TileMe()

def initializePlugin(plugin):
	print("TileMe plugin initialized...")
	vendor = "SB"
	version = "1.0"
	# tile2 = TileMe.creator()
	# tile2.creator()


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