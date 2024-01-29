cwlVersion: v1.2
class: Workflow

$namespaces:
  cwltool: "http://commonwl.org/cwltool#"

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
      default: 1

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
