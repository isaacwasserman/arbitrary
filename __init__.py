import os
from . import dependencies

with open("requirements.txt", "r") as f:
    requirements = [line for line in f.read().split("\n") if line]

if not all([dependencies.package_installed(requirement) for requirement in requirements]):
    os.system("pip install -r requirements.txt")

import easy_nodes

easy_nodes.initialize_easy_nodes(default_category="Arbitrary", auto_register=False)

# Simply importing your module gives the ComfyNode decorator a chance to register your nodes.
from .python_node import *  # noqa: F403, E402

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = easy_nodes.get_node_mappings()
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
