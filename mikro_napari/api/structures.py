from arkitekt.serialization.registry import get_current_structure_registry
from arkitekt.widgets import *
from .schema import *

MultiScaleSample = MultiScaleSampleFragment

structure_reg = get_current_structure_registry()
structure_reg.register_as_structure(
    MultiScaleSample,
    expand=aexpand_multiscale,
)
