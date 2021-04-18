#!/usr/bin/env python3

__author__ = "neutronics material maker development team"

import json
import warnings
from pathlib import Path
from typing import Optional

try:
    import openmc
except BaseException:
    warnings.warn(
        "OpenMC not found, .openmc_material, .serpent_material,"
        " .mcnp_material, .fispact_material .shif_materials not avaiable")

# from https://github.com/openmc-dev/openmc/blob/develop/openmc/data/data.py
# remove when pip install openmc via PyPi is available
NATURAL_ABUNDANCE = {
    'H1': 0.99984426, 'H2': 0.00015574, 'He3': 0.000002,
    'He4': 0.999998, 'Li6': 0.07589, 'Li7': 0.92411,
    'Be9': 1.0, 'B10': 0.1982, 'B11': 0.8018,
    'C12': 0.988922, 'C13': 0.011078, 'N14': 0.996337,
    'N15': 0.003663, 'O16': 0.9976206, 'O17': 0.000379,
    'O18': 0.0020004, 'F19': 1.0, 'Ne20': 0.9048,
    'Ne21': 0.0027, 'Ne22': 0.0925, 'Na23': 1.0,
    'Mg24': 0.78951, 'Mg25': 0.1002, 'Mg26': 0.11029,
    'Al27': 1.0, 'Si28': 0.9222968, 'Si29': 0.0468316,
    'Si30': 0.0308716, 'P31': 1.0, 'S32': 0.9504074,
    'S33': 0.0074869, 'S34': 0.0419599, 'S36': 0.0001458,
    'Cl35': 0.757647, 'Cl37': 0.242353, 'Ar36': 0.003336,
    'Ar38': 0.000629, 'Ar40': 0.996035, 'K39': 0.932581,
    'K40': 0.000117, 'K41': 0.067302, 'Ca40': 0.96941,
    'Ca42': 0.00647, 'Ca43': 0.00135, 'Ca44': 0.02086,
    'Ca46': 0.00004, 'Ca48': 0.00187, 'Sc45': 1.0,
    'Ti46': 0.0825, 'Ti47': 0.0744, 'Ti48': 0.7372,
    'Ti49': 0.0541, 'Ti50': 0.0518, 'V50': 0.0025,
    'V51': 0.9975, 'Cr50': 0.04345, 'Cr52': 0.83789,
    'Cr53': 0.09501, 'Cr54': 0.02365, 'Mn55': 1.0,
    'Fe54': 0.05845, 'Fe56': 0.91754, 'Fe57': 0.02119,
    'Fe58': 0.00282, 'Co59': 1.0, 'Ni58': 0.680769,
    'Ni60': 0.262231, 'Ni61': 0.011399, 'Ni62': 0.036345,
    'Ni64': 0.009256, 'Cu63': 0.6915, 'Cu65': 0.3085,
    'Zn64': 0.4917, 'Zn66': 0.2773, 'Zn67': 0.0404,
    'Zn68': 0.1845, 'Zn70': 0.0061, 'Ga69': 0.60108,
    'Ga71': 0.39892, 'Ge70': 0.2052, 'Ge72': 0.2745,
    'Ge73': 0.0776, 'Ge74': 0.3652, 'Ge76': 0.0775,
    'As75': 1.0, 'Se74': 0.0086, 'Se76': 0.0923,
    'Se77': 0.076, 'Se78': 0.2369, 'Se80': 0.498,
    'Se82': 0.0882, 'Br79': 0.50686, 'Br81': 0.49314,
    'Kr78': 0.00355, 'Kr80': 0.02286, 'Kr82': 0.11593,
    'Kr83': 0.115, 'Kr84': 0.56987, 'Kr86': 0.17279,
    'Rb85': 0.7217, 'Rb87': 0.2783, 'Sr84': 0.0056,
    'Sr86': 0.0986, 'Sr87': 0.07, 'Sr88': 0.8258,
    'Y89': 1.0, 'Zr90': 0.5145, 'Zr91': 0.1122,
    'Zr92': 0.1715, 'Zr94': 0.1738, 'Zr96': 0.028,
    'Nb93': 1.0, 'Mo92': 0.14649, 'Mo94': 0.09187,
    'Mo95': 0.15873, 'Mo96': 0.16673, 'Mo97': 0.09582,
    'Mo98': 0.24292, 'Mo100': 0.09744, 'Ru96': 0.0554,
    'Ru98': 0.0187, 'Ru99': 0.1276, 'Ru100': 0.126,
    'Ru101': 0.1706, 'Ru102': 0.3155, 'Ru104': 0.1862,
    'Rh103': 1.0, 'Pd102': 0.0102, 'Pd104': 0.1114,
    'Pd105': 0.2233, 'Pd106': 0.2733, 'Pd108': 0.2646,
    'Pd110': 0.1172, 'Ag107': 0.51839, 'Ag109': 0.48161,
    'Cd106': 0.01245, 'Cd108': 0.00888, 'Cd110': 0.1247,
    'Cd111': 0.12795, 'Cd112': 0.24109, 'Cd113': 0.12227,
    'Cd114': 0.28754, 'Cd116': 0.07512, 'In113': 0.04281,
    'In115': 0.95719, 'Sn112': 0.0097, 'Sn114': 0.0066,
    'Sn115': 0.0034, 'Sn116': 0.1454, 'Sn117': 0.0768,
    'Sn118': 0.2422, 'Sn119': 0.0859, 'Sn120': 0.3258,
    'Sn122': 0.0463, 'Sn124': 0.0579, 'Sb121': 0.5721,
    'Sb123': 0.4279, 'Te120': 0.0009, 'Te122': 0.0255,
    'Te123': 0.0089, 'Te124': 0.0474, 'Te125': 0.0707,
    'Te126': 0.1884, 'Te128': 0.3174, 'Te130': 0.3408,
    'I127': 1.0, 'Xe124': 0.00095, 'Xe126': 0.00089,
    'Xe128': 0.0191, 'Xe129': 0.26401, 'Xe130': 0.04071,
    'Xe131': 0.21232, 'Xe132': 0.26909, 'Xe134': 0.10436,
    'Xe136': 0.08857, 'Cs133': 1.0, 'Ba130': 0.0011,
    'Ba132': 0.001, 'Ba134': 0.0242, 'Ba135': 0.0659,
    'Ba136': 0.0785, 'Ba137': 0.1123, 'Ba138': 0.717,
    'La138': 0.0008881, 'La139': 0.9991119, 'Ce136': 0.00186,
    'Ce138': 0.00251, 'Ce140': 0.88449, 'Ce142': 0.11114,
    'Pr141': 1.0, 'Nd142': 0.27153, 'Nd143': 0.12173,
    'Nd144': 0.23798, 'Nd145': 0.08293, 'Nd146': 0.17189,
    'Nd148': 0.05756, 'Nd150': 0.05638, 'Sm144': 0.0308,
    'Sm147': 0.15, 'Sm148': 0.1125, 'Sm149': 0.1382,
    'Sm150': 0.0737, 'Sm152': 0.2674, 'Sm154': 0.2274,
    'Eu151': 0.4781, 'Eu153': 0.5219, 'Gd152': 0.002,
    'Gd154': 0.0218, 'Gd155': 0.148, 'Gd156': 0.2047,
    'Gd157': 0.1565, 'Gd158': 0.2484, 'Gd160': 0.2186,
    'Tb159': 1.0, 'Dy156': 0.00056, 'Dy158': 0.00095,
    'Dy160': 0.02329, 'Dy161': 0.18889, 'Dy162': 0.25475,
    'Dy163': 0.24896, 'Dy164': 0.2826, 'Ho165': 1.0,
    'Er162': 0.00139, 'Er164': 0.01601, 'Er166': 0.33503,
    'Er167': 0.22869, 'Er168': 0.26978, 'Er170': 0.1491,
    'Tm169': 1.0, 'Yb168': 0.00123, 'Yb170': 0.02982,
    'Yb171': 0.14086, 'Yb172': 0.21686, 'Yb173': 0.16103,
    'Yb174': 0.32025, 'Yb176': 0.12995, 'Lu175': 0.97401,
    'Lu176': 0.02599, 'Hf174': 0.0016, 'Hf176': 0.0526,
    'Hf177': 0.186, 'Hf178': 0.2728, 'Hf179': 0.1362,
    'Hf180': 0.3508, 'Ta180': 0.0001201, 'Ta181': 0.9998799,
    'W180': 0.0012, 'W182': 0.265, 'W183': 0.1431,
    'W184': 0.3064, 'W186': 0.2843, 'Re185': 0.374,
    'Re187': 0.626, 'Os184': 0.0002, 'Os186': 0.0159,
    'Os187': 0.0196, 'Os188': 0.1324, 'Os189': 0.1615,
    'Os190': 0.2626, 'Os192': 0.4078, 'Ir191': 0.373,
    'Ir193': 0.627, 'Pt190': 0.00012, 'Pt192': 0.00782,
    'Pt194': 0.32864, 'Pt195': 0.33775, 'Pt196': 0.25211,
    'Pt198': 0.07356, 'Au197': 1.0, 'Hg196': 0.0015,
    'Hg198': 0.1004, 'Hg199': 0.1694, 'Hg200': 0.2314,
    'Hg201': 0.1317, 'Hg202': 0.2974, 'Hg204': 0.0682,
    'Tl203': 0.29524, 'Tl205': 0.70476, 'Pb204': 0.014,
    'Pb206': 0.241, 'Pb207': 0.221, 'Pb208': 0.524,
    'Bi209': 1.0, 'Th230': 0.0002, 'Th232': 0.9998,
    'Pa231': 1.0, 'U234': 0.000054, 'U235': 0.007204,
    'U238': 0.992742
}

