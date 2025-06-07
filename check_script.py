from pathlib import Path
import re

# Load your file
file_path = Path("MidsummerDream.txt")
text = file_path.read_text(encoding="utf-8", errors="replace")

# Find non-ASCII characters
non_ascii_matches = list(re.finditer(r"[^\x00-\x7F]", text))

if non_ascii_matches:
    print(f"Found {len(non_ascii_matches)} non-ASCII characters:")
    for match in non_ascii_matches:
        char = match.group()
        pos = match.start()
        print(f"U+{ord(char):04X} at position {pos}: '{char}'")
else:
    print("No non-ASCII characters found.")

# Detect unusual control characters (except newline and tab)
control_matches = list(re.finditer(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", text))

if control_matches:
    print(f"Found {len(control_matches)} control characters:")
    for match in control_matches:
        char = match.group()
        pos = match.start()
        print(f"U+{ord(char):04X} at position {pos}")
else:
    print("No unusual control characters found.")

data = Path("MidsummerDream.txt").read_bytes()

print(f"\\r found: {data.count(b'\\r')}")
print(f"\\n found: {data.count(b'\\n')}")