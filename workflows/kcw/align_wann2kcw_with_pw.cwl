# Workflow for aligning the settings of a kcw.x calculation (with calculation == wann2kcw) with a preceeding pw.x calculation

cwlVersion: v1.2
class: Workflow

requirements:
   StepInputExpressionRequirement: {}

inputs:
   original_kcw_parameters:
      type: { $import: "../../types/qe/kcw/parameters.yml" }
   pw_parameters:
      type: { $import: "../../types/qe/pw/parameters.yml" }
   _outdir_string:
      type: string
      default: "outdir"
outputs:
   updated_kcw_parameters:
      type: { $import: "../../types/qe/kcw/parameters.yml" }
      outputSource: set_outdir/updated_record
steps:
   set_outdir:
      run: ../set_value.cwl
      in:
         original_record: original_kcw_parameters
         key: _outdir_string
         value:
            source: pw_parameters
            valueFrom: $(self.control.outdir)
      out: [updated_record]