from pathlib import Path
import re

play = Path("MidsummerDream.txt").read_text(encoding="utf-8")

# Pattern: start of line, followed by 3+ capital letters
pattern = re.compile(r"^[A-Z]{3,}.*", re.MULTILINE)

for match in pattern.finditer(play):
    print(match.group())
