from fastapi import Body
from src.models.sms import CreateSMSModel


def main(app):
    @app.get("/sms")
    def sms():
        # TODO:
        pass

    @app.post("/sms")
    def send_sms(user: CreateSMSModel = Body(...)):
        # TODO:
        pass
