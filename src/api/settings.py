from fastapi import Body
from src.models.settings import (
    UpdateSettingsModel,
)


def main(app):
    @app.get("/settings")
    def get_settings():
        # TODO:
        pass

    @app.post("/settings")
    def reset_settings():
        # TODO:
        pass

    @app.put("/settings")
    def update_config(settings: UpdateSettingsModel = Body(...)):
        # TODO:
        pass
