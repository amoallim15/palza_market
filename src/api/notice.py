from fastapi import Body
from src.models.notice import (
    CreateNoticeModel,
    UpdateNoticeModel,
)


def main(app):
    @app.get("/notice")
    def notices():
        # TODO:
        pass

    @app.get("/notice/{notice_id}")
    def get_notice(notice_id: str):
        # TODO:
        pass

    @app.post("/notice")
    def create_notice(notice: CreateNoticeModel = Body(...)):
        # TODO:
        pass

    @app.put("/notice/{notice_id}")
    def update_notice(notice_id: str, notice: UpdateNoticeModel = Body(...)):
        # TODO:
        pass

    @app.delete("/notice/{notice_id}")
    def delete_notice(notice_id: str):
        # TODO:
        pass
