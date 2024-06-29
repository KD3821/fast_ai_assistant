import os
import json
from pathlib import Path

from src.settings import fast_ai_settings


def create_json_file(file_data, file_name, dir_name):
    dir_path = Path(f"{fast_ai_settings.docs_dir}/{dir_name}")

    if not os.path.exists(dir_path):
        dir_path.mkdir(parents=True)

    file_path = os.path.join(dir_path, file_name)

    with open(file_path, 'w') as f:
        json.dump(file_data, f, indent=2)
