cwlVersion: v1.2
class: Workflow

$namespaces:
  cwltool: "http://commonwl.org/cwltool#"

inputs:
   atoms:
      type: { $import: "../../types/atoms.yml" }
   pseudopotentials:
      type:
         type: array
         items: { $import: "../../types/pseudopotentials.yml" }
   qe:
      type: { $import: "../../types/qe_parameters.yml" }

requirements:
   InlineJavascriptRequirement: {}
   SubworkflowFeatureRequirement: {}

outputs:
   error_code:
      type: int
      outputSource: pw_with_error_recovery/error_code

steps:
   pw_with_error_recovery:
      run: pw_error_recovery.cwl
      in: 
         atoms: atoms
         pseudo_directory: pseudo_directory
         ecutwfc: ecutwfc
         error_code_input: error_code_input
      out: [error_code, ecutwfc_out]
      requirements:
         cwltool:Loop:
            loopWhen: $(inputs.error_code_input > 0)
            loop:
               error_code_input: error_code
               ecutwfc: ecutwfc_out
            outputMethod: last
