from pathlib import Path
from koopmans_cwl.workflow import Workflow

def pw_base(structure: Path, pseudo_directory: Path, ecutwfc: int, error_code: int) -> int:
    return 0

def test_from_cwl():
    wf = Workflow.from_cwl(str(Path(__file__).parent / 'pw' / 'pw_error_recovery.cwl'), operations={'pw_base': pw_base})
    wf.run()
