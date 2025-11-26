from OpenGL.GL import *
import glfw

from computeshader import *
from texbuffer import *

def initialize ():
  buf = TexBuffer("data", np.array([1, 2, 3, 4], dtype='float32'))
  cs = ComputeShader("../shaders/cs/compute_shader.glsl")
  cs.AttachTexBuffer(buf)
  cs.Dispatch(1)
  print(buf.GetData())

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,5)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT,GL_TRUE)
    win = glfw.create_window(600, 600, "2D scene", None, None)
    if not win:
        glfw.terminate()
        return
    # Make the window's context current
    glfw.make_context_current(win)
    print("OpenGL version: ",glGetString(GL_VERSION))

    initialize()

if __name__ == "__main__":
    main()