from pathlib import Path

import yaml

from cwl_quantum.ase_operations import ase_operations
from cwl_quantum.patch import create_workflow
from cwl_quantum.utils import populate_listings


def run():
    # Create the workflow object
    wf = create_workflow("kcw.cwl", operations=ase_operations)

    # Update the runtime context
    wf.factory.runtime_context.rm_tmpdir = False
    wf.factory.runtime_context.tmpdir_prefix = (
        str(Path(__file__).parent / wf.factory.runtime_context.tmpdir_prefix.lstrip("/")) + "/"
    )

    # Make sure the tmpdir exists
    Path(wf.factory.runtime_context.tmpdir_prefix).mkdir(parents=True, exist_ok=True)

    # Load the workflow inputs from file
    with open("ozone.yml", "r") as f:
        inputs = yaml.safe_load(f)
    populate_listings(inputs)

    # Run the workflow
    outputs = wf(**inputs)
    print(outputs)


if __name__ == "__main__":
    run()
