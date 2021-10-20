import yaml
import os
from pathlib import Path
import uuid


def get_config():
    env = os.getenv("ENV", "DEV")
    with open(f"src/config/{env}.yaml", "r") as stream:
        config = yaml.safe_load(stream)
        return config


def update_image(app, old_path, new_path, name):
    host = app.config["IMAGE_STORE_CONFIG"]["host"]
    bucket_name = app.config["IMAGE_STORE_CONFIG"]["bucket"]
    #
    file = Path(old_path)
    old_key = f"{bucket_name}/" + "/".join(file.parts[2:])
    new_key = f"{new_path}/{name}{file.suffix}"
    #
    app.s3.Object(bucket_name, new_key).copy_from(CopySource=old_key)
    #
    return f"{host}/{new_key}"


def short_uuid():
    return str(uuid.uuid4())[:8]
