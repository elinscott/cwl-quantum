from ase import Atoms
from ase.cell import Cell
from ase.calculators.espresso import Espresso

def pw_base(atoms, parameters, pseudopotentials) -> int:
   # Construct an ASE Atoms object
   symbols = [at['symbol'] for at in atoms['positions']]
   cell = Cell.fromcellpar([atoms['cell'][k] for k in ['a', 'b', 'c', 'alpha', 'beta', 'gamma']])
   ase_atoms = Atoms(symbols, cell=cell)

   # Add the positions
   positions = [at['position'] for at in atoms['positions']]
   ase_atoms.set_scaled_positions(positions)

   # Construct the calculator
   params = {k: v for subdct in parameters.values() for k, v in subdct.items()}
   params['pseudo_dir'] = pseudopotentials['directory']['path']
   params['pseudopotentials'] = {entry['symbol']: entry['filename'] for entry in pseudopotentials['filenames']}
   ase_atoms.calc = Espresso(atoms=ase_atoms, **params)

   # Perform the calculation
   err = 0
   try:
      ase_atoms.calc.calculate()
   except:
      err = 1

   return err

ase_operations = {"pw_base": pw_base}