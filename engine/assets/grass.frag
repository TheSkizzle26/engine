#version 330

in vec2 fragTexCoord;
in vec4 fragColor;
out vec4 finalColor;

uniform sampler2D texture0;


void main() {
    vec4 color = texture(texture0, fragTexCoord);

    float b = 1 - pow(fragTexCoord.y, 1.15) * 1.3;
    color.x *= b;
    color.y *= b;
    color.z *= b;

    finalColor = color;
}