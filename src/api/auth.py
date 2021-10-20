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

    @app.patch("/auth")
    async def change_password(
        current_user=Depends(app.current_user),
        user_form: ChangePasswordUserModel = Body(...),
    ):
        if not app.secret.verify(user_form.password, current_user.password):
            raise HTTPException(status_code=400, details="Incorrect password.")
        if user_form.new_password != user_form.confirm_new_password:
            raise HTTPException(status_code=400, details="Password does not match.")
        #
        password = app.secret.hash(user_form.new_password)
        #
        await app.db["users"].update_one(
            {"_id": current_user.id}, {"$set": {"password": password}}
        )
        data = await app.db["users"].find_one({"_id": current_user.id})
        #
        return UserModel(**data)
