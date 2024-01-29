from cwltool.factory import Factory
from cwltool.utils import get_listing
import yaml
import pytest
from pathlib import Path

def populate_listings(dct):
    keys = list(dct.keys())
    for k in keys:
        v = dct[k]
        if isinstance(v, dict):
            populate_listings(v)
        elif k == 'class' and v in ['File', 'Directory']:
            dct['contents'] = None
            dct['basename'] = Path(dct['path']).name
    return


@pytest.mark.parametrize("test_input", Path("tests/custom_types").glob("input_*.yml"))
def test_custom_class(test_input):
    # Read the inputs from a YAML file
    with open(test_input) as f:
        inputs = yaml.safe_load(f)
    populate_listings(inputs)

    # Create a workflow
    factory = Factory()
    test_cwl = test_input.parent / (test_input.stem.replace("input_", "test_") + '.cwl')
    wf = factory.make(str(test_cwl))

    wf(**inputs)
