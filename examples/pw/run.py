from pathlib import Path

import yaml

from cwl_quantum.ase_operations import ase_operations
from cwl_quantum.patch import create_workflow
from cwl_quantum.utils import populate_listings


def run():
    # Create the workflow object
    wf = create_workflow("../../workflows/pw/pw.cwl", operations=ase_operations)

    # Update the runtime context
    wf.factory.runtime_context.rm_tmpdir = False
    tmpdir_prefix = Path('tmp')
    tmpdir_prefix.mkdir(exist_ok=True)
    wf.factory.runtime_context.tmpdir_prefix = str(tmpdir_prefix) + '/'

    # Load the workflow inputs from file
    with open("si.yml", "r") as f:
        inputs = yaml.safe_load(f)
    populate_listings(inputs)

    # Run the workflow
    outputs = wf(**inputs)
    print(outputs)

if __name__ == '__main__':
    run()
