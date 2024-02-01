# This workflow implements the error recovery logic for a pw.x Quantum ESPRESSO calculation
# It wraps pw_base.cwl, which must be separately implemented.

cwlVersion: v1.2
class: Workflow

$namespaces:
  cwltool: "http://commonwl.org/cwltool#"

inputs:
   atoms:
      type: { $import: "../../types/atoms.yml" }
   parameters:
      type: { $import: "../../types/qe/pw/parameters.yml" }
   pseudopotentials:
      type: { $import: "../../types/pseudopotentials.yml" }
   first_attempt: # do not provide this input explicitly; it enables the error recovery loop to function as desired
      type: boolean
      default: true
   prior_error_code: # do not provide this input explicitly; it enables the error recovery loop to function as desired
      type: int
      default: 0

requirements:
   InlineJavascriptRequirement: {}
   SubworkflowFeatureRequirement: {}

outputs:
   error_code:
      type: int
      outputSource: pw_attempts/error_code
   updated_parameters:
      type: { $import: "../../types/qe/pw/parameters.yml" }
      outputSource: pw_attempts/updated_parameters
   xml:
      type: File
      outputSource: pw_attempts/xml
   wavefunctions:
      type:
         type: array
         items: File
      outputSource: pw_attempts/wavefunctions
   charge_density:
      type: File
      outputSource: pw_attempts/charge_density

steps:
   pw_attempts:
      # Repeatedly attempt the pw_attempt step until it succeeds
      requirements:
         cwltool:Loop:
            loopWhen: $(inputs.first_attempt || inputs.prior_error_code != 0)
            loop:
               parameters: updated_parameters
               first_attempt: first_attempt
               prior_error_code: error_code
            outputMethod: last

      in: 
         atoms: atoms
         parameters: parameters
         pseudopotentials: pseudopotentials
         first_attempt: first_attempt
         prior_error_code: prior_error_code

      out: [error_code, updated_parameters, first_attempt, xml, wavefunctions, charge_density]

      run:
         class: Workflow
         inputs:
            atoms:
               type: { $import: "../../types/atoms.yml" }
            parameters:
               type: { $import: "../../types/qe/pw/parameters.yml" }
            pseudopotentials:
               type: { $import: "../../types/pseudopotentials.yml" }
            first_attempt: boolean
            prior_error_code: int
         outputs:
            error_code:
               type: int
               outputSource: pw_attempt/error_code
            updated_parameters:
               type: { $import: "../../types/qe/pw/parameters.yml" }
               outputSource: update_parameters_as_required/parameters_out
            first_attempt:
               type: boolean
               outputSource: update_parameters_as_required/first_attempt
            xml:
               type: File
               outputSource: pw_attempt/xml
            wavefunctions:
               type:
                  type: array
                  items: File
               outputSource: pw_attempt/wavefunctions
            charge_density:
               type: File
               outputSource: pw_attempt/charge_density
         steps:
            update_parameters_as_required:
               # Update the QE parameters, based on the prior error code. Note that for the first attempt,
               # the prior error code is 0, so the parameters are not altered.
               # This should probably be reimplemented using update_record.cwl
               run:
                  class: ExpressionTool
                  inputs:
                     error_code: int
                     parameters_in:
                        type: { $import: "../../types/qe/pw/parameters.yml" }
                  outputs:
                     parameters_out:
                        type: { $import: "../../types/qe/pw/parameters.yml" }
                     first_attempt: boolean
                  expression: |
                     ${
                        var parameters_out = {};
                        // Copy the contents of parameters_in to parameters_out
                        for (var namelist in inputs.parameters_in) {
                              parameters_out[namelist] = {};
                              for (var keyword in inputs.parameters_in[namelist]) {
                                 parameters_out[namelist][keyword] = inputs.parameters_in[namelist][keyword];
                              }
                           }
                        // Dummy error recovery logic
                        if (inputs.error_code != 0) {
                           parameters_out["system"]["ecutwfc"] += 10.0;
                        } else {
                        }
                        return {"parameters_out": parameters_out, "first_attempt": false}
                     }
               in:
                  error_code: prior_error_code
                  parameters_in: parameters
               out: [parameters_out, first_attempt]
            pw_attempt:
               # Run pw.x using the updated parameters
               run: pw_base.cwl
               in: 
                  atoms: atoms
                  parameters: update_parameters_as_required/parameters_out
                  pseudopotentials: pseudopotentials
               out: [error_code, xml, wavefunctions, charge_density]