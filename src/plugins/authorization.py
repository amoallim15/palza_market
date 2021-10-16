from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.models.user import UserModel


def main(app, authentication_url):
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=authentication_url)
    err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    def current_user_id(token: str = Depends(oauth2_scheme)):
        payload = app.secret.payload(token)
        if not payload:
            raise err
        user_id = payload.get("sub")
        return user_id

    async def current_user(user_id: str = Depends(current_user_id)):
        user = await app.db["users"].find_one({"_id": user_id})
        if not user:
            raise err
        return UserModel(**user)

    #
    app.current_user_id = current_user_id
    app.current_user = current_user
