from fastapi import Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from src.core.enums import UserType, UserRole, UserMethod
from src.core.model import ListModel
from src.core.utils import store_image

from src.models.user import (
    UserModel,
    CreateUserModel,
    UpdateUserModel,
    PatchUserModel,
)


def main(app):
    #
    @app.get("/user", response_model=ListModel)
    async def users(current_user=Depends(app.current_user), page: int = Query(0, ge=0)):
        page_size = app.config["APP"]["page_size"]
        #
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        cursor = app.db["users"].find().skip(page * page_size).limit(page_size)
        data_list = []
        #
        async for user in cursor:
            data_list.append(UserModel(**user))
        #
        return ListModel(page=page, count=len(data_list), data=data_list)

    @app.get("/user/{user_id}", response_model=UserModel)
    async def get_user(user_id: str, current_user=Depends(app.current_user)):
        data = await app.db["users"].find_one({"_id": user_id})
        if data is None:
            return HTTPException(status_code=404, detail="user not found.")
        #
        return UserModel(**data)

    @app.post("/user", response_model=UserModel)
    async def create_user(user: CreateUserModel = Body(...)):
        if not user.personal_info_use_consent or not user.terms_and_conditions_consent:
            raise HTTPException(status_code=400, detail="Consent not given.")
        #
        duplicate_email = await app.db["users"].find_one({"email": user.email})
        if duplicate_email:
            raise HTTPException(status_code=400, detail="Duplicated email.")
        #
        if user.user_type == UserType.AGENCY and (
            not user.business_name
            or not user.business_representative
            or not user.brokerage_record_no
            or not user.legal_address
            or not user.business_registeration_no
            or not user.business_license_url
            or not user.brokerage_card_url
        ):
            raise HTTPException(
                status_code=400, detail="Agency required information is missing."
            )
        #
        if user.user_method == UserMethod.EMAIL:
            if not user.password or user.confirm_password:
                raise HTTPException(
                    status_code=400, detail="EMAIL sign up requires password."
                )
            if user.password != user.confirm_password:
                raise HTTPException(status_code=400, detail="Password does not match.")
            #
            user.password = app.secret.hash(user.password)
        #
        duplicate_username = await app.db["users"].find_one({"username": user.username})
        if duplicate_username:
            raise HTTPException(status_code=400, detail="Duplicated username.")
        #
        if user.user_type == UserType.AGENCY:
            user.business_license_url = store_image(
                app=app,
                tmp_path=user.business_license_url,
                perm_path=f"users/{user.id}",
                name="business_license",
            )
            user.brokerage_card_url = store_image(
                app=app,
                tmp_path=user.brokerage_card_url,
                perm_path=f"users/{user.id}",
                name="brokerage_card",
            )
        #
        user = jsonable_encoder(user)
        #
        user["display_name"] = user["username"]
        user["user_role"] = UserRole.CLIENT
        user["is_approved"] = False
        #
        del user["confirm_password"]
        del user["personal_info_use_consent"]
        del user["terms_and_conditions_consent"]
        #
        result = await app.db["users"].insert_one(user)
        data = await app.db["users"].find_one({"_id": result.inserted_id})
        #
        return UserModel(**data)

    @app.patch("/user/{user_id}")
    async def patch_user(
        user_id: str,
        user: PatchUserModel = Body(...),
        current_user=Depends(app.current_user),
    ):

        if user_id != current_user.id and current_user.user_role not in [
            UserRole.ADMIN,
            UserRole.EMPLOYEE,
        ]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        user = jsonable_encoder(user)
        await app.db["users"].update_one({"_id": user_id}, {"$set": user})
        data = await app.db["users"].find_one({"_id": user_id})
        #
        return UserModel(**data)

    @app.put("/user/{user_id}")
    async def update_user(
        user_id: str,
        user: UpdateUserModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if user_id != current_user.id and current_user.user_role not in [
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
        #
        return UserModel(**data)
