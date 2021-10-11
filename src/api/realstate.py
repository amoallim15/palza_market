from src.models.api_models import Realstate
from uuid import UUID


def main(app):
    @app.get("/realstate")
    def realstates():
        # TODO:
        pass

    @app.post("/realstate")
    def create_realstate():
        # TODO:
        pass

    @app.put("/realstate/{realstate_id}")
    def update_realstate(realstate_id: UUID, realstate: Realstate):
        # TODO:
        pass

    @app.delete("/realstate/{realstate_id}")
    def delete_realstate(realstate_id: UUID, realstate: Realstate):
        # TODO:
        pass

    @app.patch("/like/{realstate_id}")
    def like(realstate_id: str, realstate: Realstate):
        # TODO: toggle realstate like
        pass

    @app.patch("/approve/{realstate_id}")
    def approve(realstate_id: str, realstate: Realstate):
        # TODO: approve realstate
        pass
