from fastapi import Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from src.core.utils import update_image, short_uuid
from src.core.model import ListModel, SuccessModel
from src.core.enums import UserRole, BannerLocation

from src.models.banner import (
    BannerModel,
    UpdateBannerModel,
)


def main(app):
    @app.get("/banner-locations", response_model=ListModel)
    async def banner_locations():
        data_list = list(map(lambda x: {x.name: x.value}, BannerLocation))
        print(data_list)
        return ListModel(page=0, count=len(data_list), data=data_list)

    @app.get("/banner", response_model=ListModel)
    async def banners(page: int = Query(0, ge=0)):
        page_size = app.config["APP"]["page_size"]
        #
        cursor = app.db["banners"].find().skip(page * page_size).limit(page_size)
        count = await app.db["banners"].count_documents({})
        data_list = []
        #
        async for banner in cursor:
            data_list.append(BannerModel(**banner))
        #
        return ListModel(page=page, count=count, data=data_list)
        # TODO:
        pass

    @app.get("/banner/{location}", response_model=BannerModel)
    async def get_banner(location: str):
        data = await app.db["banners"].find_one({"location": location})
        if data is None:
            raise HTTPException(status_code=404, detail="Banner not found.")
        #
        return BannerModel(**data)

    @app.post("/banner", response_model=BannerModel)
    async def create_banner(
        banner: BannerModel = Body(...), current_user=Depends(app.current_user)
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        duplicated_banner_location = app.db["banner"].find_one(
            {"location": banner.location}
        )
        if duplicated_banner_location:
            raise HTTPException(status_code=400, detail="Duplicated Banner location.")
        #
        image_urls = []
        for index, image_url in enumerate(banner.image_urls):
            image_urls.push(
                update_image(
                    app=app,
                    old_path=image_url,
                    new_path=f"banners/{banner.id}",
                    name=f"{short_uuid()}-image-{index}",
                )
            )
        banner.image_urls = image_urls
        #
        banner = jsonable_encoder(banner)
        result = await app.db["banners"].insert_one(banner)
        data = await app.db["banners"].find_one({"_id": result.inserted_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Banner not found.")
        #
        return BannerModel(**data)

    @app.put("/banner/{banner_id}", response_model=BannerModel)
    async def update_banner(
        banner_id: str,
        banner: UpdateBannerModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        duplicated_banner_location = app.db["banner"].find_one(
            {"location": banner.location}
        )
        if duplicated_banner_location and duplicated_banner_location._id != banner_id:
            raise HTTPException(status_code=400, detail="Banner location is taken.")
        #
        for index, image_url in enumerate(banner.image_urls):
            if "tmp" in image_url:
                banner.image_urls[index] = update_image(
                    app=app,
                    old_path=image_url,
                    new_path=f"banners/{banner.id}",
                    name=f"{short_uuid()}-image-{index}",
                )
        #
        banner = jsonable_encoder(banner)
        await app.db["banners"].update_one({"_id": banner_id}, {"$set": banner})
        data = await app.db["banners"].find_one({"_id": banner_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Banner not found.")
        #
        return BannerModel(**data)

    @app.delete("/banner/{banner_id}", response_model=SuccessModel)
    async def delete_banner(
        banner_id: str,
        current_user=Depends(app.current_user),
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        result = await app.db["banners"].delete_one({"_id": banner_id})
        if result.deleted_count == 1:
            return SuccessModel()
        #
        raise HTTPException(status_code=404, detail="Banner not found.")
