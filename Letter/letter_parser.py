import os
import re
import typing
import itertools


class MultiLineSeparator(typing.TypedDict):
    start: str
    end: str

class LetterParser:
    def __init__(self, path: os.PathLike) -> None:
        self.letter_path = path
        self.single_line_sep = ":-"
        self.multi_line_sep = MultiLineSeparator(start="~-", end="-~")
        self.letter_iterator = iter(self.read_letter_file())

    def parse(self) -> typing.Dict[str, str]:
        configurations = dict()
        for line in self.letter_iterator:
            if self.single_line_sep in line:
                key, value = self.read_single_line(line)
            elif self.multi_line_sep["start"] in line:
                key, value = self.read_multi_line(line)
            elif line == "\n":
                continue
            else:
                raise ValueError(f"Invalid line: {line}")
            configurations[key.strip().capitalize()] = value.strip()
        configurations["Content"] = self.format(configurations["Content"])
        return configurations

    def format(self, content: str) -> str:
        formatted_content = self.format_links(content)
        formatted_content = self.format_email_addresses(formatted_content)
        return formatted_content

    def format_links(self, content: str) -> str:
        # Format Link(Display, URL).
        link_pattern = r'Link\(([^,]+),\s*([^)]+)\)'
        return re.sub(
            link_pattern,
            r'\\href{\2}{\\textcolor{Purple_200}{\\underline{\1}}}',
            content
        )

    def format_email_addresses(self, content: str) -> str:
        # Emails are automatically detected and formatted.
        email_pattern = r'(\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b)'
        return re.sub(
            email_pattern,
            r'\\href{mailto:\1}{\\textcolor{Purple_200}{\\underline{\1}}}',
            content
        )

    def read_single_line(self, line: str) -> typing.Tuple[str, str]:
        return line.split(self.single_line_sep)

    def read_multi_line(self, line: str) -> typing.Tuple[str, str]:
        name = self.determine_multi_line_name(line, default="Content")
        return name, self.read_multi_line_content()

    def read_multi_line_content(self, allow_single_newline=True) -> str:
        content = str()
        parser, pre_parser = itertools.tee(self.letter_iterator)
        next(pre_parser, None)
        for line, next_line in itertools.zip_longest(parser, pre_parser):
            halt = self.multi_line_sep["end"] in line
            if halt:
                break
            current_line_has_text = line != "\n"
            next_line_has_text = next_line != "\n" and next_line is not None
            skip_single_newline = not current_line_has_text and next_line_has_text
            if allow_single_newline or not skip_single_newline:
                content += line
        return content

    def determine_multi_line_name(self, line: str, *, default: str) -> str:
        name = line.split(self.multi_line_sep["start"])[0]
        return name if name != "" else default

    def read_letter_file(self) -> typing.List[str]:
        with open(self.letter_path, "r") as f:
            return f.readlines()


def debug():
    parser = LetterParser("Example.letter")
    import pprint
    pprint.pprint(parser.parse())


if __name__ == "__main__":
    raise RuntimeError("Parser is not meant to be ran directly.")