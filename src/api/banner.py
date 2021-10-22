from fastapi import Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from src.core.utils import update_image, short_uuid
from src.core.model import ListModel, SuccessModel
from src.core.enums import UserRole, BannerLocation

from src.models.banner import BannerModel


def main(app):
    @app.get("/banner-locations", response_model=ListModel)
    async def banner_locations():
        data_list = list(map(lambda x: {x.name: x.value}, BannerLocation))
        return ListModel(page=0, count=len(data_list), data=data_list)

    @app.get("/banner", response_model=ListModel)
    async def banners():
        cursor = app.db["banners"].find()
        data_list = []
        #
        async for banner in cursor:
            data_list.append(BannerModel(**banner))
        #
        return ListModel(page=0, count=len(data_list), data=data_list)

    @app.get("/banner/{location}", response_model=BannerModel)
    async def get_banner(location: str):
        data = await app.db["banners"].find_one({"location": location})
        if data is None:
            raise HTTPException(status_code=404, detail="Banner not found.")
        #
        return BannerModel(**data)

    @app.put("/banner/{location}", response_model=BannerModel)
    async def put_banner(
        location: str,
        banner: BannerModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        if location not in list(map(lambda x: x.value, BannerLocation)):
            raise HTTPException(status_code=400, detail="Invalid banner location.")
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
        await app.db["banners"].update_one(
            {"location": location}, {"$set": banner}, upsert=True
        )
        #
        data = await app.db["banners"].find_one({"location": location})
        if data is None:
            raise HTTPException(status_code=404, detail="Banner not found.")
        #
        return BannerModel(**data)

    @app.delete("/banner/{location}", response_model=SuccessModel)
    async def delete_banner(
        location: str,
        current_user=Depends(app.current_user),
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        result = await app.db["banners"].delete_one({"location": location})
        if result.deleted_count == 1:
            return SuccessModel()
        #
        raise HTTPException(status_code=404, detail="Banner not found.")
