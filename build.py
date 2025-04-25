"""build module"""
#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")

# pylint: disable=invalid-name
name = "G8X.2025.TYY.GE2"
default_task = "publish"

# pylint: disable=unused-argument, unnecessary-pass
@init
def set_properties(project):
    """
    Initialize project properties for the build process
    """
    pass
