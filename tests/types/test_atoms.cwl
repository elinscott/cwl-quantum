# A dummy workflow to check that the atoms class works as intended

cwlVersion: v1.2
class: Workflow

inputs:
   atoms:
      type: { $import: "../../types/atoms.yml" }

outputs: {}

steps: {}
