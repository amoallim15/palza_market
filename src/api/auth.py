from fastapi import Body
from src.models.user import (
    CreateUserModel,
    UpdateUserModel,
    ControlUserStateModel,
    AuthenticateUserModel,
)


def main(app):
    @app.get("/user")
    def users():
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
    def control_user_state(user_id: str, user: ControlUserStateModel = Body(...)):
        # TODO:
        pass

    @app.post("/auth")
    def authenticate_user(user: AuthenticateUserModel = Body(...)):
        # TODO:
        pass
