from pathlib import Path

print(__file__)
Path(__file__).relative_to(Path.cwd())
