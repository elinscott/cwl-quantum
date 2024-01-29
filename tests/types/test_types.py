from pathlib import Path

import pytest
import yaml
from cwltool.factory import Factory

from koopmans_cwl.utils import populate_listings

custom_types = [t for t in Path("types").glob("*.yml")]


@pytest.mark.parametrize("custom_type", custom_types, ids=[t.stem for t in custom_types])
def test_custom_class(custom_type):
    # Find the corresponding test input
    test_input = Path(__file__).parent / f"input_{custom_type.stem}.yml"
    if not test_input.exists():
        raise NotImplementedError(f"Input .yml file for the {custom_type} custom type is missing")

    # Find the corresponding test cwl file
    test_cwl_file = Path(__file__).parent / f"test_{custom_type.stem}.cwl"
    if not test_cwl_file.exists():
        raise NotImplementedError(f".cwl file for testing the {custom_type} custom type is missing")

    # Read the inputs from a YAML file
    with open(test_input) as f:
        inputs = yaml.safe_load(f)
    populate_listings(inputs)

    # Create a workflow
    factory = Factory()
    wf = factory.make(str(test_cwl_file))

    # Run thw workflow
    wf(**inputs)
