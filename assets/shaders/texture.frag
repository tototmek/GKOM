#version 460 core
out vec4 fragColor;

struct Material {
    sampler2D texture1;
    sampler2D texture2;
};

struct DirectionalLight {
    vec3 direction;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

uniform Material material;
uniform DirectionalLight light;

uniform vec3 cameraPos;

in vec3 normal;
in vec3 fragPos;
in vec2 texCoords;
in mat4 viewMatrix;

void main()
{
    vec4 mainColor = texture(material.texture1, texCoords);
    if (mainColor.a < 0.05f) {
        discard;
    }

    vec3 lightDirection = vec3(viewMatrix * vec4(light.direction, 0.0f));

    // ambient
    vec3 ambient = light.ambient * vec3(mainColor);

    // diffuse
    vec3 norm = normalize(vec3(viewMatrix * vec4(normal, 0.0f)));
    vec3 lightDir = normalize(-lightDirection);
    float diffuseStrength = max(dot(norm, lightDir), 0.0f);
    vec3 diffuse = light.diffuse * diffuseStrength * vec3(mainColor);

    // specular
    vec3 viewDir = normalize(-fragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float specularStrength = pow(max(dot(viewDir, reflectDir), 0.0f), 32.0f);
    vec3 specular = light.specular * specularStrength * vec3(texture(material.texture2, texCoords));

    vec3 result = ambient + diffuse + specular;
    fragColor = vec4(result, 1.0f);
}