import os


def main(output_dir: str) -> None:
    print(output_dir)


if __name__ == "__main__":
    directory_path = os.environ.get("OUTPUT_DIR")

    main(directory_path)
