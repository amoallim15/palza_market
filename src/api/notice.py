from src.models.api_models import Notice
from uuid import UUID


def main(app):
    @app.get("/notice")
    def notices():
        # TODO: get notices from the database
        pass

    @app.post("/notice")
    def create_notice():
        # TODO: post new notice
        pass

    @app.put("/notice/{notice_id}")
    def update_notice(notice_id: UUID, notice: Notice):
        # TODO: update notice
        pass

    @app.delete("/notice/{notice_id}")
    def delete_notice(notice_id: UUID, notice: Notice):
        # TODO: delete notice
        pass
