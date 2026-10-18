from fnmatch import fnmatchcase
from pathlib import Path


def _is_excluded(rules, path):
    excluded = False
    for rule in rules:
        negated = rule.startswith("!")
        pattern = rule[1:] if negated else rule
        directory_pattern = pattern.rstrip("/")
        if (
            fnmatchcase(path, pattern)
            or fnmatchcase(Path(path).name, pattern)
            or (pattern.endswith("/") and path.startswith(directory_pattern + "/"))
        ):
            excluded = not negated
    return excluded


def test_docker_build_contexts_exclude_environment_files_and_local_artifacts():
    project_root = Path(__file__).resolve().parents[2]
    for relative in ("backend/.dockerignore", "frontend/.dockerignore"):
        dockerignore = project_root / relative
        rules = [
            line.strip()
            for line in dockerignore.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        for filename in (".env", ".env.example", ".env.production"):
            assert _is_excluded(rules, filename), f"{filename} must be excluded from {relative}"
    backend_rules = [line.strip() for line in (project_root / "backend/.dockerignore").read_text(encoding="utf-8").splitlines()]
    assert _is_excluded(backend_rules, "uploads/avatars/photo.jpg")
    frontend_rules = [line.strip() for line in (project_root / "frontend/.dockerignore").read_text(encoding="utf-8").splitlines()]
    assert _is_excluded(frontend_rules, "node_modules/package/index.js")