ATOMIC_SYMBOL = {
    0: 'n', 1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C',
    7: 'N', 8: 'O', 9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg', 13: 'Al',
    14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K',
    20: 'Ca', 21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn',
    26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zn', 31: 'Ga',
    32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br', 36: 'Kr', 37: 'Rb',
    38: 'Sr', 39: 'Y', 40: 'Zr', 41: 'Nb', 42: 'Mo', 43: 'Tc',
    44: 'Ru', 45: 'Rh', 46: 'Pd', 47: 'Ag', 48: 'Cd', 49: 'In',
    50: 'Sn', 51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs',
    56: 'Ba', 57: 'La', 58: 'Ce', 59: 'Pr', 60: 'Nd', 61: 'Pm',
    62: 'Sm', 63: 'Eu', 64: 'Gd', 65: 'Tb', 66: 'Dy', 67: 'Ho',
    68: 'Er', 69: 'Tm', 70: 'Yb', 71: 'Lu', 72: 'Hf', 73: 'Ta',
    74: 'W', 75: 'Re', 76: 'Os', 77: 'Ir', 78: 'Pt', 79: 'Au',
    80: 'Hg', 81: 'Tl', 82: 'Pb', 83: 'Bi', 84: 'Po', 85: 'At',
    86: 'Rn', 87: 'Fr', 88: 'Ra', 89: 'Ac', 90: 'Th', 91: 'Pa',
    92: 'U', 93: 'Np', 94: 'Pu', 95: 'Am', 96: 'Cm', 97: 'Bk',
    98: 'Cf', 99: 'Es', 100: 'Fm', 101: 'Md', 102: 'No',
    103: 'Lr', 104: 'Rf', 105: 'Db', 106: 'Sg', 107: 'Bh',
    108: 'Hs', 109: 'Mt', 110: 'Ds', 111: 'Rg', 112: 'Cn',
    113: 'Nh', 114: 'Fl', 115: 'Mc', 116: 'Lv', 117: 'Ts',
    118: 'Og'
}


