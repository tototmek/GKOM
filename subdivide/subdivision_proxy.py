import model


class SubdivisionRunner:
    def __init__(self, subdivision_function) -> None:
        self.function = subdivision_function
        self.meshes = {}  # subdivided meshes for each level

    def compute(self, vertices, faces, max_subdivision_level):
        self.meshes[0] = (vertices, faces)
        for level in range(1, max_subdivision_level + 1):
            print(f"Computing subdivision {level}...")
            prev_mesh = self.meshes[level - 1]
            self.meshes[level] = self.function(prev_mesh[0].copy(), prev_mesh[1].copy())

    def get_mesh(self, level):
        return self.meshes[level]


def meshes_to_models(meshes: dict):
    models = {}
    for key, value in meshes.items():
        models[key] = model.Model(value[0], value[1])
    return models


class SubdivisionProxy:
    def __init__(
        self, subdivision_function, vertices, faces, max_subdivision_level
    ) -> None:
        self.subdivider = SubdivisionRunner(subdivision_function)
        self.subdivider.compute(vertices, faces, max_subdivision_level)
        self.models = meshes_to_models(self.subdivider.meshes)
        self.level = 0
        self.max_level = max_subdivision_level

    def get_next_model(self):
        self.level = min(self.level + 1, self.max_level)
        return self.get_current_model()

    def get_previous_model(self):
        self.level = max(self.level - 1, 0)
        return self.get_current_model()

    def get_current_model(self):
        return self.models[self.level]
