"""
Projeto 02 - INF1761 Computação Gráfica
Cena 3D com mesa, objetos, iluminação Phong, texturas, fog e bump mapping

Pontuação:
- Base (7.0 pts): mesa + objetos + iluminação
- Fog (1.0 pt): efeito de neblina por distância
- Bump mapping (2.0 pts): rugosidade na esfera verde
TOTAL: 10.0 pontos

Aluno: Felipe
Professor: Waldemar Celes (PUC-Rio)
"""

import glfw
from OpenGL.GL import *
import sys
import os

# Adiciona o diretório atual PRIMEIRO para usar nossos arquivos corrigidos
sys.path.insert(0, os.path.dirname(__file__))
# Adiciona o caminho do scene_graph como fallback
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "../scene_graph/python"))

import glm
from camera3d import Camera3D
from light import Light
from shader import Shader
from material import Material
from transform import Transform
from node import Node
from scene import Scene
from cube import Cube
from sphere import Sphere
from texture import Texture
from state import State
import shadows

# Importa geometrias customizadas
from cylinder import Cylinder
from cone import Cone


# Monkey patch Shader class to fix typo in framework (textunit vs texunit)
def fixed_init(self, light=None, space="camera"):
    self.shaders = []
    self.texunit = 0  # Fixed name (was textunit)
    self.light = light
    self.space = space
    self.pid = None


Shader.__init__ = fixed_init

# posição inicial do observador
viewer_pos = glm.vec3(4.0, 3.5, 5.0)

# globais
scene = None
camera = None
node_reflection = None
node_shadow_table = None
node_table_top = None
node_table_legs = None
node_objects_on_table = None
shader = None


