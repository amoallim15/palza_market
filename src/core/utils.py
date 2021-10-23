import yaml
import os
from pathlib import Path
import uuid
import base64
import requests
from urllib.parse import urlencode


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


def get_gabia_sms_access_token(secret):
    req = {
        "url": "https://sms.gabia.com/oauth/token",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f'Basic {base64.b64encode(secret).decode("utf-8")}',
        },
        "data": urlencode({"grant_type": "client_credentials"}),
        "allow_redirects": False,
    }
    res = requests.post(**req)
    #
    if res.status_code != 200:
        return None
    json = res.json()
    #
    return json["access_token"]


def send_gabia_sms(secret, callback_number, model):
    req = {
        "url": "https://sms.gabia.com/api/send/sms",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f'Basic {base64.b64encode(secret).decode("utf-8")}',
        },
        "data": urlencode(
            {
                "refkey": model.id,
                "callback": callback_number,
                "phone": model.reciever_phone_no,
                "message": model.content,
            }
        ),
        "allow_redirects": False,
    }
    res = requests.post(**req)
    #
    if res.status_code != 200:
        return False
    #
    return True


def get_gabia_sms_count(secret):
    req = {
        "url": "https://sms.gabia.com/api/user/info",
        "headers": {
            "Authorization": f'Basic {base64.b64encode(secret).decode("utf-8")}'
        },
        "allow_redirects": False,
    }
    res = requests.get(**req)
    #
    if res.status_code != 200:
        return None
    json = res.json()
    if "data" not in json:
        return None
    #
    return json["data"]["sms_count"]
