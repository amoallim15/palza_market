from fastapi import File, UploadFile, status
from fastapi.responses import JSONResponse
import uuid


def main(app):
    @app.post("/image/temporary")
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
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
