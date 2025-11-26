from OpenGL.GL import *
import shaderutl as sutl

class ComputeShader:
  def __init__ (self, filename):
    self.texunit = 0
    self.pid = None
    self.texbuffers = []
    self.shader = sutl.create_shader(GL_COMPUTE_SHADER,filename)

  def AttachTexBuffer (self, texbuffer):
    self.texbuffers.append(texbuffer)

  def Dispatch (self, nx, ny=1, nz=1):
    if not self.pid:
      self.pid = sutl.create_program(self.shader)

    glUseProgram(self.pid)
    for i,tb in enumerate(self.texbuffers):
      tex = tb.GetTexId()
      loc = glGetUniformLocation(self.pid,tb.varname)
      assert loc >= 0, "Invalid uniform name: " + tb.varnames
      glUniform1i(loc,i)
      #glActiveTexture(GL_TEXTURE0 + i)
      glBindImageTexture(i,tex,0,GL_FALSE,0,GL_READ_WRITE,tb.format)
      #glBindTexture(GL_TEXTURE_BUFFER,tex)
    glDispatchCompute(nx, ny, nz)
    glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT |
                    GL_TEXTURE_FETCH_BARRIER_BIT |
                    GL_BUFFER_UPDATE_BARRIER_BIT)