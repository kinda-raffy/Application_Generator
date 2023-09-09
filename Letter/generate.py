"""
Usage:
  generate.py LETTER_CONTEXT_FILE_PATH [-o OUTPUT_PDF_DIR] [--no-name-stamp] [--parse-only]

Options:
  -o OUTPUT_PDF_DIR      Generates the PDF file at the given path. [default: build/]
  --no-name-stamp        Do not prepend PDF name with "Cover_Letter_Rafat_Mahiuddin".
  --parse-only           Only parse the letter context file into configuration files.
"""


import os
import shutil
import typing
import docopt
import letter_parser


default_configuration = {
    "Location": "Melbourne, VIC",
    "Recipient": "Hiring Manager",
    "Closing": "Warm Regards",
}


class Generator:
    def __init__(
        self,
        context_file_path: os.PathLike,
        output_pdf_path: os.PathLike,
        no_pdf_name_stamp: typing.Optional[bool] = False,
        parse_only: typing.Optional[bool] = False
    ) -> None:
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.config_directory = os.path.join(self.script_directory, "config")
        self.build_directory = os.path.join(self.script_directory, "build")
        self.prepare_configuration_directory()
        self.context_file_path = context_file_path
        self.context_file_name = self.retreive_context_file_name()
        self.output_pdf_path = output_pdf_path
        self.no_pdf_name_stamp = no_pdf_name_stamp
        self.parse_only = parse_only

    def generate(self) -> None:
        parser = letter_parser.LetterParser(self.context_file_path)
        config = default_configuration.copy()
        parsed_config = parser.parse()
        config.update(parsed_config)
        self.write_configuration(config)
        if self.parse_only:
            return
        self.clean_build_directory()
        self.generate_pdf()
        self.move_pdf_to_output_directory()

    def move_pdf_to_output_directory(self) -> None:
        pdf_name = self.context_file_name
        if not self.no_pdf_name_stamp:
            pdf_name = "Cover_Letter_Rafat_Mahiuddin_" + pdf_name
        shutil.move(
            os.path.join(self.build_directory, f"{self.context_file_name}.pdf"),
            os.path.join(self.output_pdf_path, f"{pdf_name}.pdf")
        )

    def generate_pdf(self) -> None:
        os.system(
            'lualatex  -synctex=1 -interaction=nonstopmode ' +
            '-file-line-error -recorder ' +
            f'-output-directory="{os.path.join(self.script_directory, "build")}" ' +
            f'-jobname={self.context_file_name} ' +
            f'"{os.path.join(self.script_directory, "./Cover_Letter.tex")}"'
        )

    def clean_build_directory(self) -> None:
        shutil.rmtree(self.build_directory, ignore_errors=True)
        os.makedirs(self.build_directory)

    def write_configuration(self, config: dict[str, str]) -> None:
        for key, value in config.items():
            self.create_tex_file(key, value)

    def create_tex_file(self, name: str, content: str) -> None:
        with open(os.path.join(self.config_directory, f"{name}.tex"), "w") as f:
            f.write(content)

    def prepare_configuration_directory(self) -> None:
        shutil.rmtree(self.config_directory, ignore_errors=True)
        os.makedirs(self.config_directory)

    def retreive_context_file_name(self) -> str:
        return os.path.splitext(os.path.basename(self.context_file_path))[0]


def main():
    arguments = docopt.docopt(__doc__)
    context_file_path = arguments["LETTER_CONTEXT_FILE_PATH"]
    if not os.path.isfile(context_file_path):
        raise FileNotFoundError(f"File not found: {context_file_path}")
    output_pdf_path = arguments["-o"]
    if output_pdf_path != "build/" and not os.path.isdir(output_pdf_path):
        raise NotADirectoryError(f"Directory not found: {output_pdf_path}")
    generator = Generator(
        context_file_path, output_pdf_path,
        arguments["--no-name-stamp"], arguments["--parse-only"]
    )
    generator.generate()


if __name__ == "__main__":
    main()