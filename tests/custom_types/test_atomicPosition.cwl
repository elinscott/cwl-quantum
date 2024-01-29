# A dummy workflow to check that the cell class works as intended

cwlVersion: v1.2
class: Workflow

inputs:
   atomic_position:
      type: { $import: "../../types/atomicPosition.yml" }

outputs: {}

steps: {}
