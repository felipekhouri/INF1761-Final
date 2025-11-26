"""
Classe Cone para geração de geometria de cone
Compatível com o framework de grafo de cena
"""

from OpenGL.GL import *
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../scene_graph/python"))

from shape import Shape
import numpy as np
import math


class Cone(Shape):
    """
    Gera um cone orientado ao longo do eixo Y.
    Base em Y=0, vértice em Y=1.
    Raio da base = 1 (antes de transformações).
    """

    def __init__(self, nslices=32, with_base=True, disable_culling=False):
        """
        nslices: número de subdivisões ao redor do cone
        with_base: se True, gera base circular
        disable_culling: se True, desabilita face culling ao renderizar
        """
        self.nslices = nslices
        self.with_base = with_base
        self.disable_culling = disable_culling

        # Calcula número total de vértices e índices
        # Corpo do cone (vértice superior + círculo da base)
        body_vertices = 1 + (nslices + 1)  # vértice + borda
        body_indices = nslices * 3  # triângulos do corpo

        # Base (se habilitada)
        base_vertices = 0
        base_indices = 0
        if with_base:
            base_vertices = 1 + (nslices + 1)  # centro + borda
            base_indices = nslices * 3

        total_vertices = body_vertices + base_vertices
        total_indices = body_indices + base_indices

        # Arrays
        coords = np.empty(3 * total_vertices, dtype="float32")
        normals = np.empty(3 * total_vertices, dtype="float32")
        texcoords = np.empty(2 * total_vertices, dtype="float32")
        indices = np.empty(total_indices, dtype="uint32")

        vid = 0
        cid = 0
        nid = 0
        tid = 0
        iid = 0

        # ===== CORPO DO CONE =====

        # Vértice superior (topo)
        coords[cid : cid + 3] = [0, 1, 0]
        cid += 3
        # Normal no topo aponta para cima
        normals[nid : nid + 3] = [0, 1, 0]
        nid += 3
        texcoords[tid : tid + 2] = [0.5, 1.0]
        tid += 2
        vertex_top = vid
        vid += 1

        # Vértices da base (círculo em Y=0)
        base_start = vid
        for slice in range(nslices + 1):
            theta = (slice / nslices) * 2 * math.pi
            x = math.cos(theta)
            z = math.sin(theta)
            u = slice / nslices

            coords[cid : cid + 3] = [x, 0, z]
            cid += 3

            # Normal lateral do cone (perpendicular à superfície)
            # Para um cone, a normal lateral tem componente Y
            # tan(angle) = height/radius = 1/1 = 1, então angle = 45°
            # Normal = normalize([x, 1, z])
            nx = x
            ny = 1.0
            nz = z
            length = math.sqrt(nx * nx + ny * ny + nz * nz)
            normals[nid : nid + 3] = [nx / length, ny / length, nz / length]
            nid += 3

            texcoords[tid : tid + 2] = [u, 0.0]
            tid += 2
            vid += 1

        # Índices do corpo (triângulos conectando topo à base)
        for slice in range(nslices):
            v0 = vertex_top
            v1 = base_start + slice
            v2 = base_start + slice + 1
            indices[iid : iid + 3] = [v0, v1, v2]
            iid += 3

        # ===== BASE (SE HABILITADA) =====
        if with_base:
            base_vid_start = vid

            # Vértice central da base
            coords[cid : cid + 3] = [0, 0, 0]
            cid += 3
            normals[nid : nid + 3] = [0, -1, 0]
            nid += 3
            texcoords[tid : tid + 2] = [0.5, 0.5]
            tid += 2
            center_base = vid
            vid += 1

            # Vértices da borda da base
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

            # Índices da base
            for slice in range(nslices):
                v0 = center_base
                v1 = base_vid_start + 1 + slice
                v2 = base_vid_start + 1 + slice + 1
                indices[iid : iid + 3] = [v0, v1, v2]
                iid += 3

        self.nind = len(indices)

        # ===== CRIAR VAO E VBOs =====
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        buffers = glGenBuffers(4)

        # Buffer de coordenadas (location 0)
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
        """Renderiza o cone"""
        # Desabilita culling se necessário
        culling_was_enabled = glIsEnabled(GL_CULL_FACE)
        if self.disable_culling and culling_was_enabled:
            glDisable(GL_CULL_FACE)

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.nind, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        # Restaura culling se foi desabilitado
        if self.disable_culling and culling_was_enabled:
            glEnable(GL_CULL_FACE)
