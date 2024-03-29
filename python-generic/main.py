import json
import traceback
import argparse
import importlib.util

parser = argparse.ArgumentParser(
    description='Process inputs')

parser.add_argument('--config', type=str, help='Path to config file')

args = parser.parse_args()


def run(config):
    #SCRIPT BODY GOES HERE
    print("HELLO WORLD")
    print(config.script)

    #create new python file

    with open('custom_script.py', 'w') as file:
        file.write(config.script)

    spec = importlib.util.spec_from_file_location("custom_script", "./custom_script.py")
    custom_script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(custom_script)
    
    # Step 3: Execute the script function and capture its output
    output = custom_script.run(config.data_file_path)
    print('DONE', json.dumps(output))


def fail(error):
    result = {
        "status": "error",
        "error": """{}
         {}""".format(str(error), traceback.format_exc())
    }

    output_json = json.dumps(result)
    print('DONE', output_json)


def load_config(file_path):
    raw_config = load_json(file_path)
    print('RAW CONFIG', raw_config)

    data_file_path = raw_config.get('dataFilePath', None)
    script = raw_config.get('config').get('script')

    return Config(data_file_path, script)


def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        True
        print(f"File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        True
        print(f"JSON decoding error: {e}")
    except Exception as e:
        True
        print(f"An error occurred: {e}")


class ConfigError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Config:
    def __init__(self, data_file_path, script):
        self.data_file_path = data_file_path
        self.script = script

    @ property
    def data_file_path(self):
        return self._data_file_path

    @ data_file_path.setter
    def data_file_path(self, value):
        if value is None:
            raise ConfigError("Missing data file path in config.")
        else:
            self._data_file_path = value

    @ property
    def script(self):
        return self._script

    @ script.setter
    def script(self, value):
        if value is None:
            raise ConfigError("Missing script in config.")
        else:
            self._script = value


# Main Program
if __name__ == "__main__":
    try:
        config = load_config(args.config)
        run(config)
    except ConfigError as e:
        fail(e)
