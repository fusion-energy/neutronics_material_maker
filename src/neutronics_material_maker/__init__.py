try:
    from importlib.metadata import version, PackageNotFoundError
except (ModuleNotFoundError, ImportError):
    from importlib_metadata import version, PackageNotFoundError
try:
    __version__ = version("neutronics_material_maker")
except PackageNotFoundError:
    from setuptools_scm import get_version

    __version__ = get_version(root="..", relative_to=__file__)

__all__ = ["__version__"]

from .utils import make_fispact_material
from .utils import make_serpent_material
from .utils import make_mcnp_material
from .utils import make_shift_material
from .utils import AddMaterialFromDir
from .utils import AddMaterialFromFile
from .utils import AvailableMaterials
from .utils import material_dict
from .utils import isotope_to_zaid
from .utils import zaid_to_isotope
from .utils import check_add_additional_end_lines
from .utils import NATURAL_ABUNDANCE
from .utils import SaveMaterialsToFile

from .material import Material
