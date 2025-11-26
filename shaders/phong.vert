#version 410

layout(location = 0) in vec4 coord;
layout(location = 1) in vec3 normal;
layout(location = 3) in vec2 texcoord;

uniform mat4 Mv, Mn, Mvp;
uniform vec4 lpos;

out vec3 veye;
out vec3 neye;
out vec3 light;
out vec2 ftexcoord;

void main(void) {
    veye = vec3(Mv * coord);
    neye = normalize(vec3(Mn * vec4(normal, 0.0)));

    if (lpos.w == 0.0)
        light = normalize(vec3(lpos));
    else
        light = normalize(vec3(lpos) - veye);

    ftexcoord = texcoord;
    gl_Position = Mvp * coord;
}