def initialize(win):
    """Inicializa a cena 3D com mesa, objetos, fog e bump mapping"""
    global scene, camera, shader
    global node_table_top, node_table_legs, node_objects_on_table
    global node_reflection, node_shadow_table

    # OpenGL
    glClearColor(0.1, 0.1, 0.1, 1.0)  # fundo cinza escuro
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    # ===== CÂMERA COM ARCBALL =====
    camera = Camera3D(viewer_pos[0], viewer_pos[1], viewer_pos[2])
    arcball = camera.CreateArcball()
    arcball.Attach(win)

    # ===== LUZ POSICIONAL PERTO DA LÂMPADA =====
    light = Light(0.65, 1.7, 0.3, 1.0, "world")
    light.SetAmbient(0.05, 0.05, 0.05)
    light.SetDiffuse(2.5, 2.5, 2.5)
    light.SetSpecular(1.0, 1.0, 1.0)

    # ===== SHADER PHONG COM FOG E BUMP =====
    shader = Shader(light, "world")
    shader.AttachVertexShader("shaders/phong.vert")
    shader.AttachFragmentShader("shaders/phong.frag")
    shader.Link()

    # Configura fog
    shader.UseProgram()
    fogColorLoc = glGetUniformLocation(shader.pid, "fogColor")
    useFogLoc = glGetUniformLocation(shader.pid, "useFog")
    useBumpLoc = glGetUniformLocation(shader.pid, "useBump")
    glUniform3f(fogColorLoc, 0.1, 0.1, 0.1)
    glUniform1i(useFogLoc, 1)
    glUniform1i(useBumpLoc, 1)

    # ===== MATERIAIS =====

    # Material para o tampo da mesa (semi-transparente para reflexão)
    mat_table_top = Material(
        0.6, 0.4, 0.2, 0.3
    )  # Marrom com alpha 0.3 (bem transparente)
    mat_table_top.SetDiffuse(
        0.6, 0.4, 0.2, 0.3
    )  # Fix: Explicitly set diffuse alpha for shader
    mat_table_top.SetSpecular(0.8, 0.8, 0.8, 1.0)
    mat_table_top.SetShininess(64.0)

    # Material branco para objetos texturizados (pernas da mesa)
    mat_white = Material(1.0, 1.0, 1.0, 1.0)
    mat_white.SetSpecular(0.5, 0.5, 0.5, 1.0)
    mat_white.SetShininess(32.0)

    # Verde para esfera com bump
    mat_green = Material(0.1, 0.8, 0.1, 1.0)
    mat_green.SetSpecular(1.0, 1.0, 1.0, 1.0)
    mat_green.SetShininess(64.0)

    # Cinza claro para a xícara
    mat_cup = Material(0.7, 0.7, 0.7, 1.0)
    mat_cup.SetSpecular(0.8, 0.8, 0.8, 1.0)
    mat_cup.SetShininess(128.0)

    # Azul para a lâmpada
    mat_blue = Material(0.1, 0.3, 0.8, 1.0)
    mat_blue.SetSpecular(1.0, 1.0, 1.0, 1.0)
    mat_blue.SetShininess(64.0)

    # ===== TEXTURAS =====
    tex_white = Texture("decal", None, glm.vec3(1.0, 1.0, 1.0))
    tex_wood = Texture("decal", "texturas/wood.jpg")
    tex_paper = Texture("decal", "texturas/paper.jpg")
    tex_noise = Texture("bumpTex", "texturas/noise.png")

    # ===== GEOMETRIAS =====
    cube = Cube()
    sphere = Sphere(64, 64)
    cylinder = Cylinder(32, 1, True)
    cylinder_no_cap = Cylinder(32, 1, False, True)
    cone = Cone(32, True, True)

    # ===== MESA =====
    # Table surface Y = 1.1 (top of table top cube)
    # Cube Y goes from 0 to 1. After Scale(3, 0.1, 2), Y goes from 0 to 0.1
    # Translate to Y=1.0 puts the top surface at Y=1.1

    # Tampo da mesa (será desenhado semi-transparente)
    # Using tex_white instead of tex_wood for transparency
    trf_tampo = Transform()
    trf_tampo.Translate(0.0, 1.0, 0.0)
    trf_tampo.Scale(3.0, 0.1, 2.0)
    node_table_top = Node(None, trf_tampo, [mat_table_top, tex_white], [cube])

    # Pernas da mesa (cubos finos nos 4 cantos)
    # Table top is 3.0 x 2.0, so legs at corners: X = ±1.3, Z = ±0.85
    # Cube Y goes from 0 to 1. After Scale(0.08, 1.0, 0.08), Y goes from 0 to 1.0
    # Translate Y=0 keeps legs from Y=0 to Y=1.0 (just under the table top at Y=1.0)
    leg_positions = [
        (1.3, 0.0, 0.85),  # front-right
        (-1.3, 0.0, 0.85),  # front-left
        (1.3, 0.0, -0.85),  # back-right
        (-1.3, 0.0, -0.85),  # back-left
    ]

    leg_nodes = []
    for pos in leg_positions:
        trf = Transform()
        trf.Translate(pos[0], pos[1], pos[2])
        trf.Scale(0.08, 1.0, 0.08)  # Thin square legs
        leg_nodes.append(Node(None, trf, [mat_white, tex_wood], [cube]))

    node_table_legs = Node(None, nodes=leg_nodes)

    # ===== OBJETOS SOBRE A MESA =====
    # Table surface Y = 1.1

    # PAPEL
    trf_paper = Transform()
    trf_paper.Translate(-0.8, 1.11, 0.3)
    trf_paper.Scale(0.4, 0.02, 0.3)
    node_paper = Node(None, trf_paper, [mat_white, tex_paper], [cube])

    # XÍCARA
    trf_cup = Transform()
    trf_cup.Translate(0.8, 1.2, -0.3)
    trf_cup.Scale(0.15, 0.2, 0.15)
    node_cup = Node(None, trf_cup, [mat_cup, tex_white], [cylinder_no_cap])

    # ESFERA VERDE COM BUMP
    trf_sphere_bump = Transform()
    trf_sphere_bump.Translate(-0.3, 1.4, -0.2)
    trf_sphere_bump.Scale(0.3, 0.3, 0.3)
    node_sphere_bump = Node(None, trf_sphere_bump, [mat_green, tex_noise], [sphere])

    # LÂMPADA
    # Cylinder Y goes from 0 to 1
    # Lamp base: Scale(0.2, 0.04, 0.2) -> Y from 0 to 0.04
    # Place on table at Y=1.1
    trf_lamp_base = Transform()
    trf_lamp_base.Translate(1.15, 1.1, 0.5)
    trf_lamp_base.Scale(0.2, 0.04, 0.2)
    node_lamp_base = Node(None, trf_lamp_base, [mat_blue, tex_white], [cylinder])

    # Lamp stem 1: Scale(0.05, 0.6, 0.05) -> Y from 0 to 0.6
    # Starts at Y=1.14 (above base)
    trf_lamp_stem1 = Transform()
    trf_lamp_stem1.Translate(1.15, 1.14, 0.5)
    trf_lamp_stem1.Scale(0.05, 0.6, 0.05)
    node_lamp_stem1 = Node(None, trf_lamp_stem1, [mat_blue, tex_white], [cylinder])

    # Lamp stem 2 (angled): starts at top of stem 1 (Y=1.74)
    trf_lamp_stem2 = Transform()
    trf_lamp_stem2.Translate(1.15, 1.74, 0.5)
    trf_lamp_stem2.Rotate(45.0, 0.0, 0.0, 1.0)
    trf_lamp_stem2.Scale(0.05, 0.5, 0.05)
    node_lamp_stem2 = Node(None, trf_lamp_stem2, [mat_blue, tex_white], [cylinder])

    trf_lamp_head = Transform()
    trf_lamp_head.Translate(0.65, 1.9, 0.3)
    trf_lamp_head.Rotate(45.0, 1.0, 0.0, 0.0)
    trf_lamp_head.Rotate(-35.0, 0.0, 0.0, 1.0)
    trf_lamp_head.Scale(0.25, 0.3, 0.25)
    node_lamp_head = Node(None, trf_lamp_head, [mat_blue, tex_white], [cone])

    # Grupo de objetos sobre a mesa
    node_objects_on_table = Node(
        None,
        nodes=[
            node_paper,
            node_cup,
            node_sphere_bump,
            node_lamp_base,
            node_lamp_stem1,
            node_lamp_stem2,
            node_lamp_head,
        ],
    )

    # ===== SHADOW SHADER =====
    shadow_shader = Shader(light, "world")
    shadow_shader.AttachVertexShader("shaders/shadow.vert")
    shadow_shader.AttachFragmentShader("shaders/shadow.frag")
    shadow_shader.Link()

    # ===== REFLEXÃO =====
    # Reflete em Y=1.1 (superfície da mesa)
    # Scale(1, -1, 1) espelha em Y=0, então precisamos transladar
    trf_reflection = Transform()
    trf_reflection.Translate(0.0, 2.2, 0.0)  # Move up by 2*1.1
    trf_reflection.Scale(1.0, -1.0, 1.0)  # Mirror
    node_reflection = Node(shader, trf_reflection, nodes=[node_objects_on_table])

    # ===== SOMBRA NA MESA =====
    trf_shadow_table = Transform()
    trf_shadow_table.MultMatrix(shadows.get_shadow_matrix([0.65, 1.7, 0.3], 1.1))
    node_shadow_table = Node(
        shadow_shader, trf_shadow_table, nodes=[node_objects_on_table]
    )

    # Root (não usado diretamente, mas mantemos para compatibilidade)
    scene = Scene(Node(shader))


