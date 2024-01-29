# A dummy workflow to check that the qe_parameters_control class works as intended

cwlVersion: v1.2
class: Workflow

inputs:
   control:
      type: { $import: "../../types/qe_parameters_control.yml" }

outputs: {}

steps: {}
