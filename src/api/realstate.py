from fastapi import Body
from src.models.realstate import (
    CreateRealstateModel,
    UpdateRealstateModel,
    PatchRealstateModel,
)


def main(app):
    @app.get("/realstate")
    def realstates():
        # TODO:
        pass

    @app.get("/realstate/{realstate_id}")
    def get_realstate(realstate_id: str):
        # TODO:
        pass

    @app.post("/realstate")
    def create_realstate(realstate: CreateRealstateModel = Body(...)):
        # TODO:
        pass

    @app.put("/realstate/{realstate_id}")
    def update_realstate(
        realstate_id: str, realstate: UpdateRealstateModel = Body(...)
    ):
        # TODO:
        pass

    @app.delete("/realstate/{realstate_id}")
    def delete_realstate(realstate_id: str):
        # TODO:
        pass

    @app.patch("/like/{realstate_id}")
    def like(realstate_id: str, realstate: PatchRealstateModel):
        # TODO: toggle realstate like
        pass

    @app.patch("/approve/{realstate_id}")
    def approve(realstate_id: str, realstate: PatchRealstateModel):
        # TODO: approve realstate
        pass