def display(win):
    """Renderiza a cena com reflexão e sombra na mesa"""
    global camera, shader
    global node_table_top, node_table_legs, node_objects_on_table
    global node_reflection, node_shadow_table

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

    if camera:
        st = State(camera)

        # ═══════════════════════════════════════════════════════════════════
        # 1️⃣ STENCIL PASS - Mark table top area in stencil buffer
        # ═══════════════════════════════════════════════════════════════════
        glEnable(GL_STENCIL_TEST)
        glStencilFunc(GL_ALWAYS, 1, 0xFF)
        glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
        glStencilMask(0xFF)

        # Draw table top to stencil ONLY (no color, no depth)
        glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
        glDepthMask(GL_FALSE)

        shader.Load(st)
        node_table_top.Render(st)
        shader.Unload(st)

        glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
        glDepthMask(GL_TRUE)
        glStencilMask(0x00)  # Stop writing to stencil

        # ═══════════════════════════════════════════════════════════════════
        # 2️⃣ REFLECTION PASS - Draw reflected objects
        # ═══════════════════════════════════════════════════════════════════
        # Fix: Enable stencil test to clip reflection to table surface
        glEnable(GL_STENCIL_TEST)
        glStencilFunc(GL_EQUAL, 1, 0xFF)
        glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)

        # Flip culling for mirrored geometry
        glCullFace(GL_FRONT)

        # Clear depth buffer so reflection can draw
        glClear(GL_DEPTH_BUFFER_BIT)

        # Draw reflection WITH depth writing so table blends properly
        node_reflection.Render(st)

        glCullFace(GL_BACK)

        # ═══════════════════════════════════════════════════════════════════
        # 3️⃣ TABLE TOP PASS - Draw semi-transparent table over reflection
        # ═══════════════════════════════════════════════════════════════════

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Fix: Enable depth test so table blends with reflection but occludes legs
        glEnable(GL_DEPTH_TEST)

        shader.Load(st)
        node_table_top.Render(st)
        shader.Unload(st)

        # Re-enable stencil for shadows
        glEnable(GL_STENCIL_TEST)

        # ═══════════════════════════════════════════════════════════════════
        # 4️⃣ SHADOW PASS - Draw shadows where stencil == 1
        # ═══════════════════════════════════════════════════════════════════
        # Use stencil to clip shadows to table AND prevent double-darkening
        glStencilMask(0xFF)
        glStencilFunc(GL_EQUAL, 1, 0xFF)
        glStencilOp(GL_KEEP, GL_KEEP, GL_INCR)

        glDepthMask(GL_FALSE)

        # Polygon offset to draw shadow slightly above table
        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(-1.0, -1.0)

        node_shadow_table.Render(st)

        glDisable(GL_POLYGON_OFFSET_FILL)
        glDepthMask(GL_TRUE)
        glDisable(GL_STENCIL_TEST)
        glDisable(GL_BLEND)

        # ═══════════════════════════════════════════════════════════════════
        # 5️⃣ TABLE LEGS (opaque)
        # ═══════════════════════════════════════════════════════════════════
        shader.Load(st)
        node_table_legs.Render(st)
        shader.Unload(st)

        # ═══════════════════════════════════════════════════════════════════
        # 6️⃣ OBJECTS ON TABLE (opaque)
        # ═══════════════════════════════════════════════════════════════════
        shader.Load(st)
        node_objects_on_table.Render(st)
        shader.Unload(st)


