cwlVersion: v1.2
class: Workflow

inputs:
   atoms:
      type: { $import: "../../types/atoms.yml" }
   parameters:
      type: { $import: "../../types/qe_parameters.yml" }
   pseudopotentials:
      type: { $import: "../../types/pseudopotentials.yml" }
   perform_error_recovery:
      type: boolean
      default: false
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
   updated_parameters:
      type: { $import: "../../types/qe_parameters.yml" }
      outputSource: pw/parameters

steps:
   update_parameters_based_on_error:
      when: $(inputs.perform_error_recovery && inputs.error_code_input != 0)
      run:
         class: ExpressionTool
         inputs:
            error_code: int
            parameters_in:
               type: { $import: "../../types/qe_parameters.yml" }
         outputs:
            parameters_out:
               type: { $import: "../../types/qe_parameters.yml" }
         expression: |
            ${
               var parameters_out = {};
               for (var namelist in inputs.parameters_in) {
                     parameters_out[namelist] = {};
                     for (var keyword in inputs.parameters_in[namelist]) {
                        if (keyword == "ecutwfc") {
                           parameters_out[namelist][keyword] = inputs.parameters_in[namelist][keyword] + 10.0;
                        } else {
                        parameters_out[namelist][keyword] = inputs.parameters_in[namelist][keyword];
                        }
                     }
                  }
               return {"parameters_out": parameters_out}
            }
      in:
         perform_error_recovery: perform_error_recovery
         error_code: error_code_input
         parameters_in: parameters
      out: [parameters_out]
   pw:
      run: pw_base.cwl
      in: 
         atoms: atoms
         parameters: update_parameters_based_on_error/parameters
         pseudopotentials: pseudopotentials
      out: [error_code]
