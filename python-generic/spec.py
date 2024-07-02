import json

# Define the JSON structure as a dictionary
json_data = {
    "type": "SPEC",
    "spec": {
        "title": "Python Custom Script",
        "type": "object",
        "properties": {
            "script": {
                "type": "code",
                "language": "python",
                "defaultValue": """
                    def run():
                        print('STARTING SCRIPT')
                        with open(data_file_path, 'w') as f:
                            f.write('good, not good')
                        return {
                          'status': 'ok',
                          'file': './data.csv',
                          'columns': [
                            {'name': 'column_one_name', 'type': 'VARCHAR'},
                            {'name': 'column_two_name', 'type': 'BOOLEAN'}
                          ]
                        }
                """
            }
        }
    }
}

# Convert the dictionary to a JSON string
json_string = json.dumps(json_data)

# Print the JSON string
print(json_string)