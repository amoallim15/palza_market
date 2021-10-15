from fastapi import Body, Depends

# from fastapi.security import OAuth2PasswordRequestForm
from src.models.user import (
    CreateUserModel,
    UpdateUserModel,
    PatchUserModel,
    AuthenticateUserModel,
)


def main(app):
    @app.get("/user")
    def users(token: str = Depends(app.token)):
        # TODO:
        pass

    @app.get("/user/{user_id}")
    def get_user(user_id: str):
        # TODO:
        pass

    @app.post("/user")
    def create_user(user: CreateUserModel = Body(...)):
        # TODO:
        pass

    @app.put("/user/{user_id}")
    def update_user(user_id: str, user: UpdateUserModel = Body(...)):
        # TODO:
        pass

    @app.patch("/user/{user_id}")
    def patch_user(user_id: str, user: PatchUserModel = Body(...)):
        # TODO:
        pass

    @app.post("/auth")
    def authenticate_user(user_form: AuthenticateUserModel = Depends()):
        print(user_form.username, user_form.password)
        # TODO:
        pass
