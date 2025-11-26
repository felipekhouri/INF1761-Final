#version 410
layout(location = 0) in vec3 position;
uniform mat4 Mvp;
void main() {
    gl_Position = Mvp * vec4(position, 1.0);
}
