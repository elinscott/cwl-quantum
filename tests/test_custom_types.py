from cwltool.factory import Factory
import yaml
import pytest
from pathlib import Path

@pytest.mark.parametrize("test_input", Path("tests/custom_types").glob("input_*.yml"))
def test_custom_class(test_input):
    # Read the inputs from a YAML file
    with open(test_input) as f:
        inputs = yaml.safe_load(f)

    # Create a workflow
    factory = Factory()
    test_cwl = test_input.parent / (test_input.stem.replace("input_", "test_") + '.cwl')
    wf = factory.make(str(test_cwl))

    wf(**inputs)
