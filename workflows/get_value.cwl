# Extract the value corresponding to the key in a given record
cwlVersion: v1.2
class: ExpressionTool

requirements:
   InlineJavascriptRequirement: {}

inputs:
   record:
      type: Any
      doc: The record containing the key-value pair

   key:
      type: string
      doc: The key to be updated within the record

outputs:
   value:
      type: Any
      doc: The updated value for the specified key

expression: |
   ${ return {"value": inputs.record[inputs.key]} }
