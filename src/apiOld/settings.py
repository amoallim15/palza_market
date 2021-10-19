from fastapi import Body, status, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.models.settings import CreateSettingsModel, UpdateSettingsModel, SettingsModel


def main(app):
    @app.get("/settings")
    async def get_settings(response: Response):
        data = await app.db["settings"].find_one()
        #
        if data is None:
            # initialize:
            default_data = jsonable_encoder(
                CreateSettingsModel(**app.config["SETTINGS"])
            )
            await app.db["settings"].insert_one(default_data)
            response.status_code = status.HTTP_201_CREATED
        #
        data = await app.db["settings"].find_one()
        return SettingsModel(**data)

    @app.post("/settings")
    async def reset_settings():
        data = await app.db["settings"].find_one()
        #
        if data is not None:
            result = await app.db["settings"].delete_one({"_id": data["_id"]})
            if result.deleted_count == 1:
                return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        #
        raise HTTPException(status_code=404, detail="Settings not found.")

    @app.put("/settings")
    async def update_settings(settings: UpdateSettingsModel = Body(...)):
        # TODO:
        settings = jsonable_encoder(settings)
        result = await app.db["settings"].update_one({}, {"$set": settings})
        # if result.modified_count == 1:
        data = await app.db["settings"].find_one()
        return SettingsModel(**data)
        # raise HTTPException(status_code=404, detail="Settings not found.")
