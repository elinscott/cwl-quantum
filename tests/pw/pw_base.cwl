cwlVersion: v1.2
class: Operation

inputs:
   atoms:
      type: { $import: "../../types/atoms.yml" }
   parameters:
      type: { $import: "../../types/qe_parameters.yml" }
   pseudopotentials:
      type: { $import: "../../types/pseudopotentials.yml" }

outputs:
   error_code:
      type: int
