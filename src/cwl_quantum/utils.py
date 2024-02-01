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

def _convert_cwl_dict_to_path(dct):
    """Convert any CWL File/Directory objects in a nested dictionary to Path objects."""
    if not isinstance(dct, dict):
        return dct

    if dct.get("class", None) in ["File", "Directory"]:
            return Path(dct["path"])

    for key, value in dct.items():
        dct[key] = convert_cwls_to_paths(value)

    return dct    

def convert_cwls_to_paths(item):
    """Convert any CWL File/Directory objects in a nested dictionary/list to Path objects."""
    if isinstance(item, dict):
        return _convert_cwl_dict_to_path(item)
    elif isinstance(item, list):
        return [convert_cwls_to_paths(sub_item) for sub_item in item]
    else:
        return item

def _convert_path_to_cwl_dict(path: Path) -> dict:
    """Convert a Path object to a CWL File/Directory object."""
    if path.is_dir():
        cwl_dct = {"class": "Directory", "path": str(path)}
    else:
        cwl_dct = {"class": "File", "path": str(path)}
    populate_listings(cwl_dct)
    return cwl_dct

def convert_paths_to_cwls(obj: Any):
    """Convert any Path objects to CWL File/Directory objects recursively."""
    if isinstance(obj, Path):
        return _convert_path_to_cwl_dict(obj)
    
    elif isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = convert_paths_to_cwls(v)
        return obj
    
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            obj[i] = convert_paths_to_cwls(v)
        return obj
    
    else:
        return obj