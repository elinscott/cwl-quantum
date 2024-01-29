# A dummy workflow to check that the cell class works as intended

cwlVersion: v1.2
class: Workflow

inputs:
   cell:
      type: { $import: "../../types/cell.yml" }

outputs: {}

steps: {}
