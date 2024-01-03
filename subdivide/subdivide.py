#! /usr/bin/python

import cli
import model_io


def main():
    args = cli.parse_arguments()
    print(f"Model: {args.model_path}")
    print(f"Algorithm: {args.algorithm}")
    vertices, faces = model_io.load_model(args.model_path)
    print(vertices)
    print(faces)


if __name__ == "__main__":
    main()
