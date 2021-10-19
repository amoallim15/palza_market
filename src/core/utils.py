import yaml
import os
from pathlib import Path


def get_config():
    env = os.getenv("ENV", "DEV")
    with open(f"src/config/{env}.yaml", "r") as stream:
        config = yaml.safe_load(stream)
        return config


def store_image(app, tmp_path, perm_path, name):
    host = app.config["IMAGE_STORE_CONFIG"]["host"]
    bucket_name = app.config["IMAGE_STORE_CONFIG"]["bucket"]
    #
    file = Path(tmp_path)
    key = f"{bucket_name}/tmp/{file.name}"
    new_key = f"{perm_path}/{name}{file.suffix}"
    #
    app.s3.Object(bucket_name, new_key).copy_from(CopySource=key)
    return f"{host}/{new_key}"
