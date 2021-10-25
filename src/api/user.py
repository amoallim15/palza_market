from fastapi import Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from src.core.enums import UserType, UserRole, UserMethod
from src.core.model import ListModel
from src.core.utils import update_image, short_uuid

from src.models.user import (
    UserModel,
    CreateUserModel,
    UpdateUserModel,
    PatchUserModel,
)


def main(app):
    #
    @app.get("/user", response_model=ListModel)
    async def users(
        current_user=Depends(app.current_user),
        page: int = Query(0, ge=0),
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
            result = await app.db["users"].aggregate(pipeline).next()
        except StopAsyncIteration:
            result = {"info": {"count": 0, "page": page, "page_size": page_size}}
        return ListModel(**result)

    @app.get("/user/{user_id}", response_model=UserModel)
    async def get_user(user_id: str, current_user=Depends(app.current_user)):
        data = await app.db["users"].find_one({"_id": user_id})
        if data is None:
            raise HTTPException(status_code=404, detail="User not found.")
        #
        return UserModel(**data)

    @app.post("/user", response_model=UserModel)
    async def create_user(user: CreateUserModel = Body(...)):
        print(user, type(user))
        duplicate_email = await app.db["users"].find_one({"email": user.email})
        if duplicate_email:
            raise HTTPException(status_code=400, detail="Duplicated email.")
        #
        duplicate_username = await app.db["users"].find_one({"username": user.username})
        if duplicate_username:
            raise HTTPException(status_code=400, detail="Duplicated username.")
        #
        if user.user_method == UserMethod.EMAIL:
            user.password = app.secret.hash(user.password)
        #
        if user.user_type == UserType.AGENCY:
            user.business_license_url = update_image(
                app=app,
                old_path=user.business_license_url,
                new_path=f"users/{user.id}",
                name=f"{short_uuid()}-business_license",
            )
            user.brokerage_card_url = update_image(
                app=app,
                old_path=user.brokerage_card_url,
                new_path=f"users/{user.id}",
                name=f"{short_uuid()}-brokerage_card",
            )
        #
        user = jsonable_encoder(user)
        #
        del user["confirm_password"]
        #
        result = await app.db["users"].insert_one(user)
        data = await app.db["users"].find_one({"_id": result.inserted_id})
        if data is None:
            raise HTTPException(status_code=404, detail="User not found.")
        #
        return UserModel(**data)

    @app.patch("/user/{user_id}")
    async def patch_user(
        user_id: str,
        user: PatchUserModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        user = jsonable_encoder(user)
        await app.db["users"].update_one({"_id": user_id}, {"$set": user})
        data = await app.db["users"].find_one({"_id": user_id})
        if data is None:
            raise HTTPException(status_code=404, detail="User not found.")
        #
        return UserModel(**data)

    @app.put("/user/{user_id}")
    async def update_user(
        user_id: str,
        user: UpdateUserModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if user_id != (current_user.id) and current_user.user_role not in [
            UserRole.ADMIN,
            UserRole.EMPLOYEE,
        ]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        duplicate_email = await app.db["users"].find_one({"email": user.email})
        if duplicate_email and duplicate_email["_id"] != user_id:
            raise HTTPException(status_code=400, detail="Duplicated email.")
        #
        user = jsonable_encoder(user)
        await app.db["users"].update_one({"_id": user_id}, {"$set": user})
        data = await app.db["users"].find_one({"_id": user_id})
        if data is None:
            raise HTTPException(status_code=404, detail="User not found.")
        #
        return UserModel(**data)
