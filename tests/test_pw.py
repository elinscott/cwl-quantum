from pathlib import Path

import yaml

from cwl_quantum.ase_operations import ase_operations
from cwl_quantum.patch import create_workflow
from cwl_quantum.utils import populate_listings


def test_pw_base():
    # Create the workflow object
    wf = create_workflow("workflows/pw/pw_base.cwl", operations=ase_operations)

    # Update the runtime context
    wf.factory.runtime_context.rm_tmpdir = False
    wf.factory.runtime_context.tmpdir_prefix = (
        str(Path(__file__).parent / wf.factory.runtime_context.tmpdir_prefix.lstrip("/")) + "/"
    )

    # Load the workflow inputs from file
    with open("examples/silicon_with_pw/si.yml", "r") as f:
        inputs = yaml.safe_load(f)
    inputs["pseudopotentials"]["directory"] = {"class": "Directory", "path": "examples/pseudos"}
    populate_listings(inputs)

    # Run the workflow
    outputs = wf(**inputs)
    assert outputs["error_code"] == 0


def test_pw_error_recovery():
    # Make a dumb wrapper of ase_operations['pw_base'] that will return an error if ecutwfc is too low
    def pw_base(**kwargs):
        ecutwfc = kwargs["parameters"]["system"]["ecutwfc"]
        if ecutwfc < 55.0:
            return {"error_code": 1, "xml": None, "wavefunctions": None, "charge_density": None}
        else:
            return ase_operations["pw_base"](**kwargs)

    # Create the workflow object
    wf = create_workflow("workflows/pw/pw.cwl", operations={"pw_base": pw_base})

    # Update the runtime context
    wf.factory.runtime_context.rm_tmpdir = False
    wf.factory.runtime_context.tmpdir_prefix = (
        str(Path(__file__).parent / wf.factory.runtime_context.tmpdir_prefix.lstrip("/")) + "/"
    )

    # Load the workflow inputs from file
    with open("examples/silicon_with_pw/si.yml", "r") as f:
        inputs = yaml.safe_load(f)
    inputs["pseudopotentials"]["directory"] = {"class": "Directory", "path": "examples/pseudos"}
    populate_listings(inputs)

    # Run the workflow
    outputs = wf(**inputs)

    # Check the outputs
    assert outputs["error_code"] == 0
    assert outputs["updated_parameters"]["system"]["ecutwfc"] > 55.0
