from pathlib import Path

import yaml

from cwl_quantum.ase_operations import ase_operations
from cwl_quantum.patch import create_workflow
from cwl_quantum.utils import populate_listings


def main():
    # Create the workflow object
    wf = create_workflow("workflows/pw/pw.cwl", operations=ase_operations)

    # Update the runtime context
    wf.factory.runtime_context.rm_tmpdir = False
    wf.factory.runtime_context.tmpdir_prefix = 'tmp/'

    # Load the workflow inputs from file
    with open("ozone.yml", "r") as f:
        inputs = yaml.safe_load(f)
    populate_listings(inputs)

    # Run the workflow
    outputs = wf(**inputs)

if __name__ == '__main__':
    main()
