"""
Classe Cylinder para geração de geometria de cilindro
Compatível com o framework de grafo de cena
"""

from OpenGL.GL import *
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../scene_graph/python"))

from shape import Shape
from grid import Grid
import numpy as np
import math


class Cylinder(Shape):
    """
    Gera um cilindro orientado ao longo do eixo Y.
    Base inferior em Y=0, base superior em Y=1.
    Raio = 1 (antes de transformações).
    """

    def __init__(self, nslices=32, nstacks=1, with_caps=True, disable_culling=False):
        """
        nslices: número de subdivisões ao redor do cilindro
        nstacks: número de subdivisões verticais
        with_caps: se True, gera tampas superior e inferior
        disable_culling: se True, desabilita face culling ao renderizar (para objetos ocos)
        """
        self.nslices = nslices
        self.nstacks = nstacks
        self.with_caps = with_caps
        self.disable_culling = disable_culling

        # Calcula número total de vértices e índices
        # Corpo do cilindro
        body_vertices = (nstacks + 1) * (nslices + 1)
        body_indices = nstacks * nslices * 6  # 2 triângulos por quad

        # Tampas (se habilitadas)
        cap_vertices = 0
        cap_indices = 0
        if with_caps:
            # Cada tampa: 1 vértice central + (nslices + 1) vértices na borda
            cap_vertices = 2 * (1 + nslices + 1)  # 2 tampas * (centro + borda)
            # Cada tampa: nslices triângulos
            cap_indices = 2 * nslices * 3

        total_vertices = body_vertices + cap_vertices
        total_indices = (
            body_indices + cap_indices
        )  # Arrays para coordenadas, normais e texcoords
        coords = np.empty(3 * total_vertices, dtype="float32")
        normals = np.empty(3 * total_vertices, dtype="float32")
        texcoords = np.empty(2 * total_vertices, dtype="float32")
        indices = np.empty(total_indices, dtype="uint32")

        vid = 0  # vertex id
        cid = 0  # coord id
        nid = 0  # normal id
        tid = 0  # texcoord id
        iid = 0  # index id

        # ===== CORPO DO CILINDRO =====
        for stack in range(nstacks + 1):
            y = stack / nstacks  # Y varia de 0 a 1
            v = stack / nstacks  # coordenada de textura V

            for slice in range(nslices + 1):
                theta = (slice / nslices) * 2 * math.pi
                u = slice / nslices  # coordenada de textura U

                # Posição
                x = math.cos(theta)
                z = math.sin(theta)
                coords[cid : cid + 3] = [x, y, z]
                cid += 3

                # Normal (perpendicular ao eixo Y)
                normals[nid : nid + 3] = [x, 0, z]
                nid += 3

                # Texcoord
                texcoords[tid : tid + 2] = [u, v]
                tid += 2

                vid += 1

        # Índices do corpo
        for stack in range(nstacks):
            for slice in range(nslices):
                # Quad formado por 4 vértices
                v0 = stack * (nslices + 1) + slice
                v1 = v0 + 1
                v2 = v0 + (nslices + 1)
                v3 = v2 + 1

                # Primeiro triângulo
                indices[iid : iid + 3] = [v0, v2, v1]
                iid += 3

                # Segundo triângulo
                indices[iid : iid + 3] = [v1, v2, v3]
                iid += 3

        # ===== TAMPAS (SE HABILITADAS) =====
        if with_caps:
            base_vid = vid

            # Tampa inferior (Y=0, normal apontando para baixo)
            # Vértice central
            coords[cid : cid + 3] = [0, 0, 0]
            cid += 3
            normals[nid : nid + 3] = [0, -1, 0]
            nid += 3
            texcoords[tid : tid + 2] = [0.5, 0.5]
            tid += 2
            center_bottom = vid
            vid += 1

            # Vértices da borda
            for slice in range(nslices + 1):
                theta = (slice / nslices) * 2 * math.pi
                x = math.cos(theta)
                z = math.sin(theta)

                coords[cid : cid + 3] = [x, 0, z]
                cid += 3
                normals[nid : nid + 3] = [0, -1, 0]
                nid += 3
                # Texcoord circular
                u = 0.5 + 0.5 * x
                v = 0.5 + 0.5 * z
                texcoords[tid : tid + 2] = [u, v]
                tid += 2
                vid += 1

            # Índices da tampa inferior
            for slice in range(nslices):
                v0 = center_bottom
                v1 = base_vid + 1 + slice
                v2 = base_vid + 1 + slice + 1
                indices[iid : iid + 3] = [v0, v1, v2]
                iid += 3

            # Tampa superior (Y=1, normal apontando para cima)
            base_vid = vid

            # Vértice central
            coords[cid : cid + 3] = [0, 1, 0]
            cid += 3
            normals[nid : nid + 3] = [0, 1, 0]
            nid += 3
            texcoords[tid : tid + 2] = [0.5, 0.5]
            tid += 2
            center_top = vid
            vid += 1

            # Vértices da borda
            for slice in range(nslices + 1):
                theta = (slice / nslices) * 2 * math.pi
                x = math.cos(theta)
                z = math.sin(theta)

                coords[cid : cid + 3] = [x, 1, z]
                cid += 3
                normals[nid : nid + 3] = [0, 1, 0]
                nid += 3
                # Texcoord circular
                u = 0.5 + 0.5 * x
                v = 0.5 + 0.5 * z
                texcoords[tid : tid + 2] = [u, v]
                tid += 2
                vid += 1

            # Índices da tampa superior
            for slice in range(nslices):
                v0 = center_top
                v1 = base_vid + 1 + slice
                v2 = base_vid + 1 + slice + 1
                indices[iid : iid + 3] = [
                    v0,
                    v2,
                    v1,
                ]  # Ordem inversa para normal externa
                iid += 3

        self.nind = len(indices)

        # ===== CRIAR VAO E VBOs =====
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Buffers
        buffers = glGenBuffers(4)

        # Buffer de coordenadas (location 0 e 1 - posição e normal)
        glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
        glBufferData(GL_ARRAY_BUFFER, coords.nbytes, coords, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        # Buffer de normais (location 1)
        glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
        glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)

        # Buffer de texcoords (location 3)
        glBindBuffer(GL_ARRAY_BUFFER, buffers[2])
        glBufferData(GL_ARRAY_BUFFER, texcoords.nbytes, texcoords, GL_STATIC_DRAW)
        glVertexAttribPointer(3, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(3)

        # Buffer de índices
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[3])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glBindVertexArray(0)

    def Draw(self, st):
        """Renderiza o cilindro"""
        # Desabilita culling se necessário (para objetos ocos como copos)
        culling_was_enabled = glIsEnabled(GL_CULL_FACE)
        if self.disable_culling and culling_was_enabled:
            glDisable(GL_CULL_FACE)

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.nind, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        # Restaura culling se foi desabilitado
        if self.disable_culling and culling_was_enabled:
            glEnable(GL_CULL_FACE)