def keyboard(win, key, scancode, action, mods):
    """Callback de teclado para controles adicionais"""
    if action == glfw.PRESS and key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(win, True)


def main():
    """Função principal do programa"""

    # GLFW
    if not glfw.init():
        print("Erro ao inicializar GLFW")
        return

    # contexto OpenGL
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

    # janela
    win = glfw.create_window(
        1024, 768, "Projeto 02 - Mesa com Fog e Bump Mapping", None, None
    )
    if not win:
        print("Erro ao criar janela GLFW")
        glfw.terminate()
        return

    # teclado
    glfw.set_key_callback(win, keyboard)

    # contexto da janela
    glfw.make_context_current(win)

    print("OpenGL version:", glGetString(GL_VERSION).decode("utf-8"))
    print("")
    print("PROJETO 02 - INF1761 Computação Gráfica")
    print("=" * 50)
    print("Pontuação:")
    print("  • Base (7.0 pts): Mesa + objetos + iluminação Phong")
    print("  • Fog (1.0 pt): Efeito de neblina por distância")
    print("  • Bump mapping (2.0 pts): Rugosidade na esfera verde")
    print("  TOTAL: 10.0 pontos")
    print("")
    print("CONTROLES:")
    print("  • Arraste com o mouse para rotacionar a cena (arcball)")
    print("  • ESC para sair")
    print("=" * 50)
    print("")

    # inicializa a cena
    initialize(win)

    # loop principal
    while not glfw.window_should_close(win):
        display(win)
        glfw.swap_buffers(win)
        glfw.poll_events()

    # finaliza GLFW
    glfw.terminate()


if __name__ == "__main__":
    main()
