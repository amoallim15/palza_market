import yaml
import os


def get_config():
    env = os.getenv("ENV", "DEV")
    with open(f"src/config/{env}.yaml", "r") as stream:
        config = yaml.safe_load(stream)
        return config
