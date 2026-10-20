from pathlib import Path
import ast
import sys

root = Path(__file__).resolve().parent
missing = []
for script in ("server.py", "run_pipeline.py"):
    path = root / script
    if not path.exists():
        continue
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=script)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("src."):
            target = root.joinpath(*node.module.split("."))
            if not target.with_suffix(".py").is_file() and not (target / "__init__.py").is_file():
                missing.append(f"{script}:{node.lineno}: {node.module} (expected {target.relative_to(root)}.py)")
if missing:
    print("ERROR: Missing source modules in Docker build context:", file=sys.stderr)
    print("\n".join(missing), file=sys.stderr)
    print("Commit the original src/ folder to GitHub before redeploying.", file=sys.stderr)
    sys.exit(1)
print("Source module files verified.")
