from koopmans.workflows import Workflow
from cwltool.load_tool import load_tool

class CWLWorkflow(Workflow):
   @classmethod
   def from_cwl(cls, cwl_file):
      cwl = load_tool(cwl_file)
      raise NotImplementedError()