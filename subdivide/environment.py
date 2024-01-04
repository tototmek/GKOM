import glm


class Light:
    position: glm.vec3
    ambient: glm.vec3
    diffuse: glm.vec3
    specular: glm.vec3


class Environment:
    view_matrix: glm.mat4
    projection_matrix: glm.mat4
    light: Light
    material_diffuse: glm.vec3
    material_specular: glm.vec3
