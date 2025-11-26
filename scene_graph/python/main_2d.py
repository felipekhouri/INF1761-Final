from OpenGL.GL import *
import glfw
import random as rd

from camera2d import *
from color import *
from transform import *
from quad import *
from triangle import *
from node import *
from shader import *
from scene import *
from engine import *

class MovePointer(Engine):
  def __init__ (self, trf):
    self.trf = trf
  def Update (self, dt):
    self.trf.Rotate(6*dt,0,0,-1)

def initialize ():
  # set background color: white 
  glClearColor(0.8,1.0,1.0,1.0)
  # enable depth test 
  glEnable(GL_DEPTH_TEST)

  # create objects
  global camera
  camera = Camera2D(0,10,0,10)

  trf1 = Transform()
  trf1.Translate(3,3,-0.5)
  trf1.Scale(4,4,1)
  face = Node(trf=trf1,apps=[Color(1,1,1)],shps=[Quad()])
  trf2 = Transform()
  trf2.Translate(5,5,0)
  trf3 = Transform()
  trf3.Scale(0.1,2,1)
  pointer = Node(trf=trf2,nodes=[Node(trf=trf3,apps=[Color(1,0,0)],shps=[Triangle()])])

  shader = Shader()
  shader.AttachVertexShader("../shaders/2d/vertex.glsl")
  shader.AttachFragmentShader("../shaders/2d/fragment.glsl")
  shader.Link()

  # build scene
  root = Node(shader, nodes = [face,pointer])
  global scene 
  scene = Scene(root)
  scene.AddEngine(MovePointer(trf2))

def update (dt):
  scene.Update(dt)

def display ():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
  scene.Render(camera)

def keyboard (win, key, scancode, action, mods):
   if key == glfw.KEY_Q and action == glfw.PRESS:
      glfw.set_window_should_close(win,glfw.TRUE)

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT,GL_TRUE)
    win = glfw.create_window(600, 600, "2D scene", None, None)
    if not win:
        glfw.terminate()
        return
    glfw.set_key_callback(win,keyboard)

    # Make the window's context current
    glfw.make_context_current(win)
    print("OpenGL version: ",glGetString(GL_VERSION))

    initialize()

    # Loop until the user closes the window
    t0 = glfw.get_time()
    while not glfw.window_should_close(win):
        t = glfw.get_time()
        update(t-t0)
        t0 = t
        display()

        # Swap front and back buffers
        glfw.swap_buffers(win)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()