from fastapi import Body
from src.models.homepage import CreateHomePageSectionModel, UpdateHomePageSectionModel


def main(app):
    @app.get("/home_page")
    def sections():
        # TODO:
        pass

    @app.get("/home_page/{section_id}")
    def get_section(section_id: str):
        # TODO:
        pass

    @app.post("/home_page")
    def create_section(section: CreateHomePageSectionModel = Body(...)):
        # TODO:
        pass

    @app.put("/home_page/{section_id}")
    def update_section(
        section_id: str, section: UpdateHomePageSectionModel = Body(...)
    ):
        # TODO:
        pass

    @app.delete("/home_page/{section_id}")
    def delete_section(section_id: str):
        # TODO:
        pass
