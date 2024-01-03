import argparse
import os
import model_io

supported_file_extensions = model_io.model_loaders.keys()


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
    return validate_args(parser.parse_args())


def validate_args(args):
    file_extension = os.path.splitext(args.model_path)[1][1:].lower()
    if file_extension not in supported_file_extensions:
        print(
            f"Error: Unsupported file extension '{file_extension}'. Supported extensions are: {', '.join(supported_file_extensions)}"
        )
        exit(1)

    if not os.path.isfile(args.model_path):
        print(f"Error: The specified file '{args.model_path}' does not exist.")
        exit(1)

    if not os.access(args.model_path, os.R_OK):
        print(f"Error: Error: Cannot access '{args.model_path}: Permission denied.'")
        exit(1)

    return args
