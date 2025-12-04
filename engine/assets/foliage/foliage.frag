#version 450 core

in vec2 uv;
in float instance_id;
out vec4 f_color;

struct Object {
    vec2 pos;
    int texture_idx;
    float angle;
};

struct TextureData {
    vec2 size;
    vec2 origin;
    int atlas_x;
    int _pad1, _pad2, _pad3;
};

layout(std430, binding=0) buffer ObjectsBuffer {
    Object objects[];
};

layout(std430, binding=1) buffer TextureDataBuffer {
    TextureData texture_data[];
};

uniform sampler2D atlas;
uniform vec2 atlas_size;


void main() {
    Object cur = objects[int(instance_id)];
    TextureData tex = texture_data[cur.texture_idx];

    vec2 pos = vec2(
            float(tex.atlas_x) / atlas_size.x,
            0.0
    );

    vec2 size = tex.size / atlas_size;

    f_color = texture(atlas, pos + uv * size);
}