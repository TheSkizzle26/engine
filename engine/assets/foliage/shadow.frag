#version 430 core

struct TextureData {
    vec2 size;
    vec2 origin;
    float atlas_x;
    float _pad;
};

struct Object {
    vec2 pos;
    float angle;
    float tex_idx;
};

layout(std430, binding=0) buffer TextureDataBuffer {
    TextureData textures[];
};

layout(std430, binding=1) buffer ObjectBuffer {
    Object objects[];
};

in vec2 uv;
out vec4 f_color;

in float tex_idx;

uniform float shadow_darkness;


void main() {
    float a = clamp(1 - length(uv - 0.5)*2, 0, 1);
    a = pow(a, 2);

    f_color = vec4(0, 0, 0, a * shadow_darkness);
}