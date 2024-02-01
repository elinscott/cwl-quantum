from pathlib import Path
from typing import Any, Dict, List

from ase import Atoms
from ase.calculators.calculator import CalculationFailed
from ase.calculators.espresso import Espresso, Wann2KC
from ase.cell import Cell
from cwltool.loghandler import _logger as logger


def pw_base(
    atoms: Dict[str, Dict[str, Any]],
    parameters: Dict[str, Dict[str, Any]],
    pseudopotentials: Dict[str, Any],
) -> int:
    # Construct an ASE Atoms object
    assert isinstance(atoms["positions"], list)
    symbols = [at["symbol"] for at in atoms["positions"]]
    cell = Cell.fromcellpar([atoms["cell"][k] for k in ["a", "b", "c", "alpha", "beta", "gamma"]])
    ase_atoms = Atoms(symbols, cell=cell)

    # Add the positions
    positions = [at["position"] for at in atoms["positions"]]
    ase_atoms.set_scaled_positions(positions)

    # Construct the calculator
    params = {k: v for subdct in parameters.values() for k, v in subdct.items()}
    params["pseudo_dir"] = pseudopotentials["directory"]
    params["pseudopotentials"] = {
        entry["symbol"]: entry["filename"] for entry in pseudopotentials["filenames"]
    }
    ase_atoms.calc = Espresso(atoms=ase_atoms, **params)

    # Perform the calculation
    err = 0
    try:
        ase_atoms.calc.calculate()
    except CalculationFailed:
        err = 1

    if err:
        logger.error("Calculation failed")
    else:
        logger.info("Calculation succeeded")

    outdir = Path(ase_atoms.calc.parameters["outdir"])
    xml = outdir / (ase_atoms.calc.parameters["prefix"] + ".xml")
    wavefunctions = [
        w for w in (outdir / (ase_atoms.calc.parameters["prefix"] + ".save")).glob("wfc*.dat")
    ]
    charge_density = outdir / (ase_atoms.calc.parameters["prefix"] + ".save/charge-density.dat")

    return {
        "error_code": err,
        "xml": xml,
        "wavefunctions": wavefunctions,
        "charge_density": charge_density,
    }


def kcw_wann2kcw_base(parameters: Dict[str, Dict[str, Any]], wavefunctions: List[str]):
    # Construct a dummy atoms object
    atoms = Atoms()

    # Construct the calculator
    parameters = {k: v for subdct in parameters.values() for k, v in subdct.items()}
    atoms.calc = Wann2KC(atoms=atoms, **parameters)

    import ipdb
    ipdb.set_trace()

    # Run the calculator
    atoms.calc.calculate()

    # Extract the results
    return {"error_code": 0}


ase_operations = {"pw_base": pw_base, "kcw_wann2kcw_base": kcw_wann2kcw_base}
