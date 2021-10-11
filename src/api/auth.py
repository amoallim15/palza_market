from src.models.api_models import User
from uuid import UUID


def main(app):
    @app.get("/user")
    def users():
        # TODO:
        pass

    @app.post("/user")
    def create_user():
        # TODO:
        pass

    @app.put("/user/{user_id}")
    def update_user(user_id: UUID, user: User):
        # TODO:
        pass

    @app.patch("/user/{user_id}")
    def patch_user(user_id: UUID, user: User):
        # TODO:
        pass

    @app.post("/auth")
    def authenticate_user():
        # TODO:
        pass
