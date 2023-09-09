import letter_parser
import os
import shutil
import argparse


class Generator:
    def __init__(self) -> None:
        self.directory = os.path.join(os.getcwd(), "config")
        self.prepare_configuration_directory()

    def generate(self, path: os.PathLike) -> None:
        parser = letter_parser.LetterParser(path)
        config = parser.parse()
        self.write_configuration(config)

    def write_configuration(self, config: dict[str, str]) -> None:
        for key, value in config.items():
            self.create_tex_file(key, value)

    def create_tex_file(self, name: str, content: str) -> None:
        with open(os.path.join(self.directory, f"{name}.tex"), "w") as f:
            f.write(content)

    def prepare_configuration_directory(self) -> None:
        shutil.rmtree(self.directory, ignore_errors=True)
        os.makedirs(self.directory)


def main():
    generator = Generator()
    generator.generate("Company.letter")


if __name__ == "__main__":
    main()