# -*- coding: utf-8 -*-

"""Test implementation of creating koopmans Workflows from cwl files."""

from .workflow import Workflow
from cwltool.utils import files
from cwltool.process import use_custom_schema

ext10 = files("cwltool").joinpath("extensions.yml").read_text("utf-8")
ext11 = files("cwltool").joinpath("extensions-v1.1.yml").read_text("utf-8")
ext12 = files("cwltool").joinpath("extensions-v1.2.yml").read_text("utf-8")
use_custom_schema("v1.0", "http://commonwl.org/cwltool", ext10)
use_custom_schema("v1.1", "http://commonwl.org/cwltool", ext11)
use_custom_schema("v1.2", "http://commonwl.org/cwltool", ext12)
use_custom_schema("v1.2.0-dev1", "http://commonwl.org/cwltool", ext11)
use_custom_schema("v1.2.0-dev2", "http://commonwl.org/cwltool", ext11)
use_custom_schema("v1.2.0-dev3", "http://commonwl.org/cwltool", ext11)
