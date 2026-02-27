import json
import traceback
import argparse
import importlib.util
from aws import get_secret

parser = argparse.ArgumentParser(
    description='Process inputs')

parser.add_argument('--config', type=str, help='Path to config file')

args = parser.parse_args()


def run(config):
    # create new python file
    with open('custom_script.py', 'w') as file:
        file.write(config.script)

    spec = importlib.util.spec_from_file_location(
        "custom_script", "./custom_script.py")
    custom_script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(custom_script)

    # Step 3: Execute the script function and capture its output
    output = custom_script.run(config)
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

    data_file_path = raw_config.get('dataFilePath', None)

    config_section = raw_config.get('config')
    if config_section is None:
        raise ConfigError("Missing 'config' section in config file.")
    script = config_section.get('script')

    env_section = raw_config.get('env')
    if env_section is None:
        raise ConfigError("Missing 'env' section in config file.")
    aws_access_key = env_section.get('aws.accessKeyId')
    aws_secret_key = env_section.get('aws.secretKey')
    aws_creds = {'aws_secret_key': aws_secret_key,
                 'aws_access_key_id': aws_access_key}
    city_alias = raw_config.get('cityAlias')
    instance_bounding_box = raw_config.get('boundingBox')

    return Config(data_file_path, script, aws_creds, city_alias, instance_bounding_box, raw_config=raw_config)


def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise ConfigError(f"Config file '{file_path}' not found.")
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in config file: {e}")
    except Exception as e:
        raise ConfigError(f"Failed to read config file: {e}")


class ConfigError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Config:
    KEYS = ['data_file_path', 'script', 'aws_creds', 'city_alias', 'instance_bounding_box']
    
    def __init__(self, data_file_path, script, aws_creds, city_alias, instance_bounding_box, raw_config=None):
        self.data_file_path = data_file_path
        self.script = script
        self.aws_creds = aws_creds
        self.city_alias = city_alias
        self.instance_bounding_box = instance_bounding_box
        self.raw_config = raw_config

    @property
    def data_file_path(self):
        return self._data_file_path

    @data_file_path.setter
    def data_file_path(self, value):
        if value is None:
            raise ConfigError("Missing data file path in config.")
        self._data_file_path = value

    @property
    def script(self):
        return self._script

    @script.setter
    def script(self, value):
        if value is None:
            raise ConfigError("Missing script in config.")
        self._script = value

    @property
    def aws_creds(self):
        return self._aws_creds

    @aws_creds.setter
    def aws_creds(self, value):
        if value is None:
            raise ConfigError("Missing aws credentials in env.")
        self._aws_creds = value

    # Dictionary-like access
    def __getitem__(self, key):
        if key in Config.KEYS:
            return getattr(self, key)
        raise KeyError(f"Key '{key}' not found.")

    def __setitem__(self, key, value):
        if key in Config.KEYS:
            setattr(self, key, value)
        else:
            raise KeyError(f"Key '{key}' not found.")



# Main Program
if __name__ == "__main__":
    try:
        config = load_config(args.config)
        run(config)
    except ConfigError as e:
        fail(e)
    except Exception as e:
        fail(e)
