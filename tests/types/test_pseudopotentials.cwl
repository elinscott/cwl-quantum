# A dummy workflow to check that the pseudopotentials class works as intended

cwlVersion: v1.2
class: Workflow

inputs:
   pseudos:
      type: { $import: "../../types/pseudopotentials.yml" }

outputs: {}

steps: {}
