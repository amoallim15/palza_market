from fastapi import Body, Depends, HTTPException
from src.models.user import AuthenticateUserModel, ChangePasswordUserModel, UserModel


def main(app):
    #
    @app.get("/auth")
    async def info(current_user=Depends(app.current_user)):
        return current_user

    @app.post("/auth")
    async def authenticate(user_form: AuthenticateUserModel = Body(...)):
        data = await app.db["users"].find_one({"username": user_form.username})
        if data is None:
            raise HTTPException(status_code=401, detail="Incorrect username.")
        if not app.secret.verify(user_form.password, data["password"]):
            raise HTTPException(status_code=401, detail="Incorrect password.")
        #
        token = app.secret.token({"sub": data["_id"]})
        #
        return {"access_token": token, "token_type": "bearer"}

    @app.patch("/auth/{user_id}")
    async def change_password(
        user_id: str,
        current_user=Depends(app.current_user),
        user_form: ChangePasswordUserModel = Body(...),
    ):
        current_user_tmp = await app.db["users"].find_one({"_id": user_id})
        #
        if not app.secret.verify(user_form.password, current_user_tmp["password"]):
            raise HTTPException(status_code=400, detail="Incorrect password.")
        if user_form.new_password != user_form.confirm_new_password:
            raise HTTPException(status_code=400, detail="Password does not match.")
        #
        password = app.secret.hash(user_form.new_password)
        #
        await app.db["users"].update_one(
            {"_id": user_id}, {"$set": {"password": password}}
        )
        data = await app.db["users"].find_one({"_id": user_id})
        #
        return UserModel(**data)
