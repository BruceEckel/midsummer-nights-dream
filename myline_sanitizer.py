from pathlib import Path
import re
from dataclasses import dataclass

@dataclass
class Config:
    input_file: Path
    output_file: Path

# Customize input/output filenames here
config = Config(
    input_file=Path("MidsummerDream.txt"),
    output_file=Path("MidsummerDream_clean.txt")
)

# Patterns
speaker_re = re.compile(r"^\s*([A-Z][A-Z ]{2,})\s*$")
stage_direction_re = re.compile(r"^\s*\(.*?\)\s*$")
inline_stage_direction_re = re.compile(r"\(.*?\)")
act_scene_re = re.compile(r"^\s*(ACT|SCENE)\b.*$", re.IGNORECASE)

def sanitize_script(text: str) -> str:
    lines = text.splitlines()
    output = []
    current_speaker = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Preserve Act/Scene headers, uppercased
        if act_scene_re.match(line):
            output.append("")
            output.append(line.upper())
            output.append("")
            current_speaker = None
            continue

        # Skip full-line stage directions
        if stage_direction_re.match(line):
            continue

        # New speaker detected
        match = speaker_re.match(line)
        if match:
            current_speaker = match.group(1).strip()
            output.append("")
            output.append(current_speaker)
            continue

        # Remove inline stage directions
        cleaned_line = inline_stage_direction_re.sub("", line).strip()

        if current_speaker:
            output.append(cleaned_line)
        else:
            # No speaker detected; optionally skip these lines or include them
            # Here we skip lines that don't belong to a speaker
            continue

    return "\n".join(output)

def main(config: Config) -> None:
    text = config.input_file.read_text(encoding="utf-8")
    cleaned = sanitize_script(text)
    config.output_file.write_text(cleaned, encoding="utf-8")
    print(f"Sanitized script written to: {config.output_file}")

if __name__ == "__main__":
    main(config)
