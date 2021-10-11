from src.models.api_models import HomePageSection
from uuid import UUID


def main(app):
    @app.get("/home_page")
    def sections():
        # TODO:
        pass

    @app.post("/home_page")
    def create_section():
        # TODO:
        pass

    @app.put("/home_page/{section_id}")
    def update_section(section_id: UUID, section: HomePageSection):
        # TODO:
        pass

    @app.delete("/home_page/{section_id}")
    def delete_section(section_id: UUID, section: HomePageSection):
        # TODO:
        pass
