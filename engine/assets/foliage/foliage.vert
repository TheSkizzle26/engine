#version 450 core

in vec2 in_vert;
out vec2 uv;
out float instance_id;

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

uniform vec2 RES;
uniform vec2 camera_offset;
uniform float camera_scale;


void main() {
    uv = in_vert;
    instance_id = gl_InstanceID;

    Object cur = objects[gl_InstanceID];
    TextureData texture = texture_data[0];

    vec2 pos = (camera_scale * 2 * cur.pos) / RES * vec2(1, -1);
    vec2 size = (camera_scale * 2 * texture.size) / RES;

    gl_Position = vec4(pos + in_vert * size, 0.0, 1.0);
}