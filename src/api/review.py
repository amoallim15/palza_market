from fastapi import Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from src.core.model import ListModel, SuccessModel
from src.core.enums import UserType

from src.models.review import ReviewModel, CreateReviewModel, UpdateReviewModel


def main(app):
    @app.get("/review", response_model=ListModel)
    async def reviews(page: int = Query(0, ge=0), page_size: int = 10):
        pipeline = [
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user",
                },
            },
            {"$unwind": "$user"},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "agency_id",
                    "foreignField": "_id",
                    "as": "agency",
                },
            },
            {"$unwind": "$agency"},
            {"$sort": {"_id": -1}},
            {
                "$facet": {
                    "data": [{"$skip": page * page_size}, {"$limit": page_size}],
                    "info": [
                        {"$count": "count"},
                        {"$addFields": {"page": page}},
                        {"$addFields": {"page_size": page_size}},
                    ],
                }
            },
            {"$unwind": "$info"},
        ]
        #
        try:
            result = await app.db["reviews"].aggregate(pipeline).next()
        except StopAsyncIteration:
            result = {"info": {"count": 0, "page": page, "page_size": page_size}}
        return ListModel(**result)

    @app.get("/review/agency/{agency_id}", response_model=ListModel)
    async def reviews_by_agent(
        agency_id: str, page: int = Query(0, ge=0), page_size: int = 10
    ):
        pipeline = [
            {"$match": {"agency_id": agency_id}},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user",
                },
            },
            {"$unwind": "$user"},
            {"$sort": {"_id": -1}},
            {
                "$facet": {
                    "data": [{"$skip": page * page_size}, {"$limit": page_size}],
                    "info": [
                        {"$count": "count"},
                        {"$addFields": {"page": page}},
                        {"$addFields": {"page_size": page_size}},
                    ],
                }
            },
            {"$unwind": "$info"},
        ]
        #
        try:
            result = await app.db["reviews"].aggregate(pipeline).next()
        except StopAsyncIteration:
            result = {"info": {"count": 0, "page": page, "page_size": page_size}}
        return ListModel(**result)

    @app.get("/review/{review_id}", response_model=ReviewModel)
    async def get_review(review_id: str):
        data = await app.db["reviews"].find_one({"_id": review_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Review not found.")
        #
        return ReviewModel(**data)

    @app.post("/review", response_model=ReviewModel)
    async def create_review(
        agency_id: str,
        review: CreateReviewModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_type != UserType.INDIVIDUAL:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        agency = app.db["users"].find_one({"agency_id": review.agency_id})
        if not agency:
            raise HTTPException(status_code=400, detail="Agency does not exist.")
        #
        review = jsonable_encoder(review)
        #
        review["user_id"] = str(current_user.id)
        #
        result = await app.db["reviews"].insert_one(review)
        data = await app.db["reviews"].find_one({"_id": result.inserted_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Review not found.")
        #
        return ReviewModel(**data)

    @app.put("/review/{review_id}", response_model=ReviewModel)
    async def update_review(
        review_id: str,
        review: UpdateReviewModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_type != UserType.INDIVIDUAL:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        data = await app.db["reviews"].find_one({"_id": review_id})
        if not data:
            raise HTTPException(status_code=404, detail="Review not found.")
        if data["user_id"] != str(current_user.id):
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        review = jsonable_encoder(review)
        await app.db["reviews"].update_one({"_id": review_id}, {"$set": review})
        data = await app.db["reviews"].find_one({"_id": review_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Review not found.")
        #
        return ReviewModel(**data)

    @app.delete("/review/{review_id}", response_model=SuccessModel)
    async def delete_review(
        review_id: str,
        current_user=Depends(app.current_user),
    ):
        if current_user.user_type != UserType.INDIVIDUAL:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        data = await app.db["reviews"].find_one({"_id": review_id})
        if not data:
            raise HTTPException(status_code=404, detail="Review not found.")
        if data["user_id"] != str(current_user.id):
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        result = await app.db["reviews"].delete_one({"_id": review_id})
        if result.deleted_count == 1:
            return SuccessModel()
        #
        raise HTTPException(status_code=404, detail="Review not found.")
