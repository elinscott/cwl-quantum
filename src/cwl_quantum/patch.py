import threading
from pathlib import Path
from typing import Any, Callable, Dict, List, MutableMapping, MutableSequence, Optional, Union, cast

from cwltool.builder import Builder
from cwltool.context import LoadingContext, RuntimeContext
from cwltool.cwlprov.provenance_profile import ProvenanceProfile
from cwltool.factory import Factory
from cwltool.process import Process
from cwltool.utils import (
    CWLObjectType,
    CWLOutputType,
    DirectoryType,
    JobsGeneratorType,
    OutputCallbackType,
    normalizeFilesDirs,
)
from cwltool.workflow import default_make_tool
from ruamel.yaml.comments import CommentedMap

from .utils import chdir, convert_cwls_to_paths, convert_paths_to_cwls


class PythonJob:
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

    def run(
        self, runtimeContext: RuntimeContext, tmpdir_lock: Optional[threading.Lock] = None
    ) -> None:
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
        job = PythonJob(
            builder, self.tool["operation"], output_callbacks, self.requirements, self.hints
        )

        job.prov_obj = runtimeContext.prov_obj
        yield job


def construct_make_tool(operations):
    def custom_make_tool(toolpath_object: CommentedMap, loading_context: LoadingContext) -> Process:

        if toolpath_object["class"] == "Operation":
            tool = ImplementedOperation(toolpath_object, loading_context)

            name = Path(tool.metadata["id"][7:]).stem
            if name in operations:
                # For the moment, it is up to the user to ensure that the provided operation matches the format of the required operation
                func = operations[name]
                expected_return_names = [o["id"].rsplit("#")[-1] for o in tool.tool["outputs"]]

                # Replacing tool with the matching python function
                def wrapped_func(**kwargs) -> CWLOutputType:
                    # Recursively replace CWL File/Directory objects with Path objects
                    inputs = convert_cwls_to_paths(kwargs)

                    # Run the function
                    outputs = func(**inputs)

                    # Check that we received the expected outputs
                    if not isinstance(outputs, dict):
                        raise ValueError(
                            f"Operation {name} should return a dictionary. Please modify your implementation of this operation."
                        )
                    if set(expected_return_names) != set(outputs.keys()):
                        raise ValueError(
                            f"Operation {name} is expected to return ({', '.join(expected_return_names)}) but instead it returned ({', '.join(outputs.keys())})"
                        )

                    # Recursively replace Path objects with CWL File/Directory objects
                    tidied_outputs = convert_paths_to_cwls(outputs)

                    return tidied_outputs

                tool.tool["operation"] = wrapped_func
                tool.tool["class"] = "CustomOperation"
            else:
                raise ValueError(
                    f"Operation {name} not found; in order to run this workflow you need to provide an implementation of this operation"
                )
        else:
            tool = default_make_tool(toolpath_object, loading_context)
        return tool

    return custom_make_tool


def create_workflow(cwl_file, operations: Optional[Dict[str, Callable]] = None):
    # Create a loading context that will patch all the Operations with the provided functions in operations
    loading_context = LoadingContext()
    loading_context.construct_tool_object = construct_make_tool(operations or {})

    fac = Factory(loading_context=loading_context)

    # Create the workflow object
    wf = fac.make(cwl_file)

    return wf
