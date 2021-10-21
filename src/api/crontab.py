from fastapi import Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from src.core.model import ListModel  # , SuccessModel
from src.core.enums import UserRole

from src.models.crontab import (
    CrontabModel,
    UpdateCrontabModel,
)


def main(app):
    @app.get("/crontab", response_model=ListModel)
    async def crontabs(page: int = Query(0, ge=0)):
        page_size = app.config["APP"]["page_size"]
        #
        cursor = app.db["crontabs"].find().skip(page * page_size).limit(page_size)
        count = await app.db["crontabs"].count_documents({})
        data_list = []
        #
        async for crontab in cursor:
            data_list.append(CrontabModel(**crontab))
        #
        return ListModel(page=page, count=count, data=data_list)

    @app.get("/crontab/{crontab_id}", response_model=CrontabModel)
    async def get_crontab(crontab_id: str):
        data = await app.db["crontabs"].find_one({"_id": crontab_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Crontab not found.")
        #
        return CrontabModel(**data)

    @app.post("/crontab", response_model=CrontabModel)
    async def create_crontab(
        crontab: CrontabModel = Body(...), current_user=Depends(app.current_user)
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        # TODO: run the crontab script..
        crontab = jsonable_encoder(crontab)
        result = await app.db["crontabs"].insert_one(crontab)
        data = await app.db["crontabs"].find_one({"_id": result.inserted_id})
        #
        if data is None:
            raise HTTPException(status_code=404, detail="Crontab not found.")
        #
        return CrontabModel(**data)

    @app.put("/crontab/{crontab_id}", response_model=CrontabModel)
    async def patch_crontab(crontab_id: str, crontab: UpdateCrontabModel = Body(...)):
        crontab = jsonable_encoder(crontab)
        await app.db["crontabs"].update_one({"_id": crontab_id}, {"$set": crontab})
        data = await app.db["crontabs"].find_one({"_id": crontab_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Crontab not found.")
        #
        return CrontabModel(**data)

    # @app.delete("/crontab/{crontab_id}", response_model=SuccessModel)
    # async def delete_crontab(
    #     crontab_id: str,
    #     current_user=Depends(app.current_user),
    # ):
    #     if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
    #         raise HTTPException(status_code=403, detail="Not allowed.")
    #     #
    #     result = await app.db["crontabs"].delete_one({"_id": crontab_id})
    #     if result.deleted_count == 1:
    #         return SuccessModel()
    #     #
    #     raise HTTPException(status_code=404, detail="Crontab not found.")
