cwlVersion: v1.2
class: Workflow

inputs:
   atoms:
      type: { $import: "../../types/atoms.yml" }
   parameters:
      type: { $import: "../../types/qe_parameters.yml" }
   pseudopotentials:
      type:
         type: array
         items: { $import: "../../types/pseudopotentials.yml" }

requirements:
   SubworkflowFeatureRequirement: {}
   InlineJavascriptRequirement: {}

outputs:
   error_code:
      type: int
      outputSource: pw/error_code
   parameters_out:
      type: { $import: "../../types/qe_parameters.yml" }
      outputSource: update_parameters_based_on_error/parameters_out

steps:
   pw:
      run: pw_base.cwl
      in: 
         atoms: atoms
         parameters: parameters
         pseudopotentials: pseudopotentials
         error_code: error_code_input
      out: [error_code]
   update_parameters_based_on_error:
      when: $(inputs.error_code > 0)
      run:
         class: ExpressionTool
         inputs:
            error_code: int
            ecutwfc_in: int
         outputs:
            ecutwfc_out: int
         expression: >
            ${return {'ecutwfc_out': inputs.ecutwfc_in + 10};}
      in:
         error_code: pw/error_code
         ecutwfc_in: ecutwfc
      out: [ecutwfc_out]