def check_add_additional_end_lines(value):
    """Uses to check the additional lines passed to Material and Multimaterial
    classes are correctly formatted"""

    if value is not None:
        string_codes = ['mcnp', 'serpent', 'shift', 'fispact']
        if not isinstance(value, dict):
            raise ValueError(
                'Material.additional_end_lines should be a dictionary')
        for key, entries in value.items():
            if key not in string_codes:
                raise ValueError(
                    'Material.additional_end_lines should be a '
                    'dictionary where the keys are the name of the neutronics'
                    'code. Acceptable values are {}'.format(string_codes))
            if not isinstance(entries, list):
                raise ValueError(
                    'Material.additional_end_lines should be a'
                    ' dictionary where the value of each dictionary entry is a'
                    ' list')
            for entry in entries:
                if not isinstance(entry, str):
                    raise ValueError(
                        'Material.additional_end_lines should be'
                        'a dictionary where the value of each dictionary entry'
                        ' is a list of strings')
    return value


def add_additional_end_lines(code: str, mat) -> list:
    """
    Accertains if additional lines were requested by the user for the code used
    and if so returns the additional lines request as a list to be added to the
    end of the existing material card list.
    """
    print(mat.additional_end_lines)
    if mat.additional_end_lines is not None:
        if code in list(mat.additional_end_lines.keys()):
            return mat.additional_end_lines[code]
    return []


