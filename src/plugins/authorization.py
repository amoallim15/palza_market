from fastapi.security import OAuth2PasswordBearer


def main(app, authentication_url):
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=authentication_url)
    app.token = oauth2_scheme
    pass
