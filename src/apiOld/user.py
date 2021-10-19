from fastapi import Body, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from src.core.enums import UserType, UserMethod, UserRole
from pathlib import Path

# from fastapi.security import OAuth2PasswordRequestForm
from src.models.user import (
    CreateUserModel,
    UpdateUserModel,
    PatchUserModel,
    AuthenticateUserModel,
    UserModel,
)


def main(app):
    #
    @app.get("/user")
    def users(current_user=Depends(app.current_user)):
        # TODO:
        pass

    @app.get("/user/{user_id}")
    def get_user(user_id: str, current_user=Depends(app.current_user)):
        # TODO:
        pass

    @app.post("/user", response_model=UserModel)
    async def create_user(user: CreateUserModel = Body(...)):
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
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Agnecy required information is missing.",
            )
        #
        if user.user_method == UserMethod.EMAIL:
            if not user.password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="EMAIL sign up requires password.",
                )
            else:
                user.password = app.secret.hash(user.password)
        #
        duplicate_username = await app.db["users"].find_one({"username": user.username})
        if duplicate_username:
            raise HTTPException(status_code=400, detail="Duplicated username.")
        #
        if user.user_type == UserType.AGENCY:
            host = app.config["IMAGE_STORE_CONFIG"]["host"]
            bucket_name = app.config["IMAGE_STORE_CONFIG"]["bucket"]
            #
            business_license_file = Path(user.business_license_url)
            brokerage_card_file = Path(user.brokerage_card_url)
            business_license_tmp_key = f"{bucket_name}/tmp/{business_license_file.name}"
            brokerage_card_tmp_key = f"{bucket_name}/tmp/{brokerage_card_file.name}"
            business_license_new_key = (
                f"users/{user.id}/business_license{business_license_file.suffix}"
            )
            brokerage_card_new_key = (
                f"users/{user.id}/brokerage_card{brokerage_card_file.suffix}"
            )
            #
            app.s3.Object(bucket_name, business_license_new_key).copy_from(
                CopySource=business_license_tmp_key
            )
            app.s3.Object(bucket_name, brokerage_card_new_key).copy_from(
                CopySource=brokerage_card_tmp_key
            )
            #
            user.business_license_url = f"{host}/{business_license_new_key}"
            user.brokerage_card_url = f"{host}/{brokerage_card_new_key}"
        #
        user = jsonable_encoder(user)
        #
        user["display_name"] = user["username"]
        user["user_role"] = UserRole.CLIENT
        user["is_approved"] = False
        #
        result = await app.db["users"].insert_one(user)
        data = await app.db["users"].find_one({"_id": result.inserted_id})
        return UserModel(**data)

    @app.put("/user/{user_id}")
    async def update_user(
        user_id: str,
        user: UpdateUserModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if user_id != current_user.id and current_user.user_role not in [
            "ADMIN",
            "EMPLOYEE",
        ]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username."
            )
        #
        user = jsonable_encoder(user)
        result = await app.db["users"].update_one({"_id": user_id}, {"$set": user})
        data = await app.db["users"].find_one({"_id": user_id})
        return UserModel(**data)
        # TODO:
        pass

    @app.patch("/user/{user_id}")
    def patch_user(
        user_id: str,
        user: PatchUserModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        # TODO:
        pass

    @app.get("/auth", response_model=UserModel)
    async def is_authenticated(current_user=Depends(app.current_user)):
        return current_user

    @app.post("/auth")
    async def authenticate_user(user_form: AuthenticateUserModel = Body(...)):
        data = await app.db["users"].find_one({"username": user_form.username})
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username."
            )
        if not app.secret.verify(user_form.password, data["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password."
            )
        #
        token = app.secret.token({"sub": data["_id"]})
        #
        return {"access_token": token, "token_type": "bearer"}
