cwlVersion: v1.2
class: Operation

inputs:
   parameters:
      type: { $import: "../../types/qe/kcw/wann2kcw_parameters.yml" }
   wavefunctions:
      type:
         type: array
         items: File

outputs:
   error_code:
      type: int
