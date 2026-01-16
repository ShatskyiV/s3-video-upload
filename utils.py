from datetime import datetime, UTC
from pathlib import Path
from test_files_generator.test_file import TestFile
from test_files_generator.generator import TestFileGenerator

import json

def generate_test_file(name: str, extention: str, size_gb: float, dir_path: Path) -> None:
    """
    Generate file for test
    """
    dir_path.mkdir(parents=True, exist_ok=True)
    path = dir_path / f'{name}.{extention}'
    tf = TestFile(name=name, extention=extention, size_gb=size_gb, path=path)
    TestFileGenerator(tf).generate()


def get_all_files_from_dir(path_to_dir: Path) -> set:
    """
    Get all files from directory as set of Path
    """
    files = [file for file in path_to_dir.iterdir() if file.is_file() and file.name != ".DS_Store"]
    return set(files)

def build_index(prefix, files):
    files.sort(key=lambda x: x.name)
    index = {
        "dataset": prefix,
        "files": []
    }

    for f in files:
        index["files"].append({
            "name": f.name,
            "size": f.path.stat().st_size,
            "last_modified": datetime.fromtimestamp(f.path.stat().st_mtime, UTC).isoformat() + "Z"
        })

    return index

def build_metadata(prefix, file_count):
    return {
        "dataset": prefix,
        "created_at": datetime.now(UTC).isoformat() + "Z",
        "file_count": file_count,
        "owner": "qa"
    }

def create_and_upload_json_data_file(name, data, client, bucket_name, file_path=None, prefix=''):
    if not file_path:
        file_path = Path(f"{name}.json")
    file_path.write_text(json.dumps(data, indent=2))
    client.upload_file(file_path, bucket_name, f"{prefix}_{file_path.name}")