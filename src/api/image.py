from fastapi import File, UploadFile
import uuid
from src.core.model import SuccessModel


def main(app):
    @app.post("/image/tmp")
    async def create_temporary_image(image: UploadFile = File(...)):
        #
        bucket_name = app.config["IMAGE_STORE_CONFIG"]["bucket"]
        host = app.config["IMAGE_STORE_CONFIG"]["host"]
        prefix = str(uuid.uuid4())[:8]
        #
        object = app.s3.Object(bucket_name, f"tmp/{prefix}-{image.filename}")
        object.put(Body=image.file)
        #
        return {"url": f"{host}/{object.key}"}

    @app.post("/image/refresh")
    def refresh_temporary_images():
        #
        bucket_name = app.config["IMAGE_STORE_CONFIG"]["bucket"]
        bucket = app.s3.Bucket(bucket_name)
        bucket.objects.filter(Prefix="tmp/").delete()
        #
        return SuccessModel()
