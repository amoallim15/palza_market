from fastapi import Body


def main(app):
    @app.post("/callback/kakao")
    def kakao_callback(body=Body(...)):
        # TODO:
        pass

    @app.post("/callback/naver")
    def naver_callback(body=Body(...)):
        # TODO:
        pass

    @app.post("/callback/google")
    def google_callback(body=Body(...)):
        # TODO:
        pass
