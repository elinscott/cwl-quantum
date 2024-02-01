"""Utilities for the cwl_quantum package."""

import contextlib
import os
from pathlib import Path
from typing import Any, Union


@contextlib.contextmanager
def chdir(path: Union[Path, str]):
    """Context manager for working in a directory.

    Allows for the context "with chdir(path)". All code within this
    context will be executed in the directory "path"

    :param path: The directory to work in
    :type path: Union[Path, str]
    """
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


def populate_listings(obj: Any) -> None:
    """Recursively add information that CWL expects to the provided object.

    For Files and Directory entries, CWL expects various fields to be populated. However, several of these fields are
    not strictly necessary and it is onerous to demand a user to specify them manually. Instead, one can use this
    function to automatically populate these fields.

    :param obj: The object to check for Files and Directories
    :type obj: Any
    """
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
        elif k == "class" and v in ["File", "Directory"]:
            obj["path"] = str(Path(obj["path"]).resolve())
            obj["basename"] = Path(obj["path"]).name
            if v == "File":
                obj["contents"] = None
            else:
                obj["listing"] = None
    return

def convert_cwl_files_to_paths(dct: Any) -> None:
    """Convert any CWL File/Directory objects to Path objects recursively."""

    if isinstance(dct, dict):
        for k, v in dct.items():
            if isinstance(v, dict) and v.get("class", None) in ['File', 'Directory']:
                dct[k] = Path(v['path'])
            else:
                convert_cwl_files_to_paths(v)
    elif isinstance(dct, list):
        for v in dct:
            convert_cwl_files_to_paths(v)
    return

def convert_paths_to_cwl_files(obj: Any) -> None:
    """Convert any Path objects to CWL File/Directory objects recursively."""

    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, Path):
                cwl_dct = {'class': 'File', 'path': str(v)}
                populate_listings(cwl_dct)
                obj[k] = cwl_dct
            else:
                convert_paths_to_cwl_files(v)

    elif isinstance(obj, list):
        for v in obj:
            convert_paths_to_cwl_files(v)
    return