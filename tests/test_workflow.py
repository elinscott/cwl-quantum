from koopmans_cwl import CWLWorkflow

def test_from_cwl():
    wf = CWLWorkflow.from_cwl('echo.cwl')
