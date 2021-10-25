from fastapi import Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from src.core.model import ListModel  # , SuccessModel
from src.core.enums import UserRole
from src.core.utils import (
    get_gabia_sms_access_token,
    send_gabia_sms,
    get_gabia_sms_count,
)

from src.models.sms import SMSModel, SMSCountModel, SMSSendModel


def main(app):
    @app.get("/sms", response_model=ListModel)
    async def sms_messages(
        page: int = Query(0, ge=0),
        current_user=Depends(app.current_user),
        page_size: int = 10,
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        pipeline = [
            {"$sort": {"_id": -1}},
            {
                "$facet": {
                    "data": [{"$skip": page * page_size}, {"$limit": page_size}],
                    "info": [
                        {"$count": "count"},
                        {"$addFields": {"page": page}},
                        {"$addFields": {"page_size": page_size}},
                    ],
                }
            },
            {"$unwind": "$info"},
        ]
        #
        try:
            result = await app.db["sms"].aggregate(pipeline).next()
        except StopAsyncIteration:
            result = {"info": {"count": 0, "page": page, "page_size": page_size}}
        return ListModel(**result)

    @app.get("/sms/count", response_model=SMSCountModel)
    async def sms_count(current_user=Depends(app.current_user)):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        SMS_ID = app.config["SETTINGS"]["gabia_sms_id"]
        API_KEY = app.config["SETTINGS"]["gabia_key"]
        auth = f"{SMS_ID}:{API_KEY}".encode("utf-8")
        access_token = get_gabia_sms_access_token(auth)
        #
        if not access_token:
            raise HTTPException(status_code=500, detail="Gabia API access_token error.")
        #
        secret = f"{SMS_ID}:{access_token}".encode("utf-8")
        count = get_gabia_sms_count(secret)
        if not count:
            raise HTTPException(status_code=500, detail="Gabia API get count error.")
        #
        return SMSCountModel(count=count)

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
        sms: SMSSendModel = Body(...), current_user=Depends(app.current_user)
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        SMS_ID = app.config["SETTINGS"]["gabia_sms_id"]
        API_KEY = app.config["SETTINGS"]["gabia_sms_key"]
        CALLBACK_NUMBER = app.config["SETTINGS"]["gabia_sms_callback_number"]
        #
        auth = f"{SMS_ID}:{API_KEY}".encode("utf-8")
        access_token = get_gabia_sms_access_token(auth)
        #
        if not access_token:
            raise HTTPException(status_code=500, detail="Gabia API access_token error.")
        #
        secret = f"{SMS_ID}:{access_token}".encode("utf-8")
        sending_result = send_gabia_sms(
            secret=secret, callback_number=CALLBACK_NUMBER, model=sms
        )
        #
        if not sending_result:
            raise HTTPException(status_code=500, detail="Gabia API send sms error.")
        #
        sms = jsonable_encoder(sms)
        result = await app.db["sms"].insert_one(sms)
        data = await app.db["sms"].find_one({"_id": result.inserted_id})
        if data is None:
            raise HTTPException(status_code=404, detail="SMS not found.")
        #
        return SMSModel(**data)
