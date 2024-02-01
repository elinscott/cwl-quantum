# Duplicate an arbitrary CWL record, setting 'key' to 'value'
cwlVersion: v1.2
class: ExpressionTool

requirements:
   InlineJavascriptRequirement: {}

inputs:
   original_record:
      type: Any
      doc: The original record

   key:
      type: string
      doc: The key to be updated within the record

   value:
      type: Any
      doc: The updated value for the specified key

outputs:
   updated_record:
      type: Any
      doc: The updated record

expression: |
   ${function updateNestedDictionary(dictionary, key, value) {
      for (let currentKey in dictionary) {
         if (typeof dictionary[currentKey] === 'object' && dictionary[currentKey] !== null) {
            // If the current value is an object (nested dictionary), recursively call the function
            dictionary[currentKey] = updateNestedDictionary(dictionary[currentKey], key, value);
         } else if (currentKey === key) {
            // If the current key matches the specified key, update its value
            dictionary[currentKey] = value;
         }
      }
      return dictionary;
      };
   return {"updated_record": updateNestedDictionary(inputs.original_record, inputs.key, inputs.value)}}
