#version 460 core
out vec4 fragColor;

in vec3 position;
in vec3 normal;
in vec2 texCoords;
in mat4 viewMatrix;

uniform sampler2D material_diffuse;
uniform sampler2D material_specular;

uniform vec3 light_position;
uniform vec3 light_ambient;
uniform vec3 light_diffuse;
uniform vec3 light_specular;

void main()
{
   vec3 diffuseColor = vec3(texture(material_diffuse, texCoords));
   vec3 specularColor = vec3(texture(material_specular, texCoords));

   vec3 lightDirection = vec3(viewMatrix * vec4(position - light_position, 0.0f));

    // ambient
   vec3 ambient = light_ambient * diffuseColor;

    // diffuse
   vec3 norm = normalize(vec3(viewMatrix * vec4(normal, 0.0f)));
   vec3 lightDir = normalize(-lightDirection);
   // vec3 lightDir = vec3(0.0f, 1.0f, 0.0f);
   float diffuseStrength = max(dot(norm, lightDir), 0.0f);
   vec3 diffuse = light_diffuse * diffuseStrength * diffuseColor;

    // specular
   vec3 viewDir = normalize(-position);
   vec3 reflectDir = reflect(-lightDir, norm);
   float specularStrength = pow(max(dot(viewDir, reflectDir), 0.0f), 32.0f);
   vec3 specular = light_specular * specularStrength * specularColor;

   vec3 result = ambient + diffuse + specular;
   fragColor = vec4(result,  1.0f);
}