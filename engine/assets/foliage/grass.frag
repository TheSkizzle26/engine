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

uniform sampler2D atlas;
uniform vec2 atlas_size;

uniform bool render_ao;


void main() {
    TextureData tex = textures[int(tex_idx)];

    vec2 tex_pos = vec2(
        tex.atlas_x / atlas_size.x,
        0
    );
    vec2 tex_size = tex.size / atlas_size;

    vec4 color = texture(atlas, tex_pos + uv * tex_size);

    if (render_ao) {
        float tex_uv_y = uv.y / (tex.origin.y / tex.size.y);

        float b = 1 - pow(tex_uv_y, 1.333) * 0.6;
        color.x *= b;
        color.y *= b;
        color.z *= b;
    }

    f_color = color;
}