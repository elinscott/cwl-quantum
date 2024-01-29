from pathlib import Path

import yaml

from koopmans_cwl.ase_operations import ase_operations
from koopmans_cwl.patch import create_workflow
from koopmans_cwl.utils import populate_listings


def test_create_workflow():
    with open(Path(__file__).parent / "pw" / "si.yml", "r") as f:
        inputs = yaml.safe_load(f)
    populate_listings(inputs)

    # Create the workflow object
    wf = create_workflow(
        str(Path(__file__).parent / "pw" / "pw_base.cwl"), operations=ase_operations
    )

    # Update the runtime context
    wf.factory.runtime_context.rm_tmpdir = False
    wf.factory.runtime_context.tmpdir_prefix = (
        str(Path(__file__).parent / wf.factory.runtime_context.tmpdir_prefix.lstrip("/")) + "/"
    )

    # Run the workflow
    err = wf(**inputs)
    assert err == 0
