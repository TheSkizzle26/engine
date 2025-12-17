/*
 * Do not look at this code. You were warned.
 */

/*
 * TODOs:
 *  - make random pow values in force calculations customizable
 *  - clean up code
 */


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

struct Force {
    vec2 pos;
    float dist;
    float force;
};

layout(std430, binding=0) buffer TextureDataBuffer {
    TextureData textures[];
};

layout(std430, binding=1) buffer ObjectBuffer {
    Object objects[];
};

layout(std430, binding=2) buffer ForceBuffer {
    Force forces[];
};

in vec2 in_vert;

out vec2 uv;
out float tex_idx;

uniform float num_forces;

uniform vec2 RES;
uniform vec2 atlas_size;

uniform vec2 camera_offset;
uniform float camera_scale;

uniform float time;
uniform float delta;
uniform float adaptivity;
uniform float wind_speed;
uniform float wind_force;


void update(in Object obj) {
    float target_angle = 0;

    // calculate forces
    for (int i = 0; i < num_forces; i++) {
        Force force_data = forces[i];
        vec2 pos = force_data.pos;
        float dist = force_data.dist;
        float force = force_data.force;

        float dist_to_pos = length(vec2(
               abs(obj.pos.x - pos.x),
               abs(obj.pos.y - pos.y) * 3
                                   //pow(abs(obj.pos.y - pos.y), 1.4)
               ));

        float obj_force = 1 - pow((dist_to_pos / dist), 0.8);
        //loat obj_force = 1 - (dist_to_pos / dist);
        obj_force = max(0, obj_force);

        float mult = 1;
        if (obj.pos.x < pos.x) { mult = -1; }

        target_angle += obj_force * force * mult;
    }

    int inst = gl_InstanceID;
    objects[inst].angle += (target_angle - obj.angle) * adaptivity * delta;
}

void calculate_position(in Object obj, in float master_angle) {
    TextureData tex = textures[int(obj.tex_idx)];

    uv = in_vert;
    vec2 pos = in_vert;

    // calculate pixel coordinate
    pos *= tex.size;
    pos -= tex.origin;

    // rotate
    float c = cos(master_angle + obj.angle);
    float s = sin(master_angle + obj.angle);
    float old_x = pos.x;
    pos.x = pos.x * c - pos.y * s;
    pos.y = old_x * s + pos.y * c;

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

void main() {
    Object obj = objects[gl_InstanceID];
    tex_idx = obj.tex_idx;
    float master_angle = sin(time * wind_speed + obj.pos.y / 80 + obj.pos.x / 40) * wind_force;

    update(obj);
    calculate_position(obj, master_angle);
}