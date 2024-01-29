from cwltool.load_tool import fetch_document, resolve_and_validate_document
from pathlib import Path
from dataclasses import dataclass
import inspect
from typing import Any, Callable, Dict, Tuple
from cwltool.factory import Factory
from cwltool.workflow import Workflow as cwlWorkflow
from cwltool.command_line_tool import AbstractOperation as cwlOperation, ExpressionTool as cwlExpressionTool
from cwl_utils.expression import do_eval

@dataclass
class Workflow:
   version: str
   inputs: list
   run: Callable
   nodes: Dict[str, None]

   @classmethod
   def from_workflowobj(cls, workflowobj, operations={}):

      version = workflowobj['cwlVersion']
      inputs = workflowobj['inputs']
      class_name = workflowobj['class']
      if class_name != 'Workflow':
         raise ValueError(f'This is a {class_name}, not a Workflow')
      
      steps = []
      for step in workflowobj['steps']:

         run = step.get('run', None)
         if run is not None:
            if isinstance(run, str) and run.startswith('file://') and Path(run[7:]).exists():
               _, subworkflowobj, _ = fetch_document(run[7:])
            else:
               subworkflowobj = run
            step.update(**subworkflowobj)

         if step['class'] == 'Workflow':
            steps.append(CWLWorkflow.from_workflowobj(run).run)
         elif step['class'] == 'Operation':
            try:
               name = Path(step['run']).stem
            except:
               raise ValueError()
            if name in operations:
               # Ensure that the provided operation matches the format of the required operation
               func = operations[name]
               func_info = inspect.getfullargspec(func)
               expected_args = [k for k in step['inputs']]

               # Checking the argument names
               if func_info.args != expected_args:
                  raise ValueError(f'{name} has inputs {func_info.args} but the workflow requires an operation with inputs [{", ".join(expected_args)}]')
               
               # Checking the argument types
               for arg in func_info.args:
                  expected_type_name = step['inputs'][arg]['type']
                  if expected_type_name in ['File', 'Directory']:
                     expected_type_name = 'Path'
                  provided_type = func_info.annotations[arg].__name__
                  if provided_type != expected_type_name:
                     raise ValueError(f'{name} has input {arg} of type {provided_type}, but it should be of type {expected_type_name}')
                  if arg not in step['inputs']:
                     raise ValueError(f'Operation {name} has input {arg} but the workflow does not provide it')
                  
               # Checking the return types
               expected_return_types = [v['type'] for v in step['outputs'].values()]
               provided_return_type = inspect.signature(func).return_annotation
               if provided_return_type == Tuple:
                  provided_return_types = [v.__name__ for v in provided_return_type.__args__]
               else:
                  provided_return_types = [provided_return_type.__name__]
               if provided_return_types != expected_return_types:
                  raise ValueError(f'{name} returns {provided_return_types} but it should return {expected_return_types}')
               
               # Storing the function
               raise ValueError()
               steps.append([func, expected_args])
            else:
               raise ValueError(f'Operation {name} not found; in order to run this workflow you need to provide an implementation of this operation')


      def run():
         for step in steps:
            step()
   
      return cls(version=version, inputs=inputs, run=run)
   
   @classmethod
   def from_cwlworkflow(cls, cwl_workflow: cwlWorkflow, operations: dict[str, Callable]):

      steps = []      
      for step in cwl_workflow.t.steps:
         if isinstance(step.embedded_tool, cwlOperation):
            name = Path(step.tool['run'][7:]).stem
            if name in operations:
               # Ensure that the provided operation matches the format of the required operation
               func = operations[name]
               func_info = inspect.getfullargspec(func)
               expected_args = [i['id'].rsplit('/')[-1] for i in step.tool['inputs']]

               # Checking the argument names
               if set(func_info.args) != set(expected_args):
                  raise ValueError(f'{name} has inputs {func_info.args} but the workflow requires an operation with inputs [{", ".join(expected_args)}]')
               
               # Checking the argument types
               for arg_dict in step.tool['inputs']:
                  _, arg_name = arg_dict['id'].rsplit('/', 1)
                  expected_type_name = arg_dict['type']
                  if expected_type_name in ['File', 'Directory']:
                     expected_type_name = 'Path'
                  provided_type = func_info.annotations[arg_name].__name__
                  if provided_type != expected_type_name:
                     raise ValueError(f'{name} has input {arg_name} of type {provided_type}, but it should be of type {expected_type_name}')
                  
               # Checking the return types
               expected_return_types = [o['type'] for o in step.tool['outputs']]
               provided_return_type = inspect.signature(func).return_annotation
               if provided_return_type == Tuple:
                  provided_return_types = [v.__name__ for v in provided_return_type.__args__]
               else:
                  provided_return_types = [provided_return_type.__name__]
               if provided_return_types != expected_return_types:
                  raise ValueError(f'{name} returns {provided_return_types} but it should return {expected_return_types}')
               
               # Storing the function
               raise ValueError()
               steps.append([func, expected_args])
            else:
               raise ValueError(f'Operation {name} not found; in order to run this workflow you need to provide an implementation of this operation')
         # elif isinstance(step.embedded_tool, cwlWorkflow):
         #    raise NotImplementedError()
         # elif isinstance(step.embedded_tool, cwlExpressionTool):
         #    raise ValueError()
         # else:
         #    raise NotImplementedError()
         
         # def _run():
         #    pass
         
         # if 'when' in step.tool:
         #    condition = step.tool['when']
         #    def run():
         #       if condition:
         #          _run()
         # else:
         #    run = _run
            


   @classmethod
   def from_cwl(cls, cwl_file, operations):
      fac = Factory()
      wf = fac.make(cwl_file)
      make_tool = construct_make_tool(operations)
      loading_context = LoadingContext(construct_tool_object = make_tool)
      return cls.from_cwlworkflow(wf, operations)


      raise ValueError()

      return cls.from_workflowobj(workflowobj, operations)

            
