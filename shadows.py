import glm


def get_shadow_matrix(light_pos, plane_y=0.0):
    """
    Returns the shadow projection matrix for a light at light_pos
    projecting onto the plane Y=plane_y.

    Args:
        light_pos: (x, y, z) position of the light
        plane_y: Y coordinate of the projection plane (default 0.0 for floor)

    The approach:
    1. Translate scene so plane is at Y=0
    2. Apply standard shadow projection for Y=0
    3. Translate back
    """
    Lx, Ly, Lz = light_pos[0], light_pos[1], light_pos[2]

    # Light height relative to the target plane
    Ly_rel = Ly - plane_y

    # Standard shadow projection matrix for Y=0 plane
    # (from the original project specification)
    # This projects points onto Y=0 from a light at (Lx, Ly_rel, Lz)
    shadow_y0 = glm.mat4(
        Ly_rel,
        0,
        0,
        0,  # Column 0
        -Lx,
        0,
        -Lz,
        -1,  # Column 1
        0,
        0,
        Ly_rel,
        0,  # Column 2
        0,
        0,
        0,
        Ly_rel,  # Column 3
    )

    # For non-zero plane_y:
    # 1. Translate down by plane_y (move plane to Y=0)
    # 2. Apply shadow projection
    # 3. Translate up by plane_y (move result back)

    if plane_y != 0.0:
        T_down = glm.translate(glm.mat4(1.0), glm.vec3(0, -plane_y, 0))
        T_up = glm.translate(glm.mat4(1.0), glm.vec3(0, plane_y, 0))
        return T_up * shadow_y0 * T_down
    else:
        return shadow_y0