def make_fispact_material(mat) -> str:
    """
    Returns a Fispact material card for the material. This contains the required
    keywords (DENSITY and FUEL) and the number of atoms of each isotope in the
    material for the given volume. The Material.volume_in_cm3 must be set to
    use this method. See the Fispact FUEL keyword documentation for more
    information https://fispact.ukaea.uk/wiki/Keyword:FUEL
    """

    if mat.volume_in_cm3 is None:
        raise ValueError(
            "Material.volume_in_cm3 needs setting before fispact_material can be made"
        )

    mat_card = [
        "DENSITY " + str(mat.openmc_material.get_mass_density()),
        "FUEL " + str(len(mat.openmc_material.nuclides)),
    ]
    for (
        isotope,
        atoms_barn_cm,
    ) in mat.openmc_material.get_nuclide_atom_densities().values():
        atoms_cm3 = atoms_barn_cm * 1.0e24
        atoms = mat.volume_in_cm3 * atoms_cm3
        mat_card.append(isotope + " " + "{:.12E}".format(atoms))

    mat_card = mat_card + add_additional_end_lines('fispact', mat)

    return "\n".join(mat_card)


def make_serpent_material(mat) -> str:
    """Returns the material in a string compatable with Serpent II"""

    if mat.zaid_suffix is None:
        zaid_suffix = ""
    else:
        zaid_suffix = mat.zaid_suffix

    if mat.name is None:
        name = ''
    else:
        name = mat.name

    mat_card = ["mat " + name + " " +
                str(mat.openmc_material.get_mass_density())]
    if mat.temperature_to_neutronics_code is True:
        if mat.temperature is not None:
            mat_card[0] = mat_card[0] + ' tmp ' + str(mat.temperature)
        # should check if percent type is 'ao' or 'wo'

    for isotope in mat.openmc_material.nuclides:
        if isotope[2] == "ao":
            prefix = "  "
        elif isotope[2] == "wo":
            prefix = " -"
        mat_card.append(
            "      "
            + isotope_to_zaid(isotope[0])
            + zaid_suffix
            + prefix
            + f"{isotope[1]:.{mat.decimal_places}e}"
        )

    mat_card = mat_card + add_additional_end_lines('serpent', mat)

    return "\n".join(mat_card)


