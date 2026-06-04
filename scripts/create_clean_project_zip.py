from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import argparse
import fnmatch


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DEFAULT_OUTPUT = DIST / "political-risk-agent-clean.zip"

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "dist",
}

EXCLUDED_FILES = {
    ".env",
    ".DS_Store",
}

EXCLUDED_PATTERNS = [
    "*.zip",
    "*.pyc",
]


def should_exclude(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    parts = set(relative.parts)
    if parts & EXCLUDED_DIRS:
        return True
    if relative.name in EXCLUDED_FILES:
        return True
    if relative.parts and relative.parts[0] == "outputs" and relative.name != ".gitkeep":
        return True
    return any(fnmatch.fnmatch(relative.name, pattern) for pattern in EXCLUDED_PATTERNS)


def _parse_args():
    parser = argparse.ArgumentParser(description="Create a clean shareable project zip.")
    parser.add_argument(
        "output_name",
        nargs="?",
        default=DEFAULT_OUTPUT.name,
        help="Output zip filename or path. Relative paths are written under dist/.",
    )
    return parser.parse_args()


def _resolve_output(output_name: str) -> Path:
    output = Path(output_name)
    if not output.is_absolute():
        output = DIST / output
    return output


def main():
    args = _parse_args()
    output = _resolve_output(args.output_name)
    DIST.mkdir(exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    with ZipFile(output, "w", compression=ZIP_DEFLATED) as zf:
        for path in sorted(ROOT.rglob("*")):
            if path == output or path.is_dir() or should_exclude(path):
                continue
            zf.write(path, path.relative_to(ROOT))

    print(output)


if __name__ == "__main__":
    main()
