#! /usr/bin/python

import cli


def main():
    args = cli.parse_arguments()
    print(f"Model: {args.model_path}")
    print(f"Algorithm: {args.algorithm}")


if __name__ == "__main__":
    main()
