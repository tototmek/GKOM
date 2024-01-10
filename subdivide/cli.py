import argparse
import os
import mesh_io
import re
import glm

supported_file_extensions = mesh_io.model_loaders.keys()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Visualize 3d model subdivision alogrithms."
    )
    parser.add_argument(
        "model_path",
        type=str,
        help=f"Path to the 3D model. Supported extensions: {', '.join(supported_file_extensions)}",
    )
    parser.add_argument(
        "algorithm",
        choices=["loop", "catmull-clark"],
        help="Chosen subdivision algorithm",
    )
    parser.add_argument(
        "-w",
        "--wireframe",
        action="store_true",
        help="Render the model wireframe.",
    )
    parser.add_argument(
        "--diffuse-color",
        type=str,
        help='Material diffuse color, default: "#ffffff"',
        default="#ffffff",
    )
    parser.add_argument(
        "--specular-color",
        type=str,
        help='Material specular color, default: "#ffffff"',
        default="#ffffff",
    )
    parser.add_argument(
        "--diffuse-texture",
        type=str,
        help="Path to a texture for material's diffuse channel",
    )
    parser.add_argument(
        "--specular-texture",
        type=str,
        help="Path to a texture for material's specular channel",
    )
    return validate_args(parser.parse_args())


def validate_path(path):
    if not os.path.isfile(path):
        print(f"Error: The specified file '{path}' does not exist.")
        exit(1)

    if not os.access(path, os.R_OK):
        print(f"Error: Error: Cannot access '{path}: Permission denied.'")
        exit(1)


def validate_color(color):
    color_pattern = re.compile(r"^#[0-9a-fA-F]{6}$")
    if not color_pattern.match(color):
        print(
            f"Error: '{color}' is not a valid hexadecimal color code. Use following format: #ffffff"
        )
        exit(1)


def parse_color(color_code: str) -> glm.vec3:
    color_code = color_code.lstrip("#")
    r = int(color_code[0:2], 16) / 255.0
    g = int(color_code[2:4], 16) / 255.0
    b = int(color_code[4:6], 16) / 255.0
    return glm.vec3(r, g, b)


def validate_args(args):
    file_extension = os.path.splitext(args.model_path)[1][1:].lower()
    if file_extension not in supported_file_extensions:
        print(
            f"Error: Unsupported file extension '{file_extension}'. Supported extensions are: {', '.join(supported_file_extensions)}"
        )
        exit(1)

    validate_path(args.model_path)

    if args.diffuse_texture:
        validate_path(args.diffuse_texture)

    if args.specular_texture:
        validate_path(args.specular_texture)

    validate_color(args.diffuse_color)
    args.diffuse_color = parse_color(args.diffuse_color)
    validate_color(args.specular_color)
    args.specular_color = parse_color(args.specular_color)

    return args
