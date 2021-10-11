from fastapi import File, UploadFile


def main(app):
    @app.post("/image/temporary")
    def create_temporary_image(image: UploadFile = File(...)):
        # TODO:
        pass

    @app.get("/image/refresh")
    def refresh_temporary_images():
        # TODO:
        pass
