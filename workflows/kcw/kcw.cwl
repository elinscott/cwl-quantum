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

outputs: []
#    kcw_parameters_updated:
#       type: { $import: "../../types/qe/kcw/parameters.yml" }
#       outputSource: align_wann2kcw_with_pw/updated_kcw_parameters

steps:
   pw:
      # Run pw.x
      run: ../pw/pw.cwl
      in:
         atoms: atoms
         parameters: pw_parameters
         pseudopotentials: pseudopotentials
      out: [error_code, updated_parameters, xml, wavefunctions, charge_density]
#    align_wann2kcw_with_pw:
#       # Align wann2kcw parameters with parameters from preceeding pw calculation
#       run: align_wann2kcw_with_pw.cwl
#       in:
#          original_kcw_parameters: kcw_parameters
#          pw_parameters: pw/updated_parameters
#       out: [updated_kcw_parameters]
   wann2kcw:
      # Run kcw.x (calculation == wann2kcw)
      run: kcw_wann2kcw_base.cwl
      in:
         parameters: kcw_parameters
         wavefunctions: pw/wavefunctions
      out: [error_code]
   # kcw:
   #    # Run kcw.x
   #    run: kcw_base.cwl
   #    in:
   #       atoms: atoms
   #       parameters: kcw_parameters
   #       pseudopotentials: pseudopotentials