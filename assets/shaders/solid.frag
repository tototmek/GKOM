#version 460 core
out vec4 fragColor;

uniform vec4 material_diffuse;
uniform vec4 material_specular;

uniform vec3 light_direction;
uniform vec3 light_ambient;
uniform vec3 light_diffuse;
uniform vec3 light_specular;

uniform vec3 cameraPos;

in vec3 normal;
in vec3 fragPos;
in vec2 texCoords;
in mat4 viewMatrix;

void main()
{
    vec4 mainColor = material_diffuse;

    vec3 lightDirection = vec3(viewMatrix * vec4(light_direction, 0.0f));

    // ambient
    vec3 ambient = light_ambient * vec3(mainColor);

    // diffuse
    vec3 norm = normalize(vec3(viewMatrix * vec4(normal, 0.0f)));
    vec3 lightDir = normalize(-lightDirection);
    float diffuseStrength = max(dot(norm, lightDir), 0.0f);
    vec3 diffuse = light_diffuse * diffuseStrength * vec3(mainColor);

    // specular
    vec3 viewDir = normalize(-fragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float specularStrength = pow(max(dot(viewDir, reflectDir), 0.0f), 32.0f);
    vec3 specular = light_specular * specularStrength * vec3(material_specular);

    vec3 result = ambient + diffuse + specular;
    fragColor = vec4(result, 1.0f);


}