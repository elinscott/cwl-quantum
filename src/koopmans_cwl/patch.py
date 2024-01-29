from cwltool.factory import Factory
from cwltool.builder import Builder
from cwltool.workflow import default_make_tool
from ruamel.yaml.comments import CommentedMap
from cwltool.process import Process
from cwltool.context import LoadingContext, RuntimeContext
from cwltool.utils import CWLObjectType, OutputCallbackType, JobsGeneratorType, DirectoryType, normalizeFilesDirs, CWLOutputType
from pathlib import Path
import inspect
from typing import Tuple, Optional, List, Any, cast, MutableMapping, Union, MutableSequence, Callable
import threading
from .utils import chdir

class PythonJob():
   def __init__(
      self,
      builder: Builder,
      operation: Callable,
      output_callback: Optional[OutputCallbackType],
      requirements: List[CWLObjectType],
      hints: List[CWLObjectType],
      outdir: Optional[str] = None,
      tmpdir: Optional[str] = None,
      ) -> None:

      """Initialize this PythonJob."""
      self.builder = builder
      self.operation = operation
      self.requirements = requirements
      self.hints = hints
      self.output_callback = output_callback
      self.outdir = outdir
      self.tmpdir = tmpdir
      self.prov_obj: Optional["ProvenanceProfile"] = None

   def run(self, runtimeContext: RuntimeContext,
           tmpdir_lock: Optional[threading.Lock] = None) -> None:
      """Run this PythonJob."""
      normalizeFilesDirs(self.builder.job)

      tmpdir = runtimeContext.get_tmpdir()
      with chdir(tmpdir):
         ev = self.operation(**self.builder.job)

      normalizeFilesDirs(
          cast(
              Optional[
                  Union[
                      MutableSequence[MutableMapping[str, Any]],
                      MutableMapping[str, Any],
                      DirectoryType,
                  ]
              ],
              ev,
          )
      )
      if self.output_callback:
          self.output_callback(cast(Optional[CWLObjectType], ev), "success")


class ImplementedOperation(Process):
   def job(
      self,
      job_order: CWLObjectType,
      output_callbacks: Optional[OutputCallbackType],
      runtimeContext: RuntimeContext,
   ) -> JobsGeneratorType:
      
      builder = self._init_job(job_order, runtimeContext)
      job = PythonJob(builder, self.tool['operation'],
                      output_callbacks,
                      self.requirements,
                      self.hints)
      
      job.prov_obj = runtimeContext.prov_obj
      yield job
      
      
def construct_make_tool(operations):
   def custom_make_tool(toolpath_object: CommentedMap, loading_context: LoadingContext) -> Process:

      if toolpath_object['class'] == 'Operation':
         tool = ImplementedOperation(toolpath_object, loading_context)

         name = Path(tool.metadata['id'][7:]).stem
         if name in operations:
            # # Ensure that the provided operation matches the format of the required operation
            func = operations[name]
            # func_info = inspect.getfullargspec(func)
            # expected_args = [i['id'].rsplit('#')[-1] for i in tool.tool['inputs']]

            # # Checking the argument names
            # if set(func_info.args) != set(expected_args):
            #    raise ValueError(f'{name} has inputs {func_info.args} but the workflow requires an operation with inputs [{", ".join(expected_args)}]')
            
            # # Checking the argument types
            # for arg_dict in tool.tool['inputs']:
            #    _, arg_name = arg_dict['id'].rsplit('#', 1)
            #    expected_type_name = arg_dict['type']
            #    if expected_type_name in ['File', 'Directory']:
            #       expected_type_name = 'Path'
            #    provided_type = func_info.annotations[arg_name].__name__
            #    if provided_type != expected_type_name:
            #       raise ValueError(f'{name} has input {arg_name} of type {provided_type}, but it should be of type {expected_type_name}')
            #    
            # # Checking the return types
            expected_return_names = [o['id'].rsplit('#')[-1] for o in tool.tool['outputs']]
            # expected_return_types = [o['type'] for o in tool.tool['outputs']]
            # provided_return_type = inspect.signature(func).return_annotation
            # if provided_return_type == Tuple:
            #    provided_return_types = [v.__name__ for v in provided_return_type.__args__]
            # else:
            #    provided_return_types = [provided_return_type.__name__]
            # if provided_return_types != expected_return_types:
            #    raise ValueError(f'{name} returns {provided_return_types} but it should return {expected_return_types}')
            
            # Replacing tool with the matching python function
            def wrapped_func(**kwargs) -> CWLOutputType:
               inputs = {}
               for k, v in kwargs.items():
                  if isinstance(v, MutableMapping) and v.get("class") in ["File", "Directory"]:
                     inputs[k] = Path(v["location"])
                  else:
                     inputs[k] = v
               outputs = func(**inputs)
               if not isinstance(outputs, tuple):
                  outputs = (outputs,)
               return {k: v for k, v in zip(expected_return_names, outputs)}

            tool.tool['operation'] = wrapped_func
            tool.tool['class'] = "CustomOperation"
         else:
            raise ValueError(f'Operation {name} not found; in order to run this workflow you need to provide an implementation of this operation')
      else:
         tool = default_make_tool(toolpath_object, loading_context)
      return tool
   return custom_make_tool

def create_workflow(cwl_file, operations={}):
   # Create a loading context that will patch all the Operations with the provided functions in operations
   loading_context = LoadingContext()
   loading_context.construct_tool_object = construct_make_tool(operations)

   fac = Factory(loading_context=loading_context)

   # Create the workflow object
   wf = fac.make(cwl_file)

   return wf
