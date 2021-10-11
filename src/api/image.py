from fastapi import Body
from src.models.image import CreateImageModel


def main(app):
    @app.post("/image/temporary")
    def create_temporary_image(image: CreateImageModel = Body(...)):
        # TODO:
        pass

    @app.get("/image/refresh")
    def refresh_temporary_images():
        # TODO:
        pass
