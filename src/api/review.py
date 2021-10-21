from fastapi import Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from src.core.model import ListModel, SuccessModel
from src.core.enums import UserType

from src.models.review import ReviewModel, UpdateReviewModel


def main(app):
    @app.get("/review", response_model=ListModel)
    async def reviews(page: int = Query(0, ge=0)):
        page_size = app.config["APP"]["page_size"]
        #
        cursor = app.db["reviews"].find().skip(page * page_size).limit(page_size)
        count = await app.db["reviews"].count_documents({})
        data_list = []
        #
        async for review in cursor:
            data_list.append(ReviewModel(**review))
        #
        return ListModel(page=page, count=count, data=data_list)

    @app.get("/review/agent/{agency_id}", response_model=ListModel)
    async def reviews_by_agent(agency_id: str, page: int = Query(0, ge=0)):
        page_size = app.config["APP"]["page_size"]
        #
        cursor = (
            app.db["reviews"]
            .find({"agency_id": agency_id})
            .skip(page * page_size)
            .limit(page_size)
        )
        count = await app.db["reviews"].count_documents({"agency_id": agency_id})
        data_list = []
        #
        async for review in cursor:
            data_list.append(ReviewModel(**review))
        #
        return ListModel(page=page, count=count, data=data_list)

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
        review: ReviewModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_type != UserType.CLIENT:
            raise HTTPException(status_code=403, detail="Not allowed.")
        # 
        agency = app.db["users"].find_one({"agency_id": review.agency_id})
        if not agency:
            raise HTTPException(status_code=400, detail="Agency does not exist.")
        #
        review = jsonable_encoder(review)
        # 
        review["user_id"] = current_user.id
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
        if current_user.user_type != UserType.CLIENT:
            raise HTTPException(status_code=403, detail="Not allowed.")
        # 
        data = await app.db["reviews"].find_one({"_id": review_id })
        if not data:
            raise HTTPException(status_code=404, detail="Review not found.")
        if data["user_id"] != current_user.id:
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
        if current_user.user_type != UserType.CLIENT:
            raise HTTPException(status_code=403, detail="Not allowed.")
        # 
        data = await app.db["reviews"].find_one({"_id": review_id })
        if not data:
            raise HTTPException(status_code=404, detail="Review not found.")
        if data["user_id"] != current_user.id:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        result = await app.db["reviews"].delete_one({"_id": review_id})
        if result.deleted_count == 1:
            return SuccessModel()
        #
        raise HTTPException(status_code=404, detail="Review not found.")
