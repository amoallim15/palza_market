from fastapi import Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from src.core.model import ListModel  # , SuccessModel
from src.core.enums import UserRole

from src.models.sms import SMSModel


def main(app):
    @app.get("/sms", response_model=ListModel)
    async def sms_messages(
        page: int = Query(0, ge=0), current_user=Depends(app.current_user)
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        page_size = app.config["APP"]["page_size"]
        #
        cursor = app.db["sms"].find().skip(page * page_size).limit(page_size)
        count = await app.db["sms"].count_documents({})
        data_list = []
        #
        async for sms in cursor:
            data_list.append(SMSModel(**sms))
        #
        return ListModel(page=page, count=count, data=data_list)
        # TODO:
        pass

    @app.get("/sms/{sms_id}", response_model=SMSModel)
    async def get_sms(sms_id: str, current_user=Depends(app.current_user)):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        data = await app.db["sms"].find_one({"_id": sms_id})
        if data is None:
            raise HTTPException(status_code=404, detail="SMS not found.")
        #
        return SMSModel(**data)

    @app.post("/sms", response_model=SMSModel)
    async def send_sms(
        sms: SMSModel = Body(...), current_user=Depends(app.current_user)
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        # TODO: run the sms script..
        sms = jsonable_encoder(sms)
        result = await app.db["sms"].insert_one(sms)
        data = await app.db["sms"].find_one({"_id": result.inserted_id})
        if data is None:
            raise HTTPException(status_code=404, detail="SMS not found.")
        #
        return SMSModel(**data)
