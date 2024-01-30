# A dummy workflow to check that the qe_parameters class works as intended

cwlVersion: v1.2
class: Workflow

inputs:
   qe:
      type: { $import: "../../../../types/qe/pw/parameters.yml" }

outputs: {}

steps: {}
