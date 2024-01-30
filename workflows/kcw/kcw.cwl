# This workflow implements a KCW workflow
# pw_base.cwl and kcw_base.cwl must be separately implemented.

cwlVersion: v1.2
class: Workflow

$namespaces:
  cwltool: "http://commonwl.org/cwltool#"

inputs:
   atoms:
      type: { $import: "../../types/atoms.yml" }
   pw_parameters:
      type: { $import: "../../types/qe/pw/parameters.yml" }
   kcw_parameters:
      type: { $import: "../../types/qe/kcw/parameters.yml" }
   pseudopotentials:
      type: { $import: "../../types/pseudopotentials.yml" }

requirements:
   InlineJavascriptRequirement: {}
   SubworkflowFeatureRequirement: {}

outputs:
   error_code:
      type: int
      outputSource: pw_attempts/error_code

steps:
   pw:
      # Run pw.x
      run: ../pw/pw.cwl
      in: 
         atoms: atoms
         parameters: pw_parameters
         pseudopotentials: pseudopotentials
      out: [error_code, pw_parameters_updated]
   wann2kcw:
      # Run wann2kcw.x
      run: wann2kcw_base.cwl
   kcw:
      # Run kcw.x
      run: kcw_base.cwl
      in:
         atoms: atoms
         parameters: kcw_parameters
         pseudopotentials: pseudopotentials