from fastapi import Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from src.core.model import ListModel, SuccessModel
from src.core.enums import UserType

from src.models.realstate import (
    RealstateModel,
    CreateRealstateModel,
    UpdateRealstateModel,
)


def main(app):
    @app.get("/realstate", response_model=ListModel)
    async def realstates(page: int = Query(0, ge=0), page_size: int = 10):
        pipeline = [
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user",
                },
            },
            {"$unwind": "$user"},
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
            result = await app.db["realstates"].aggregate(pipeline).next()
        except StopAsyncIteration:
            result = {"info": {"count": 0, "page": page, "page_size": page_size}}
        return ListModel(**result)

    @app.get("/realstate/{realstate}", response_model=RealstateModel)
    async def get_realstate(realstate_id: str):
        data = await app.db["realstates"].find_one({"_id": realstate_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Realstate not found.")
        #
        return RealstateModel(**data)

    @app.post("/realstate", response_model=RealstateModel)
    async def create_realstate(
        agency_id: str,
        realstate: CreateRealstateModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_type != UserType.AGENCY:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        realstate = jsonable_encoder(realstate)
        #
        realstate["user_id"] = str(current_user.id)
        #
        result = await app.db["realstates"].insert_one(realstate)
        data = await app.db["realstates"].find_one({"_id": result.inserted_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Realstate not found.")
        #
        return RealstateModel(**data)

    @app.put("/realstate/{realstate_id}", response_model=RealstateModel)
    async def update_realstate(
        realstate_id: str,
        realstate: UpdateRealstateModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_type != UserType.AGENCY:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        data = await app.db["realstates"].find_one({"_id": realstate_id})
        if not data:
            raise HTTPException(status_code=404, detail="Realstate not found.")
        if data["user_id"] != str(current_user.id):
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        realstate = jsonable_encoder(realstate)
        await app.db["realstates"].update_one(
            {"_id": realstate_id}, {"$set": realstate}
        )
        data = await app.db["realstates"].find_one({"_id": realstate_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Realstate not found.")
        #
        return RealstateModel(**data)

    @app.delete("/realstate/{realstate_id}", response_model=SuccessModel)
    async def delete_realstate(
        realstate_id: str,
        current_user=Depends(app.current_user),
    ):
        if current_user.user_type != UserType.AGENCY:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        data = await app.db["realstates"].find_one({"_id": realstate_id})
        if not data:
            raise HTTPException(status_code=404, detail="Realstate not found.")
        if data["user_id"] != str(current_user.id):
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        result = await app.db["realstates"].delete_one({"_id": realstate_id})
        if result.deleted_count == 1:
            return SuccessModel()
        #
        raise HTTPException(status_code=404, detail="Realstate not found.")
