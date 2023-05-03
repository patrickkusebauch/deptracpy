from glob import glob
import os


def load_files(paths: list[str]) -> dict[str, list[str]]:
    files: dict[str, list[str]] = {}
    for path in paths:
        results = [
            f for f in glob(f"{path}/**/*.py", recursive=True) if os.path.isfile(f)
        ]
        files[path] = []
        for result in results:
            files[path].append(result.removeprefix(path + "/"))
    return files
