cwlVersion: v1.2
class: Workflow

inputs:
   atoms:
      type: { $import: "../../types/atoms.yml" }
   pseudopotentials:
      type: { $import: "../../types/pseudopotentials.yml" }
   ecutwfc:
      type: int
      default: 30
   error_code_input:
      type: int
      default: 0

requirements:
   SubworkflowFeatureRequirement: {}
   InlineJavascriptRequirement: {}

outputs:
   error_code:
      type: int
      outputSource: pw/error_code
   ecutwfc_out:
      type: int
      outputSource: update_parameters_based_on_error/ecutwfc_out

steps:
   pw:
      run: pw_base.cwl
      in: 
         atoms: atoms
         pseudopotentials: pseudopotentials
         ecutwfc: ecutwfc
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
