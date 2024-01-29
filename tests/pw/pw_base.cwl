cwlVersion: v1.2
class: Operation

inputs:
   atoms:
      type: { $import: "../../types/atoms.yml" }
   pseudopotentials:
      type: { $import: "../../types/pseudopotentials.yml" }
   ecutwfc:
      type: int
   error_code:
      type: int

outputs:
   error_code:
      type: int