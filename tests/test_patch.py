from pathlib import Path

import yaml

from koopmans_cwl.ase_operations import ase_operations
from koopmans_cwl.patch import create_workflow
from koopmans_cwl.utils import populate_listings


def test_pw_base():
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

def test_pw_error_recovery():
    with open(Path(__file__).parent / "pw" / "si.yml", "r") as f:
        inputs = yaml.safe_load(f)
    populate_listings(inputs)

    # Make a dumb wrapper of ase_operations['pw_base'] that will return an error if ecutwfc is too low
    def pw_base(**kwargs):
        ecutwfc = kwargs['parameters']['system']['ecutwfc']
        if ecutwfc < 55.0:
            return 1
        else:
            return ase_operations['pw_base'](**kwargs)

    # Create the workflow object
    wf = create_workflow(
        str(Path(__file__).parent / "pw" / "pw.cwl"), operations={'pw_base': pw_base}
    )

    # Update the runtime context
    wf.factory.runtime_context.rm_tmpdir = False
    wf.factory.runtime_context.tmpdir_prefix = (
        str(Path(__file__).parent / wf.factory.runtime_context.tmpdir_prefix.lstrip("/")) + "/"
    )

    # Run the workflow
    outputs = wf(**inputs)
    raise ValueError()
    assert outputs['error_code'] == 0
