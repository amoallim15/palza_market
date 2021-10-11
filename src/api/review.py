from src.models.api_models import Review, Realstate
from uuid import UUID


def main(app):
    @app.get("/review/{realstate_id}")
    def reviews(realstate_id: UUID, realstate: Realstate):
        # TODO: get reviews from the database of realstate
        pass

    @app.post("/review/{realstate_id}")
    def create_review(realstate_id: UUID, realstate: Realstate):
        # TODO: post new review
        pass

    @app.put("/review/{review_id}")
    def update_review(review_id: UUID, review: Review):
        # TODO: update review
        pass

    @app.delete("/review/{review_id}")
    def delete_review(review_id: UUID, review: Review):
        # TODO: delete review
        pass
