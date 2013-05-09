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

class GLPlotWidget(QGLWidget):
    # default window size
    width, height = 96, 64
    bunny_point = [30, 50]
 
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

    def draw_bunny(self, x_val, width, y_val, height):
        top_x = x_val + width
        top_y = y_val + height

        bot = int((width / 10) * 2)
        top = int((width / 10) * 5)
        eye_width = int((width / 100) * 45)
        bot_y = int((height / 100) * 50)

        r, g, b = COLOURS['other-grey']
        gl.glColor3f(r, g, b)

        for x in xrange(x_val + bot, top_x - top):
            for y in xrange(y_val + bot_y, top_y):
                self.draw_square(x, y)
                self.draw_square(x + eye_width, y)


        bot = int((width / 100) * 30)
        top = int((width / 100) * 65)
        bot_y = int((height / 100) * 60)
        topl_y = int((height / 100) * 20)

        r, g, b = COLOURS['white']
        gl.glColor3f(r, g, b)

        for x in xrange(x_val + bot, top_x - top):
            for y in xrange(y_val + bot_y, top_y - topl_y):
                self.draw_square(x, y)
                self.draw_square(x + eye_width, y)

        r, g, b = COLOURS['grey']
        gl.glColor3f(r, g, b)

        top = int((width / 5) * 1)
        
        # draw the jaw
        for x in xrange(x_val + 1, top_x - top):
            for y in xrange(y_val + 2, y_val + 4):
                self.draw_square(x, y)

        # draw the spikes
        for x in xrange(x_val, top_x + 3, int(width / 5)):
            for y in xrange(y_val, y_val + 2):
                self.draw_square(x, y)
        
        #draw the other half of the face
        for x in xrange(x_val + top, top_x):
            for y in xrange(y_val + 2, y_val + 4):
                r, g, b = choice([COLOURS['grey'], COLOURS['other-grey']])
                gl.glColor3f(r, g, b)
                self.draw_square(x, y)



    def paintGL(self):
        """Paint the scene.
        """
        # clear the buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # set yellow color for subsequent drawing rendering calls
        
        # tell OpenGL that the VBO contains an array of vertices
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        
        for x in xrange(96):
            r, g, b = COLOURS['black'] 
            gl.glColor3f(r, g, b)
            for y in xrange(64):
                self.draw_square(x, y)
        
        r, g, b = COLOURS['grey']
        gl.glColor3f(r, g, b)
        bunny_point = self.bunny_point

        if bunny_point[0] <= 0:
            bunny_point[0] += choice([0, 1])
        elif bunny_point[0] + 18 >= self.width:
            bunny_point[0] -= choice([0, 1])
        else:
            bunny_point[0] += choice(range(-5, 6))

        if bunny_point[1] <= 0:
            bunny_point[1] += choice([0, 1, 2])
        elif bunny_point[1] + 12 >= self.height:
            bunny_point[1] -= choice([0, 1, 2])
        else:
            bunny_point[1] += choice(range(-5, 6))

        self.draw_bunny(bunny_point[0], 20, bunny_point[1], 15)

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

            self.setGeometry(0, 0, self.widget.width * 5, self.widget.height * 5)
            self.setCentralWidget(self.widget)
            self.show()

            self.paint_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.paint_timer, QtCore.SIGNAL("timeout()"), self.widget.updateGL)


            QtCore.QMetaObject.connectSlotsByName(self)
            self.paint_timer.start(2)

 
    # create the QT App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()