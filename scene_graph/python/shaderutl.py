# auxiliary functions for shader management
from OpenGL.GL import *

def create_shader (type, filename):
  id = glCreateShader(type)
  if not id:
    raise RuntimeError("could not create shader")
  text = readfile(filename)
  glShaderSource(id,text)
  compile_shader(id,filename)
  return id

def compile_shader (id, filename):
  glCompileShader(id)
  if not glGetShaderiv(id,GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(id).decode()
    raise RuntimeError("Compilation error: " + filename + "\n" + error)

def create_program (*argv):
  id = glCreateProgram()
  if not id:
    raise RuntimeError("could not create shader")
  for arg in argv:
     glAttachShader(id,arg) 
  link_program(id)
  return id

def link_program (id):
  glLinkProgram(id)
  if not glGetProgramiv(id, GL_LINK_STATUS):
      error = glGetProgramInfoLog(id).decode()
      raise RuntimeError('Linking error: ' + error)

# read file to a string
def readfile (filename):
  with open(filename) as f:
    lines = f.readlines()
  text = ""
  for l in lines:
    text = text + l
  return text
