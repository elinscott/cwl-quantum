import contextlib
from typing import Union
from pathlib import Path
import os


@contextlib.contextmanager
def chdir(path: Union[Path, str]):
    # Allows for the context "with chdir(path)". All code within this
    # context will be executed in the directory "path"

    # Ensure path is a Path object
    if not isinstance(path, Path):
        path = Path(path)

    this_dir = Path.cwd()

    # Create path if it does not exist
    path.mkdir(parents=True, exist_ok=True)

    # Move to the directory
    os.chdir(path)
    try:
        yield
    finally:
        # Return to the original directory
        os.chdir(this_dir)


def populate_listings(obj):
    if not isinstance(obj, (dict, list)):
        return

    if isinstance(obj, list):
        for v in obj:
            if isinstance(v, (dict, list)):
                populate_listings(v)
        return

    keys = list(obj.keys())
    for k in keys:
        v = obj[k]
        if isinstance(v, (dict, list)):
            populate_listings(v)
        elif k == 'class' and v in ['File', 'Directory']:
            obj['path'] = str(Path(obj['path']).resolve())
            obj['basename'] = Path(obj['path']).name
            if v == 'File':
                obj['contents'] = None
            else:
                obj['listing'] = None
    return
