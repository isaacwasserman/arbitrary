import os
from io import StringIO
from contextlib import redirect_stdout
from easy_nodes import NumberInput, ComfyNode, MaskTensor, StringInput, ImageTensor
import easy_nodes
from . import dependencies

code_placeholder = """# Arguments are accessible through the using the argument names as keys.
# (e.g. image_1, args float_2, etc.).
# Outputs should be written to the 'outputs' dictionary using the return names as keys.
# (e.g. outputs['image'], outputs['float'], etc.)."""


class ForcedNumberInput(NumberInput):
    def __new__(self, default, min_value, max_value, step=None, round=None, display="number", optional=False):
        instance = super().__new__(self, default, min_value, max_value, step, round, display, optional)
        instance.forceInput = True
        return instance

    def to_dict(self):
        metadata = super().to_dict()
        metadata["forceInput"] = True
        return metadata


@ComfyNode(
    is_output_node=True,
    color="#55FF55",
    height=600,
    width=350,
    return_types=[ImageTensor, ImageTensor, MaskTensor, MaskTensor, str, str, int, int, float, float],
    return_names=[
        "image_1",
        "image_2",
        "mask_1",
        "mask_2",
        "string_1",
        "string_2",
        "integer_1",
        "integer_2",
        "float_1",
        "float_2",
    ],
)
def python(
    image_1: ImageTensor = None,
    image_2: ImageTensor = None,
    mask_1: MaskTensor = None,
    mask_2: MaskTensor = None,
    string_1: str = StringInput("Hello World!", multiline=False, optional=True, force_input=True),
    string_2: str = StringInput("Hello World!", multiline=False, optional=True, force_input=True),
    integer_1: int = ForcedNumberInput(10, 1, 100, optional=True),
    integer_2: int = ForcedNumberInput(10, 1, 100, optional=True),
    float_1: float = ForcedNumberInput(1.0, 0, 10.0, 0.01, 0.001, optional=True),
    float_2: float = ForcedNumberInput(1.0, 0, 10.0, 0.01, 0.001, optional=True),
    requirements: str = StringInput("torch\npillow\nopencv-python\nnumpy", multiline=True),
    code: str = StringInput(code_placeholder, multiline=True),
) -> tuple[
    ImageTensor | None,
    ImageTensor | None,
    MaskTensor | None,
    MaskTensor | None,
    str | None,
    str | None,
    int | None,
    int | None,
    float | None,
    float | None,
]:
    if requirements is not None:
        requirements = [requirement.strip() for requirement in requirements.split("\n")]
        if not all([dependencies.package_installed(requirement) for requirement in requirements]):
            pip_command = f"pip install {' '.join(requirements)}"
            os.system(pip_command)

    namespace = {
        "image_1": image_1,
        "image_2": image_2,
        "mask_1": mask_1,
        "mask_2": mask_2,
        "string_1": string_1,
        "string_2": string_2,
        "integer_1": integer_1,
        "integer_2": integer_2,
        "float_1": float_1,
        "float_2": float_2,
        "outputs": {},
    }
    f = StringIO()
    with redirect_stdout(f):
        exec(code, {}, namespace)
    console_output = f.getvalue()
    easy_nodes.show_text(console_output)
    image_1_output = namespace["outputs"].get("image_1", None)
    image_2_output = namespace["outputs"].get("image_2", None)
    mask_1_output = namespace["outputs"].get("mask_1", None)
    mask_2_output = namespace["outputs"].get("mask_2", None)
    string_1_output = namespace["outputs"].get("string_1", None)
    string_2_output = namespace["outputs"].get("string_2", None)
    integer_1_output = namespace["outputs"].get("integer_1", None)
    integer_2_output = namespace["outputs"].get("integer_2", None)
    float_1_output = namespace["outputs"].get("float_1", None)
    float_2_output = namespace["outputs"].get("float_2", None)
    outputs = (
        image_1_output,
        image_2_output,
        mask_1_output,
        mask_2_output,
        string_1_output,
        string_2_output,
        integer_1_output,
        integer_2_output,
        float_1_output,
        float_2_output,
    )
    return outputs
