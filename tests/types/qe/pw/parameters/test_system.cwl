# A dummy workflow to check that the qe_parameters_system class works as intended

cwlVersion: v1.2
class: Workflow

inputs:
   system:
      type: { $import: "../../../../../types/qe/pw/parameters/system.yml" }

outputs: {}

steps: {}
