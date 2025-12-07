#version 330

in vec2 fragTexCoord;
in vec4 fragColor;
out vec4 finalColor;

uniform sampler2D texture0;
uniform float shadowDarkness;


void main() {
    vec2 uv = fragTexCoord - vec2(0.5);
    float b = 1 - (length(uv) * 2.0);

    finalColor = vec4(0.0, 0.0, 0.0, b * shadowDarkness);
}