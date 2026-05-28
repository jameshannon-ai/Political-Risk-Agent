from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import fnmatch


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUTPUT = DIST / "political-risk-agent-clean.zip"

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
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


def main():
    DIST.mkdir(exist_ok=True)
    if OUTPUT.exists():
        OUTPUT.unlink()

    with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED) as zf:
        for path in sorted(ROOT.rglob("*")):
            if path == OUTPUT or path.is_dir() or should_exclude(path):
                continue
            zf.write(path, path.relative_to(ROOT))

    print(OUTPUT)


if __name__ == "__main__":
    main()
