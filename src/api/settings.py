from fastapi import Body, status, Response, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from src.models.settings import SettingsModel
from src.core.enums import UserRole
from src.core.model import SuccessModel


def main(app):
    @app.get("/settings", response_model=SettingsModel)
    async def get_settings(response: Response):
        #
        data = await app.db["settings"].find_one()
        #
        if data is None:
            # initialize:
            default_data = jsonable_encoder(SettingsModel(**app.config["SETTINGS"]))
            await app.db["settings"].insert_one(default_data)
            response.status_code = status.HTTP_201_CREATED
        #
        data = await app.db["settings"].find_one()
        return SettingsModel(**data)

    @app.post("/settings/refresh", response_model=SuccessModel)
    async def reset_settings(current_user=Depends(app.current_user)):
        if current_user.user_role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        data = await app.db["settings"].find_one()
        #
        if data is not None:
            result = await app.db["settings"].delete_one({"_id": data["_id"]})
            if result.deleted_count == 1:
                return SuccessModel()
        #
        raise HTTPException(status_code=404, detail="Settings not found.")

    @app.put("/settings", response_model=SettingsModel)
    async def update_settings(
        settings: SettingsModel = Body(...), current_user=Depends(app.current_user)
    ):
        if current_user.user_role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        settings = jsonable_encoder(settings)
        await app.db["settings"].update_one({}, {"$set": settings})
        data = await app.db["settings"].find_one()
        if data is None:
            raise HTTPException(status_code=404, detail="Settings not found.")
        #
        return SettingsModel(**data)
