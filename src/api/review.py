from fastapi import Body
from src.models.review import CreateReviewModel, UpdateReviewModel


def main(app):
    @app.get("/review/{realstate_id}")
    def reviews(realstate_id: str):
        # TODO:
        pass

    @app.post("/review/{realstate_id}")
    def create_review(realstate_id: str, review: CreateReviewModel = Body(...)):
        # TODO:
        pass

    @app.put("/review/{review_id}")
    def update_review(review_id: str, review: UpdateReviewModel = Body(...)):
        # TODO:
        pass

    @app.delete("/review/{review_id}")
    def delete_review(review_id: str):
        # TODO:
        pass
