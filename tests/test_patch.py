from pathlib import Path
from koopmans_cwl.patch import create_workflow

global ERROR
ERROR = 3

def pw_base(structure: Path, pseudo_directory: Path, ecutwfc: int, error_code: int) -> int:
    global ERROR
    ERROR -= 1
    return ERROR

def test_create_workflow():
    psp_directory = Path('pseudos/').resolve()
    structure = Path('si.cif').resolve()
    wf_inputs = {'pseudo_directory': {'class': 'Directory', 'location': 'file://' + str(psp_directory), 'basename': psp_directory.name},
                'structure': {'class': 'File', 'location': 'file://' + str(structure), 'basename': structure.name},
                'ecutwfc': 30}
    wf = create_workflow(str(Path(__file__).parent / 'pw' / 'pw.cwl'),
                         operations={'pw_base': pw_base})
    out = wf(**wf_inputs)

    raise ValueError