def make_mcnp_material(mat) -> str:
    """Returns the material in a string compatable with MCNP6"""

    if mat.material_id is None:
        raise ValueError(
            "Material.material_id needs setting before mcnp_material can be made"
        )

    if mat.zaid_suffix is None:
        zaid_suffix = ""
    else:
        zaid_suffix = mat.zaid_suffix

    if mat.name is None:
        name = ''
    else:
        name = mat.name

    mat_card = [
        "c     "
        + name
        + " density "
        + f"{mat.openmc_material.get_mass_density():.{mat.decimal_places}e}"
        + " g/cm3"
    ]
    for i, isotope in enumerate(mat.openmc_material.nuclides):

        if i == 0:
            start = f"M{mat.material_id: <5}"
        else:
            start = "      "

        if isotope[2] == "ao":
            prefix = "  "
        elif isotope[2] == "wo":
            prefix = " -"

        rest = (
            isotope_to_zaid(isotope[0])
            + zaid_suffix
            + prefix
            + f"{isotope[1]:.{mat.decimal_places}e}"
        )

        mat_card.append(start + rest)

    mat_card = mat_card + add_additional_end_lines('mcnp', mat)

    return "\n".join(mat_card)


def make_shift_material(mat) -> str:
    """Returns the material in a string compatable with Shift"""

    if mat.material_id is None:
        raise ValueError(
            "Material.material_id needs setting before shift_material can be made"
        )
    if mat.temperature is None:
        raise ValueError(
            "Material.temperature needs setting before shift_material can be made"
        )

    mat_card = [
        "[COMP][MATERIAL]\n"
        + "name %s\n" % mat.name
        + "matid %s\n" % mat.material_id
        + "tmp %s" % mat.temperature
    ]
    zaid = 'zaid'
    nd_ = 'nd'

    # shift units in atoms / barn-cm
    for nuclide, atom_dens in mat.openmc_material.get_nuclide_atom_densities().items():
        zaid += ' ' + isotope_to_zaid(nuclide)
        nd_ += ' ' + f"{atom_dens[1]:.{mat.decimal_places}e}"

    mat_card.extend([zaid, nd_])

    mat_card = mat_card + add_additional_end_lines('shift', mat)

    return "\n".join(mat_card)


def isotope_to_zaid(isotope: str) -> str:
    """converts an isotope into a zaid e.g. Li6 -> 003006"""
    z, a, m = openmc.data.zam(isotope)
    zaid = str(z).zfill(3) + str(a).zfill(3)
    return zaid


def zaid_to_isotope(zaid: str) -> str:
    """converts an isotope into a zaid e.g. 003006 -> Li6"""
    a = str(zaid)[-3:]
    z = str(zaid)[:-3]
    symbol = ATOMIC_SYMBOL[int(z)]
    return symbol + str(int(a))


def AddMaterialFromDir(directory: str, verbose: bool = True):
    """Add materials to the internal library from a directory of json files"""
    for filename in Path(directory).rglob("*.json"):
        AddMaterialFromFile(filename, verbose)


def AddMaterialFromFile(filename: str, verbose: Optional[bool] = True) -> None:
    """Add materials to the internal library from a json file"""
    with open(filename, "r") as f:
        new_data = json.load(f)
        material_dict.update(new_data)
    if verbose:
        print("Added materials to library from", filename)
        print(sorted(list(material_dict.keys())))


def AvailableMaterials() -> dict:
    """Returns a dictionary of available materials"""
    return material_dict


def SaveMaterialsToFile(filename: str, materials: list, format='json') -> str:
    """Saves a list of materials to a json file. Useful for saving as a library
    for future use.

    Arguments:
        filename: The output filename.
        materials: List of neutronics_material_maker.Materials to save.

    Returns
        str: the filename of the json file
    """

    if format == 'json':
        with open(filename, 'w') as outfile:
            json.dump({mat.name: mat.to_json()[mat.name]
                       for mat in materials}, outfile, indent=4)
        return filename

    all_materials = ''
    for mat in materials:
        if format == 'mcnp':
            all_materials += 'c\nc\nc\n' + mat.mcnp_material

        if format == 'serpent':
            all_materials += mat.serpent_material

        if format == 'shift':
            all_materials += mat.shift_material

        if format == 'fispact':
            all_materials += mat.shift_material

    with open(filename, 'w') as outfile:
        outfile.write(all_materials)

    return filename


# loads the internal material library of materials
material_dict = {}
AddMaterialFromDir(Path(__file__).parent / "data", verbose=False)
