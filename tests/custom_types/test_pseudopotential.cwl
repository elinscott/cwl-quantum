# A dummy workflow to check that the cell class works as intended

cwlVersion: v1.2
class: Workflow

inputs:
   pseudo:
      type: { $import: "../../types/pseudopotential.yml" }

outputs: {}

steps: {}
