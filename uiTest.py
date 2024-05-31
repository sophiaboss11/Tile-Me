super().__init__(parent_window)
import maya.cmds as cmds


window_name = 'Fancy UI'

# delete this UI if it already exists
if cmds.window(window_name, exists=True):
    cmds.deleteUI(window_name, window=True)

# set title, object name, window type, and show
self.setObjectName(window_name)
self.setWindowTitle(window_name)
self.setWindowFlags(Qt.Tool)
self.show()

# set main widget and main vertical layout
widget = QtWidgets.QWidget()
self.setCentralWidget(widget)
main_layout = QtWidgets.QVBoxLayout(widget)

# add label
label = QtWidgets.QLabel('Welcome to the fancy UI')
main_layout.addWidget(label)

# add button
button = QtWidgets.QPushButton('Say Hello')
button.clicked.connect(self.say_hello)
main_layout.addWidget(button)

# this method is called by the Say Hello button
def say_hello(self):
    print('hello there')

FancyUI()
