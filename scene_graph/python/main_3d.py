import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from PIL import Image, ImageOps

import glm
from camera3d import *
from light import *
from shader import *
from material import *
from transform import *
from node import *
from scene import *
from cube import * 
from sphere import * 
from texture import * 
from polyoffset import * 
from quad import *

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT,GL_TRUE)
    win = glfw.create_window(640, 480, "Hello World", None, None)
    if not win:
        glfw.terminate()
        return
    glfw.set_key_callback(win,keyboard)

    # Make the window's context current
    glfw.make_context_current(win)
    print("OpenGL version: ",glGetString(GL_VERSION))

    initialize(win)

    # Loop until the user closes the window
    while not glfw.window_should_close(win):
        # Render here, e.g. using pyOpenGL
        display(win)

        # Swap front and back buffers
        glfw.swap_buffers(win)

        # Poll for and process events
        glfw.poll_events()

viewer_pos = glm.vec3(2.0, 3.5, 4.0)

def initialize (win):
  # set background color: white 
  glClearColor(1.0,1.0,1.0,1.0)
  # enable depth test 
  glEnable(GL_DEPTH_TEST)
  # cull back faces
  glEnable(GL_CULL_FACE)  

  # create objects
  global camera
  camera = Camera3D(viewer_pos[0],viewer_pos[1],viewer_pos[2])
  #camera.SetOrtho(true)
  arcball = camera.CreateArcball()
  arcball.Attach(win)

  # light = Light(viewer_pos[0],viewer_pos[1],viewer_pos[2])
  light = Light(0.0,0.0,0.0,1.0,"camera")

  white = Material(1.0,1.0,1.0)
  red = Material(1.0,0.5,0.5)
  poff = PolygonOffset(-1,-1)
  paper = Texture("decal","../../images/paper.jpg")

  trf1 = Transform()
  trf1.Scale(3.0,0.3,3.0)
  trf1.Translate(0.0,-1.0,0.0)
  trf2 = Transform()
  trf2.Scale(0.5,0.5,0.5)
  trf2.Translate(0.0,1.0,0.0)
  trf3 = Transform()
  trf3.Translate(0.8,0.0,0.8)
  trf3.Rotate(30.0,0.0,1.0,0.0)
  trf3.Rotate(90.0,-1.0,0.0,0.0)
  trf3.Scale(0.5,0.7,1.0);

  cube = Cube() 
  quad = Quad() 
  sphere = Sphere()

  shader = Shader(light,"world")
  shader.AttachVertexShader("../../shaders/ilum_frag/vertex.glsl")
  shader.AttachFragmentShader("../../shaders/ilum_frag/fragment.glsl")
  shader.Link()

  shd_tex = Shader(light,"world")
  shd_tex.AttachVertexShader("../../shaders/texture/vertex.glsl")
  shd_tex.AttachFragmentShader("../../shaders/texture/fragment.glsl")
  shd_tex.Link()
  # build scene
  root = Node(shader,
              nodes = [
                        Node(None,trf1,[red],[cube]),
                        Node(shd_tex,trf3,[white,poff,paper],{quad}),
                        Node(None,trf2,[white],[sphere])
                      ]
              )
  global scene 
  scene = Scene(root)

def display (win):
  global scene
  global camera
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
  scene.Render(camera)

def keyboard (win, key, scancode, action, mods):
   if key == glfw.KEY_Q and action == glfw.PRESS:
      glfw.set_window_should_close(win,glfw.TRUE)

if __name__ == "__main__":
    main()
