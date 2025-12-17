/*
 * Do not look at this code. You were warned.
 */

/*
 * TODOs:
 *  - make random pow values in force calculations customizable
 *  - clean up code
 */


#version 430 core

struct Object {
    vec2 pos;
    float angle;
    float tex_idx;
};

layout(std430, binding=1) buffer ObjectBuffer {
    Object objects[];
};

in vec2 in_vert;

out vec2 uv;
out float tex_idx;

uniform vec2 RES;
uniform vec2 shadow_size;

uniform vec2 camera_offset;
uniform float camera_scale;


void main() {
    Object obj = objects[gl_InstanceID];

    uv = in_vert;
    vec2 pos = in_vert;

    // calculate pixel coordinate
    pos *= shadow_size;
    pos -= shadow_size*0.5;

    // add object coordinate
    pos += obj.pos;

    // calculate camera coordinate
    pos *= camera_scale;

    // still calculating camera coordinate
    pos += camera_offset;

    // calculate screen coordinate
    pos /= RES;
    pos *= 2; // screen is 2 units wide
    pos.y *= -1;
    gl_Position = vec4(vec2(-1, 1) + pos, 0, 1);
}