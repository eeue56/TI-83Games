from __future__ import division

# PyQT4 imports
from PyQt4 import QtGui, QtCore, QtOpenGL
from PyQt4.QtOpenGL import QGLWidget
# PyOpenGL imports
import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo
from random import choice

COLOURS = { 'black' : [0, 0, 0],
            'other-grey' : [0.25, 0.25, 0.25],
            'grey' : [0.4, 0.4, 0.4],
            'white' : [1, 1, 1]}

class Player(object):
    def __init__(self, x, y, health=3):
        self.x = xrange
        self.y = y
        self.health = health
        self.is_exploded = False


class GLPlotWidget(QGLWidget):
    # default window size
    width, height = 96, 64
    bunny_point = [30, 50]
    player = Player(20, 20)
 
    def initializeGL(self):
        """Initialize OpenGL, VBOs, upload data on the GPU, etc.
        """
        # background color
        gl.glClearColor(0,0,0,0)
        gl.glViewport(0, 0, self.width, self.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
 
    def draw_square(self, x, y):
        gl.glRectf(x, y, x + 1, y + 1)

    def draw_player(self):

        r, g, b = COLOURS['grey']
        gl.glColor3f(r, g, b)
        for x in xrange(self.player.x, self.player.x + 4):
            for y in xrange(self.player.y, self.player.y + 3):
                self.draw_square(x, y)

            self.draw_square(x, y + 4)

    def paintGL(self):
        """Paint the scene.
        """
        # clear the buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # set yellow color for subsequent drawing rendering calls
        
        # tell OpenGL that the VBO contains an array of vertices
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        
        r, g, b = COLOURS['grey']
        gl.glColor3f(r, g, b)
        self.draw_player()

    def resizeGL(self, width, height):
        """Called upon window resizing: reinitialize the viewport.
        """
        # update the window size    
        print width
        print height
        self.width, self.height = width, height
        # paint within the whole window
        gl.glViewport(0, 0, self.width, self.height)
        # set orthographic projection (2D only)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        # the window corner OpenGL coordinates are (-+1, -+1)
        gl.glOrtho(0, 96, 0, 64, -1, 1)
 
if __name__ == '__main__':
    # import numpy for generating random data points
    import sys
 
    # define a QT window with an OpenGL widget inside it
    class TestWindow(QtGui.QMainWindow):
        def __init__(self):
            super(TestWindow, self).__init__()
            # initialize the GL widget
            self.widget = GLPlotWidget()

            self.widget.setGeometry(0, 0, self.widget.width, self.widget.height)
            self.setCentralWidget(self.widget)
            self.show()

            self.paint_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.paint_timer, QtCore.SIGNAL("timeout()"), self.widget.updateGL)

            QtCore.QMetaObject.connectSlotsByName(self)
            self.paint_timer.start(16)

        def keyPressEvent(self, event):
            key = event.key()
            if key == QtCore.Qt.Key_A:
                self.widget.player.x -= 1
            if key == QtCore.Qt.Key_D:
                self.widget.player.x += 1
            if key == QtCore.Qt.Key_W:
                self.widget.player.y += 1
            if key == QtCore.Qt.Key_S:
                self.widget.player.y -= 1
            if key == QtCore.Qt.Key_Space:
                self.widget.player.is_exploded = not self.widget.player.is_exploded
            self.widget.updateGL()

 
    # create the QT App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()