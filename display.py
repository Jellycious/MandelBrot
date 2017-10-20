from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Display:

    def __init__(self, window_width, window_height, window_title, display_func, keyboard_func=None,
                 eye_location=(0, 0, 20), reference_location=(0, 0, 0), keyboard_up_func=None):
        self.window_width = window_width
        self.window_height = window_height
        self.window_title = window_title
        self.display_func = display_func
        self.started = False
        self.keyboard_func = keyboard_func
        self.keyboard_up_func = keyboard_up_func
        self.eye_location = eye_location
        self.reference_location = reference_location

        try:
            glutInit(sys.argv)
            glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
            glutInitWindowSize(self.window_width, self.window_height)
            glutCreateWindow(self.window_title)
            glutDisplayFunc(self.display_func)

            if keyboard_func:
                glutKeyboardFunc(self.keyboard_func)
            if keyboard_up_func:
                glutKeyboardUpFunc(self.keyboard_up_func)

        except Exception as e:
            print(e)

    def update(self):
        glutSwapBuffers()
        glutPostRedisplay()

    def clear(self, r, g, b, a):
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def quit(self):
        glutDestroyWindow(glutGetWindow)

    def start(self):
        # Standard perspective
        glMatrixMode(GL_PROJECTION)
        gluPerspective(90., self.window_width / self.window_height, 2, 100)
        eye = self.eye_location
        ref = self.reference_location
        gluLookAt(eye[0], eye[1], eye[2],
                  ref[0], ref[1], ref[2],
                  0, 1, 0)
        glutMainLoop()

    def look_at(self, eye_location, reference_location):
        if len(eye_location) != 3:
            raise Exception("eye location should be of length 3")
        if len(reference_location) != 3:
            raise Exception("look location should be of length 3")
        self.reference_location = reference_location
        self.eye_location = reference_location
        gluLookAt(eye_location, reference_location, (0, 1, 0))

    def get_eye_location(self):
        return self.eye_location

    def get_reference_location(self):
        return self.reference_location

    def get_width(self):
        return self.window_width

    def get_height(self):
        return self.window_height

    def get_title(self):
        return self.window_title

    def set_display_func(self, display_func):
        self.display_func = display_func

    def set_keyboard_func(self, keyboard_func):
        self.keyboard_func = keyboard_func
