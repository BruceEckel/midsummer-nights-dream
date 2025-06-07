"""
Move each indented parenthesized line of the form "(…)" that immediately follows
an all-caps character name so that the "(…)" line comes before the name.

For example:

    BOTTOM
            (as Pyramus)

becomes:

            (as Pyramus)
    BOTTOM
"""
import argparse
import re
from pathlib import Path

# A line that's an indented "(…)"
stage_note_pattern: re.Pattern[str] = re.compile(r'^\s{4,}\(([^)]+)\)\s*$')
# S line of all caps (and spaces)
character_name_pattern: re.Pattern[str] = re.compile(r'^[A-Z]{3,}[A-Z ]*$')

def reorder(file_path: Path, fixed_file_path: Path) -> None:
    text = file_path.read_text(encoding='utf-8')
    lines = text.splitlines()
    new_lines: list[str] = []

    i = 0
    while i < len(lines):
        line = lines[i]
        # if current is name and next is "(…)", swap their order
        if (
                i + 1 < len(lines)
                and character_name_pattern.match(line)
                and (stage_note_pattern.match(lines[i + 1]))
        ):
            # keep the exact indent of the "(…)" line
            new_lines.append(lines[i + 1])
            new_lines.append(line)
            i += 2
        else:
            new_lines.append(line)
            i += 1

    fixed_file_path.write_text('\n'.join(new_lines), encoding='utf-8')


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Reorder stage instruction lines to come before the preceding all-caps character name"
    )
    parser.add_argument('file', type=Path, help='Path to the text file to process')
    parser.add_argument('outfile', type=Path, help='Path to the processed output file')
    args = parser.parse_args()

    reorder(args.file, args.outfile)


if __name__ == '__main__':
    main()
